import opcode
from tokenize import String
from typing import List
from math import log2
import sympy
from symqc.kernel.gates_lib import lib_gate
from symqc.kernel.utils import (
    gen_subset,
    get_inverse_mask,
    get_mask,
    map_bit,
    remap_bits,
)
from symqc.kernel.utils import gamma
from symqc.kernel.gate import Gate
from symqc.kernel.qubit_name_manager import QubitNameManager
from symqc.qcis.instr import QCIS_instr, QCISOpCode

"""
The implementation of class Circuit
"""


def split_insns(instructions):
    """Split the program into two parts, i.e., gates and measurements.

    Args:
        instructions (list[QCIS_Instr]): the list of QCIS instructions
    Return:
        a tuple: (gates, measurements)
    """
    first_msmt_idx = len(instructions)
    for i, insn in enumerate(instructions):
        if insn.op_code.is_measure_op():
            first_msmt_idx = i
            break

    msmt_in_the_middle = False
    for i in range(first_msmt_idx, len(instructions)):
        if not instructions[i].op_code.is_measure_op():
            msmt_in_the_middle = True

    if msmt_in_the_middle:
        return True, instructions, []
    else:
        return False, instructions[:first_msmt_idx], instructions[first_msmt_idx:]


class CircOp:
    def __init__(self, target_qubits: List[int]) -> None:
        """The base class of a circuit operation.

        A circuit operation is a gate or a measurement.
        """
        self.target_qubits = target_qubits


class CircGate(CircOp):
    def __init__(self, gate: Gate, target_qubits: List[int], control_qubits=[]):
        """Create a circuit gate.

        Args:
            gate (Gate): the gate
            target_qubits (list of int): the target qubit
            control_qubits (list of int):
                optional control qubits. Default to [].
        """
        super().__init__(target_qubits)
        self.gate = gate
        self.control_qubits = control_qubits

    def __str__(self) -> str:
        s = "gate: {}\ntargets: {}".format(self.gate, str(self.target_qubits))
        if len(self.control_qubits) != 0:
            s += "\ncontrols: {}".format(str(self.control_qubits))
        return s


class CircMsmt(CircOp):
    def __init__(self, target_qubits: List[int]):
        """Create a measurement operator.

        Args:
            qubits (list): a list of qubits, each qubit is represented
            by an integer.
        """
        super().__init__(target_qubits)


