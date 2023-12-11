from copy import deepcopy
import random
import sympy
from typing import List
from symqc.kernel.circuit import CircMsmt, CircGate, Circuit
from symqc.kernel.utils import *
from symqc.kernel.gate import Gate, ParametersGate
from symqc.kernel.qubit_name_manager import QubitNameManager


class Qubit:
    def __init__(self, qsim, num: int):
        self.id = id(qsim)
        self.rnk = num


class Qsim:
    def __init__(self, num_qubits: int = 1):
        """Create a simulator instance with `num_qubits` qubits

        Parameters
        ----------
        num_qubits : int
            The number of qubits in simulation.
        """

        self.state = None
        self.num_qubits = num_qubits
        self.global_circuit = None

    def state_valid(self):
        if self.state is None:
            raise Exception("state is None")
        norm = sum([amp * amp.conjugate() for amp in self.state])
        if not sympy.simplify(norm - 1) == 0:
            raise Exception(
                "state is invalid because the norm is not 1 ({})".format(latex(norm))
            )
        return True

    def system_size(self) -> int:
        """Return the number of qubits in the system."""
        return self.num_qubits

    def qubit(self, num: int) -> Qubit:
        return Qubit(self, num)

    def init_to_basis(self, basis: str) -> None:
        """Initialize the quantum state into a basis state.

        Parameters
        ----------
        basis : str
            The binary string of the basis, like '000', '101', etc.
            Note, the number of bits in the string must be equal to the number of qubits.
        """
        if len(basis) != self.system_size():
            raise Exception("error basis")
        self.state = sympy.zeros(1 << self.system_size(), 1)
        idx = int(basis, 2)
        self.state[idx] = 1

    def state_vector(self):
        return self.state

    def qubits(self, *argv) -> list:
        res = []
        if len(argv) == 0:
            raise Exception("None qubits")
        if isinstance(argv[0], list):
            res = argv[0]
            if len(res) == 0:
                raise Exception("None qubits")
        else:
            res = argv
        return [Qubit(self, i) for i in res]

    def checkQubit(self, qubit: Qubit) -> bool:
        """Check if the given qubit is a valid qubit of this simulator.

        Parameters
        ----------
        qubit : Qubit
            The qubit to be checked within this simulator.

        Returns
        -------
        bool
            True on valid.
        """
        return id(self) == qubit.id and self.system_size() > qubit.rnk

    def apply(self, gate: Gate, *argv, **argc) -> sympy.Matrix:
        if len(argv) <= 0:
            raise Exception("error target_qubits input")
        target_qubits = []
        if isinstance(argv[0], list):
            if len(argv[0]) <= 0 or (not isinstance(argv[0][0], Qubit)):
                raise Exception("error target_qubits input")
            target_qubits = [i for i in argv[0] if (isinstance(i, Qubit))]
        else:
            target_qubits = [i for i in argv if (isinstance(i, Qubit))]

        if len(target_qubits) == 0:
            raise Exception("error target_qubits input")

        for i in target_qubits:
            if not self.checkQubit(i):
                raise Exception("error target_qubits input")

        target_qubits = [i.rnk for i in target_qubits]

        parameters = argc.get("parameters")
        extra_ctrl_qubits = argc.get("extra_ctrl_qubits")

        if len(target_qubits) != gate.num_targets + gate.num_controls:
            raise Exception("target_qubits are not match gate")

        return self.apply_gate(
            gate,
            target_qubits,
            parameters=parameters,
            extra_ctrl_qubits=extra_ctrl_qubits,
        )

    def apply_gate(self, gate: CircGate, parameters: list = []) -> sympy.Matrix:
        target_qubits = gate.target_qubits
        extra_ctrl_qubits = gate.control_qubits
        bold_gate = gate.gate
        ctrl_qubits = target_qubits[0 : bold_gate.num_controls] + extra_ctrl_qubits
        target_qubits = target_qubits[bold_gate.num_controls :]

        if isinstance(gate, ParametersGate):
            core_mat = bold_gate.get_matrix(
                get_discrete(target_qubits), parameters=parameters
            )
        else:
            core_mat = bold_gate.get_matrix(get_discrete(target_qubits))

        # TODO: it seems that target qubit order is used on above lines, which might cause extra computation. We can fix it later.

        target_qubits.sort()
        target_qubit_mask = get_mask(target_qubits)
        # Generate a list of addresses with $2^n$ elements, where $n$
        # is the number of target qubits of the gate.
        # This adddress list defines the relative location of amplitudes
        # of the substate that is affected by the gate.
        # Refer the SymQC paper section 4.1.2 for more details.
        # `ele_addr_in_Bk` corresponds to $B_k$ in the paper.
        ele_addr_in_Bk = sorted(gen_subset(target_qubit_mask))

        other_qubits_mask = get_inverse_mask(target_qubits, self.system_size())
        # ctrl_qubit_mask being 0 means there is no control qubit
        ctrl_qubit_mask = get_mask(ctrl_qubits)

        base_addr_list = gen_subset(other_qubits_mask)

        for base_addr in base_addr_list:
            # TODO: check if the sencond condition is correct
            # what we want is that all control qubits are ones, i.e.,
            # `base_addr | ctrl_qubit_mask == base_addr`
            if ctrl_qubit_mask == 0 or base_addr & ctrl_qubit_mask:
                sub_state_addrs = [(base_addr | i) for i in ele_addr_in_Bk]
                sub_state = sympy.Matrix([self.state[i] for i in sub_state_addrs])
                sub_state = core_mat * sub_state
                for addr, amplitude in zip(sub_state_addrs, sub_state):
                    self.state[addr] = amplitude
        return self.state

    def getQubitState(self, qubit):
        pos = 0
        if isinstance(qubit, Qubit):
            if not self.checkQubit(qubit):
                raise Exception("this qubit is not in this state")
            pos = qubit.rnk
        elif isinstance(qubit, int):
            if qubit >= self.num_qubits:
                raise Exception("this qubit is not in this state")
            pos = qubit
        else:
            raise Exception("error qubit ")

        res = sympy.Matrix([0, 0])
        for i in range(1 << self.num_qubits):
            if i & (1 << pos) != 0:
                res[0, 0] += self.state[i, 0]
            else:
                res[1, 0] += self.state[i, 0]
        res[0, 0] = sympy.simplify(res[0, 0])
        res[1, 0] = sympy.simplify(res[1, 0])
        return res


