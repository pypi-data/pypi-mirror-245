from symqc import Qsim, Gate, Circuit
from sympy import pprint, Matrix, symbols, sqrt, pi, cos, sin, I, exp, simplify
from symqc.kernel.gates_lib import H, Z, CNOT, CZ
from symqc.qcis.instr import QCIS_instr, QCISOpCode
from symqc.kernel.circuit import split_insns
import pytest


def test_split_insns():
    insns1 = [QCIS_instr(QCISOpCode.X, qubit=[0])]

    insns2 = [
        QCIS_instr(QCISOpCode.X, qubit=[0]),
        QCIS_instr(QCISOpCode.Y2M, qubit=[0]),
        QCIS_instr(QCISOpCode.MEASURE, qubits_list=[0]),
    ]

    insns3 = [
        QCIS_instr(QCISOpCode.MEASURE, qubits_list=[0]),
        QCIS_instr(QCISOpCode.X, qubit=[0]),
        QCIS_instr(QCISOpCode.MEASURE, qubits_list=[0]),
    ]

    msmt_mid1, gate_or_msmt1, msmt1 = split_insns(insns1)
    msmt_mid2, gate_or_msmt2, msmt2 = split_insns(insns2)
    msmt_mid3, gate_or_msmt3, msmt3 = split_insns(insns3)

    assert msmt_mid1 is False and msmt_mid2 is False and msmt_mid3 is True

    assert (
        len(gate_or_msmt1) == 1 and len(
            gate_or_msmt2) == 2 and len(gate_or_msmt3) == 3
    )

    assert len(msmt1) == 0 and len(msmt2) == 1 and len(msmt3) == 0


def test_get_matrix_from_mixed_prog():
    insns = [
        QCIS_instr(QCISOpCode.MEASURE, qubits_list=["Q1"]),
        QCIS_instr(QCISOpCode.H, qubit="Q0"),
        QCIS_instr(QCISOpCode.CNOT, target_qubit="Q1", control_qubit="Q0"),
        QCIS_instr(QCISOpCode.MEASURE, qubits_list=["Q0"]),
    ]
    circ = Circuit.from_qcis_insns(insns, ["Q0", "Q1"])
    with pytest.raises(ValueError, match="Measurement in the middle is not supported"):
        mat = circ.get_matrix()


def test_from_qcis_insns():
    insns = [
        QCIS_instr(QCISOpCode.H, qubit="Q1"),
        QCIS_instr(QCISOpCode.CNOT, target_qubit="Q0", control_qubit="Q1"),
        QCIS_instr(QCISOpCode.MEASURE, qubits_list=["Q0", "Q1"]),
    ]
    circ = Circuit.from_qcis_insns(insns, ["Q0", "Q1"])
    print(circ.get_matrix())
    assert circ.get_matrix() == Matrix(
        [
            [sqrt(2) / 2, 0, sqrt(2) / 2, 0],
            [0,  sqrt(2) / 2, 0, sqrt(2) / 2],
            [0, sqrt(2) / 2,  0, -sqrt(2) / 2],
            [sqrt(2) / 2, 0, -sqrt(2) / 2, 0]
        ]
    )
