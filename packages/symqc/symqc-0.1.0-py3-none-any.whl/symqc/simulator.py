from pathlib import Path
from sympy import Matrix, simplify, latex
from symqc.kernel.utils import set_bit, str_bin
from symqc.qcis.parser import QCISParser, QCISOpCode
from symqc.kernel.qubit import StateVectorSimulator
from symqc.kernel.ket.qubit import Qsim_ket
from symqc.kernel.ket.store import Store_ket
from symqc.output.store import Store
from symqc.output.symbol_map import Symbol_map
from symqc.kernel.circuit import CircMsmt, Circuit
from typing import List
from symqc.kernel.gate import Gate


class SymQC(object):
    def __init__(self, num_qubits: int = 0, names: List[str] = []):
        self.args = None
        self._instructions = None
        self._names = None
        self.filename = None
        self._simulator = None
        self._save = None

        if num_qubits == 0:
            self._circ = None
        else:
            if len(names) == 0:
                names = ["Q{}".format(i) for i in range(num_qubits)]
            self._names = names
            self._circ = Circuit(num_qubits, self._names)

    def add_bare_gate(
        self, gate: Gate, target_qubits: List[int], control_qubits: List[int] = []
    ):
        self._circ.add_bare_gate(gate, target_qubits, control_qubits)

    def compile_file(self, fn):
        """Simulate the QCIS program in the given file.

        Parameters
        ----------
        fn (Path): the path to the QCIS program file.
        """
        if isinstance(fn, str):
            fn = Path(fn)

        with fn.open("r") as f:
            program = f.read()
            self.compile(program)

    def compile(self, program: str):
        """Compile the given QCIS program

        Args:
            program (str): a QCIS program in string format

        Raises:
            ValueError: if the QCIS program cannot be compiled

        Returns:
            a list of QCIS instructions and a list of qubit names
        """
        _parser = QCISParser()
        success, self._instructions, self._names = _parser.parse(data=program)
        if not success:
            print(_parser.error_list)
            raise ValueError("QCIS parser failed to compile the given QCIS program.")
        self._circ = Circuit.from_qcis_insns(self._instructions, self._names)
        return self._circ

    def get_circ_matrix(self):
        """Get the equivalent matrix of this circuit defined by the QCIS file."""
        if self._circ is None:
            raise RuntimeError("No circuit has been defined yet.")

        return self._circ.get_name_idx_map(), self._circ.get_matrix()

    def simulate(
        self,
        work_mode="one_shot",
        num_shots=1000,
        state_repr="full_amp",
        max_num_qubits=0,
        use_symbol: bool = False,
    ):
        """Simulate the compiled QCIS program.

        Parameters
        ----------
        work_mode (str, optional):
            The simulation mode to use. Defaults to "one_shot".
          - "one_shot": the simulation result is a dictionary with each key being a
             qubit measured, and the value is the outcome of measuring this qubit.
          - "final_state": the simulation result is a two-level dictionary:
            {
                'classical': {'Q1': 1, 'Q2': 0},
                'quantum': (['Q3', 'Q4'], array([0, 1, 0, 0]))
            }
        num_shots (int, optional):
            the number of iterations performed in `one_shot` mode. Ignored in other modes.

        state_repr (str, optional):
            The representation of the quantum state. Defaults to "full_amp".
            - "full_amp": the quantum state is represented as a full amplitude vector.
            - "ket": the quantum state is represented using Dirac notation.

        Returns:
            simulation result specified by `work_mode`.
        """
        if self._circ is None:
            raise RuntimeError("No circuit has been defined yet.")

        maps = Symbol_map()
        if use_symbol:
            for insn in self._instructions:
                if insn.op_code == QCISOpCode.RXY:
                    insn.altitude = maps.store_symbol("theta", insn.altitude)
                    insn.azimuth = maps.store_symbol("phi", insn.azimuth)
                elif (
                    insn.op_code == QCISOpCode.XY
                    or insn.op_code == QCISOpCode.XY2P
                    or insn.op_code == QCISOpCode.XY2M
                ):
                    insn.azimuth = maps.store_symbol("phi", insn.azimuth)
                elif (
                    insn.op_code == QCISOpCode.RX
                    or insn.op_code == QCISOpCode.RY
                    or insn.op_code == QCISOpCode.RZ
                ):
                    insn.altitude = maps.store_symbol("theta", insn.azimuth)

        max_num_qubits = max(max_num_qubits, len(self._names))

        if state_repr == "ket":
            self._simulator = Qsim_ket(max_num_qubits, self._names, maps)
            self._save = Store_ket(self._simulator, maps, [])
        elif state_repr == "full_amp":
            self._simulator = StateVectorSimulator(max_num_qubits, self._names)
            self._save = Store(self._simulator, maps, [])
        else:
            raise ValueError("Unknown state representation: {}".format(state_repr))

        if work_mode == "one_shot":
            multi_res = []
            if not self._circ.msmt_in_the_middle:
                for circ_gate in self._circ.gates:
                    self._simulator.apply_gate(circ_gate)

                for i in range(num_shots):
                    measured_qubits = []
                    for msmt in self._circ.msmts:
                        measured_qubits.extend(msmt.target_qubits)
                    big_msmt = CircMsmt(measured_qubits)

                    # only sample the msmt result and keep the original state vector.
                    one_shot_res = self._simulator.sample_msmt(big_msmt)
                    multi_res.append(one_shot_res)

            else:
                for i in range(num_shots):
                    for op in self._circ:
                        self._simulator.apply_op(circ_gate)
                    multi_res.append(self._simulator.get_msmt_trace)
            nl = [
                self._simulator.get_qubit_names()[i]
                for i in self.format_result(multi_res, "last")[0]
            ]
            return (
                nl,
                self.format_result(multi_res, "last")[1],
            )
        elif work_mode == "final_state":
            if not self._circ.msmt_in_the_middle:
                for circ_gate in self._circ.gates:
                    self._simulator.apply_gate(circ_gate)
                classical = {}
                quantum = (
                    self._simulator.get_qubit_names(),
                    self._simulator.state_vector(),
                )
                return {"classical": classical, "quantum": quantum}
            else:
                raise NotImplementedError(
                    " SymQC does not support final state simulation with measurement in the middle yet."
                )
        else:  # pragma: no cover
            raise ValueError("Unknown work mode: {}".format(work_mode))

    def ket_format(self, qubit_names: List[str], state_vec: Matrix, use_latex=False):
        num_qubits = len(qubit_names)
        length = 2**num_qubits
        assert state_vec.shape == (length, 1)
        res_str = ""

        def single_basis(basis):
            amp = state_vec[basis, 0]
            if simplify(amp) == 0:
                return ""

            amp_val = latex(amp) if use_latex else "{}".format(amp)

            amp_str = "" if simplify(amp) == 1 else amp_val

            basis_bin = str_bin(basis, num_qubits)
            basis_str = (
                r"\ket{" + basis_bin + r"}" if use_latex else "|{}>".format(basis_bin)
            )
            return amp_str + basis_str

        full_eles = [single_basis(i) for i in range(length)]
        valid_eles = [ele for ele in full_eles if ele != ""]

        return "+".join(valid_eles)

    def format_result(self, multi_result, res_fmt):
        """Format the simulation results of multiple rounds.

        Args:
            multi_result: measurement result of multiple rounds, like:
                `[[('Q1', 0), ('Q2', 0), ('Q1', 0)],
                  [('Q1', 1), ('Q2', 0), ('Q1', 0)],
                  [('Q1', 1), ('Q2', 1), ('Q1', 1)]]`.
            res_fmt (str): the target format
              - "raw": original trace, nothing is done.
              - "last": only keep the last measurement result of every qubit.
                The above example will be modified to
                    `(['Q1', 'Q2'], ['00', '00', '11'])`
              - "combined": only keep the last measurement result of every qubit and
                return the count.
                The above example will be modified to
                    `(['Q1', 'Q2'], {'00': 2, '11': 1})`
        """
        if res_fmt == "raw":
            return multi_result

        if res_fmt == "last" or res_fmt == "combined":
            if len(multi_result) == 0:
                return [[], []]

            names = list(set([name for name, bit in multi_result[0]]))
            name_to_idx = {}

            for i, name in enumerate(names):
                name_to_idx[name] = i

            results = []
            re_la = []
            for shot in multi_result:
                result = 0
                re = [0] * len(shot)
                for name, bit in shot:
                    re[name] = bit
                    result = set_bit(result, name_to_idx[name], bit)
                re_la.append(re)
                results.append(result)

            if res_fmt == "last":
                return names, re_la

            count_dict = {}
            for result in results:
                if result not in count_dict.keys():
                    count_dict[result] = 1
                else:
                    count_dict[result] = count_dict[result] + 1
            return names, count_dict

    def dump_result(self, prog_fn, out_fn):
        self._save.save_final(self._simulator.state)
        self._save.output_markdown(prog_fn, out_fn)
        # return Q.state.map                      #这里出了一点点问题