class Circuit(QubitNameManager):
    def __init__(self, num_qubits: int, qubit_names: List[str] = []):
        """Createa a quantum circuit with a list of qubits specified by
        `qubit_names`. Gates and measurements can be added to the circuit
        later.

        Though we can mix gates and measurements in a circuit, we currently
        only support all measurements at the end of the circuit.

        Args:
            num_qubits (_type_): _description_
            qubit_names (list, optional): _description_. Defaults to [].
        """
        super().__init__(qubit_names=qubit_names)
        self.num_qubits = num_qubits  # the number of qubits

        # When msmt_in_the_middle is True, all gates and measurements are
        # mixed in `all_ops`. Otherwise, `gates` and `msmts` are used separately.
        self.msmt_in_the_middle = False
        self.all_ops = []

        self.gates = []  # gates, only valid when msmt_in_the_middle is False
        self.msmts = []  # measurements, only valid when msmt_in_the_middle is False

        self.mat_size = 2**num_qubits
        self.matrix = None
        self._mat_valid = False

    @staticmethod
    def from_qcis_insns(qcis_insns: List[QCIS_instr], names: List[str]):
        circuit = Circuit(len(names), names)
        msmt_in_mid, gate_or_msmt_insns, msmt_insns = split_insns(qcis_insns)
        circuit.msmt_in_the_middle = msmt_in_mid
        if msmt_in_mid:
            for insn in gate_or_msmt_insns:
                if insn.op_code.is_measure_op():
                    circuit.add_qcis_msmt(insn, mixed=True)
                else:
                    circuit.add_qcis_gate(insn, mixed=True)
        else:
            for gate_insn in gate_or_msmt_insns:
                circuit.add_qcis_gate(gate_insn, mixed=False)
            for msmt_insn in msmt_insns:
                circuit.add_qcis_msmt(msmt_insn, mixed=False)

        return circuit

    def add_qcis_msmt(self, measure_insn: QCIS_instr, mixed=False):
        """Add a measurement defined by a QCIS measure instruction."""
        qubits = [self.to_idx(qubit_name) for qubit_name in measure_insn.qubits_list]

        if mixed:
            self.all_ops.append(CircMsmt(qubits))
        else:
            self.msmts.append(CircMsmt(qubits))

    def add_qcis_gate(self, gate_insn: QCIS_instr, mixed=False):
        """Add a gate defined by a QCIS gate instruction."""
        gate = lib_gate(gate_insn)

        if gate_insn.op_code.is_single_qubit_op():
            assert gate.num_total_qubits == 1
            target = [self.to_idx(gate_insn.qubit)]
            circ_gate = CircGate(gate, target, [])

        elif gate_insn.op_code.is_two_qubit_op():
            assert gate.num_total_qubits == 2
            target = self.to_idx(gate_insn.target_qubit)
            ctrl = self.to_idx(gate_insn.control_qubit)
            assert ctrl != target
            circ_gate = CircGate(gate, [target, ctrl], [])
        elif gate_insn.op_code.is_three_qubit_op():
            if gate_insn.op_code == QCISOpCode.Toffoli:
                assert gate.num_total_qubits == 3
                target = self.to_idx(gate_insn.target_qubit)
                ctrl1 = self.to_idx(gate_insn.control_qubit1)
                ctrl2 = self.to_idx(gate_insn.control_qubit2)
                assert ctrl1 != target and ctrl2 != target and ctrl1 != ctrl2
                circ_gate = CircGate(gate, [target, ctrl1, ctrl2], [])
        else:
            raise ValueError("Unsupported gate: {}".format(gate_insn))

        self.add_gate(circ_gate, mixed)

    def add_bare_gate(
        self, gate: Gate, target_qubits: List[int], control_qubits: List[int] = []
    ):
        """Add a gate defined by a Gate object."""
        if isinstance(target_qubits, int):
            target_qubits = [target_qubits]
        if isinstance(control_qubits, int):
            control_qubits = [control_qubits]
        for qubit in target_qubits + control_qubits:
            if qubit >= self.num_qubits:
                raise ValueError(
                    "The qubit index {} is out of range. max number of "
                    "qubits in the circuit is {}.".format(qubit, self.num_qubits)
                )
        circ_gate = CircGate(gate, target_qubits, control_qubits)
        self.add_gate(circ_gate)

    def add_gate(self, gate: CircOp, mixed: bool = False):
        """
        Add a gate to the circuit.

        Parameters
        ----------
        gate:
            The gate to be added.
        target:
            The target qubits.
        ctrl:
            The control qubits.
        """
        if mixed:
            self.all_ops.append(gate)
        else:
            self.gates.append(gate)

        self.invalidate_mat_cache()

    def add_gates(self, gates: List[Gate]):
        """
        Add a list of gates to the circuit.

        Parameters
        ----------
        Gates:
            A list of three-element tuples (gate, target qubits, control qubits).
        """
        for gate in gates:
            self.add_gate(*gate)

    def expand_gate(
        self, core_mat: sympy.Matrix, t_qubits: List[int], c_qubits: List[int] = []
    ):
        """Expand a gate to a matrix of the entire circuit.
        The size of the matrix is determined by the total number of qubits in the circuit.

        Args:
            core_mat (sympy.Matrix): the core matrix of the gate
            t_qubits (list): the target qubits
            c_qubits (list, optional): optional control qubits. Defaults to [].

        Returns:
            sympy.Matrix: the expanded matrix.
        """
        if log2(core_mat.shape[0]) != len(t_qubits):
            raise ValueError("The number of qubits is not correct")

        o_qubits = []
        used_qubits = t_qubits + c_qubits
        for i in range(self.num_qubits):
            if i not in used_qubits:
                o_qubits.append(i)

        num_target_qubits = len(t_qubits)
        num_other_qubits = len(o_qubits)
        num_ctrl_qubits = len(c_qubits)

        assert self.num_qubits == num_target_qubits + num_other_qubits + num_ctrl_qubits

        new_mat_size = 2 ** (num_target_qubits + num_other_qubits + num_ctrl_qubits)
        new_mat = sympy.zeros(new_mat_size, new_mat_size)

        for o_val in range(2**num_other_qubits):
            for ctrl_val in range(2**num_ctrl_qubits - 1):
                # not all control qubits are 1, so do nothing
                for tgt_idx in range(2**num_target_qubits):
                    iden_idx = (
                        remap_bits(o_val, o_qubits)
                        + remap_bits(ctrl_val, c_qubits)
                        + remap_bits(tgt_idx, t_qubits)
                    )
                    new_mat[iden_idx, iden_idx] = 1

            # all control qubits are 1, we need to apply the gate
            all_ones = 2**num_ctrl_qubits - 1
            for t_val in range(2**num_target_qubits):
                for i in range(2**num_target_qubits):
                    row_idx = gamma(
                        t_val, t_qubits, o_val, o_qubits, all_ones, c_qubits
                    )
                    col_idx = gamma(i, t_qubits, o_val, o_qubits, all_ones, c_qubits)
                    new_mat[row_idx, col_idx] = core_mat[t_val, i]
        return new_mat

    def invalidate_mat_cache(self):
        """Invalidate the matrix cache of the entire circuit.
        Usually called upon initialization and adding new gates.
        """
        self._mat_valid = False

    def get_matrix(self):
        """
        Get the equivalent matrix of the circuit by expanding the each gate
        in the circuit.

        Returns
        -------
        The matrix of the circuit.
        """
        if self.msmt_in_the_middle:
            raise ValueError("Measurement in the middle is not supported")

        if self._mat_valid:
            return self._matrix

        self._matrix = sympy.eye(2**self.num_qubits)
        if len(self.gates) == 0:
            return self._matrix

        # calculate the matrix of each gate, and multiply them together
        for circ_gate in self.gates:
            print("cric_gate: ", circ_gate)
            gate = circ_gate.gate
            target_qubits = circ_gate.target_qubits
            ctrl_qubits = circ_gate.control_qubits

            core_mat = gate.get_matrix()
            num_inner_targets = gate.num_targets
            num_inner_ctrls = gate.num_controls

            if len(target_qubits) != num_inner_targets + num_inner_ctrls:
                raise ValueError(
                    "The number of target qubits ({}) is does not match the exepcted number ({}).".format(
                        len(target_qubits), num_inner_targets + num_inner_ctrls
                    )
                )

            ctrl_qubits = ctrl_qubits + target_qubits[num_inner_targets:]
            target_qubits = target_qubits[:num_inner_targets]

            expanded_mat = self.expand_gate(core_mat, target_qubits, ctrl_qubits)

            self._matrix = expanded_mat * self._matrix

        self._mat_valid = True
        return self._matrix

    # TODO: this method is used to calculate the equivalent matrix of two parallel gates.
    # It is not used in the current version of the simulator, which can be added later.
    @staticmethod
    def combine_gates(gates: list, n):
        """Build the utility matrix of these gates"""
        vis = [0] * n
        mark = 0
        res = sympy.ones(2**n, 2**n)
        blnk = []

        for g, opt_list, ctrl_list in gates:
            mark = 0
            for i in opt_list:
                vis[i] = 1
            for i in ctrl_list:
                vis[i] = 1

        blnk = [i for i in range(len(vis)) if vis[i] == 0]
        vis = [i for i in range(len(vis)) if vis[i] != 0]

        matI = sympy.eye(2)

        for p in blnk:
            addr = gen_subset(get_inverse_mask([p], n))
            for i in range(matI.rows):
                for j in range(matI.cols):
                    for si in addr:
                        mi = map_bit(i, si, [p])
                        for sj in addr:
                            mj = map_bit(j, sj, [p])
                            res[mi, mj] = res[mi, mj] * matI[i, j]

        for g, opt_list, ctrl_list in gates:
            bits = opt_list + ctrl_list

            mark = get_inverse_mask(bits, n)
            addr = gen_subset(mark)
            mat = g.get_matrix(
                range(g.num_targets),
                range(g.num_targets, g.num_targets + g.num_controls),
                g.num_targets + g.num_controls,
            )

            for i in range(mat.rows):
                for j in range(mat.cols):
                    for si in addr:
                        mi = map_bit(i, si, bits)
                        for sj in addr:
                            mj = map_bit(j, sj, bits)
                            res[mi, mj] = res[mi, mj] * mat[i, j]

        return res