class StateVectorSimulator(Qsim):
    def __init__(self, num_qubits: int, qubit_names: List[int]):
        super().__init__(num_qubits=num_qubits)
        self.qnm = QubitNameManager(qubit_names)

        # init the state to |00...0>
        self.state = sympy.zeros(1 << num_qubits, 1)
        self.state[0] = 1

        self.msmt_history = []

    def get_msmt_trace(self):
        return self.msmt_history

    def get_qubit_names(self):
        return self.qnm.get_qubit_names()

    def apply_msmt(self, msmt_op: CircMsmt):
        """Apply a measurement operation and update the state vector in the simulator."""
        return self.perform_msmt(msmt_op, update=True)

    def sample_msmt(self, msmt_op: CircMsmt):
        """Retrieve the result of a measurement operation by sampling the state vector
        in the simulator, but without modifying this state vector."""
        return self.perform_msmt(msmt_op, update=False)

    def perform_msmt(self, msmt_op: CircMsmt, update: bool = False):

        ########## sample stage ##########
        target_qubits = msmt_op.target_qubits
        # [self.qnm.to_idx(qubit) for qubit in msmt_op.target_qubits qubits_list]
        target_qubit_mask = get_mask(target_qubits)
        bases = sorted(gen_subset(target_qubit_mask))
        other_qubits_mask = get_inverse_mask(target_qubits, self.system_size())
        base_addr_list = gen_subset(other_qubits_mask)

        basis_prob = []
        for basis in bases:
            prob = 0
            for base_addr in base_addr_list:
                addr = base_addr | basis
                prob += self.state[addr] * self.state[addr].conjugate()
            basis_prob.append((basis, prob))

        msmt_res = None

        rand_val = random.random()
        for basis, prob in basis_prob:
            if rand_val < prob:
                msmt_res = basis, prob
                break
            rand_val -= prob

        if msmt_res is None:
            raise Exception("measure error")

        measured_basis = msmt_res[0]

        idx_result = extract_qubit_res(target_qubits, measured_basis)

        msmt_result = [(idx, bit) for idx, bit in idx_result]

        ########## update stage ##########
        if update:
            prob = msmt_res[1]
            new_state = sympy.zeros(1 << self.system_size(), 1)
            for base_addr in base_addr_list:
                addr = base_addr | measured_basis
                new_state[addr] = self.state[addr]
            new_state /= Abs(sympy.sqrt(prob))
            self.state = sympy.simplify(new_state)

            self.msmt_history.extend(msmt_result)

        return msmt_result
