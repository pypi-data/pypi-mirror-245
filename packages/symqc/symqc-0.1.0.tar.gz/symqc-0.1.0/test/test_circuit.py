from symqc import Qsim, Gate, Circuit
from sympy import pprint, Matrix, symbols, sqrt, pi, cos, sin, I, exp, simplify
from symqc.kernel.gates_lib import H, Z, CNOT, CZ, X, RZ
from symqc.qcis.instr import QCIS_instr, QCISOpCode
from symqc.kernel.circuit import split_insns
import pytest


def test_cz():
    Z = Gate([[1, 0], [0, -1]])
    circ = Circuit(2)
    circ.add_bare_gate(Z, [0], [1])
    assert circ.get_matrix() == Matrix(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]
    )


def test_ccnot():
    X = Gate([[0, 1], [1, 0]])
    circ = Circuit(3)
    circ.add_bare_gate(X, target_qubits=[0], control_qubits=[1, 2])
    assert circ.get_matrix() == Matrix(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
        ]
    )


def test_in_gate_control():
    CCX = Gate([[0, 1], [1, 0]], 2)
    circ = Circuit(3)
    circ.add_bare_gate(CCX, [0, 1, 2])
    assert circ.get_matrix() == Matrix(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
        ]
    )


def cz_h_cnot():
    h = H()
    cnot = CNOT()
    cz = CZ()

    cnot_circ = Circuit(2)
    cnot_circ.add_bare_gate(cnot, [0, 1])

    cz_circ = Circuit(2)
    cz_circ.add_bare_gate(h, 0)
    cz_circ.add_bare_gate(cz, [0, 1])
    cz_circ.add_bare_gate(h, 0)

    assert cnot_circ.get_matrix() == cz_circ.get_matrix()


def test_rz():
    x = X()
    rz1 = RZ(pi/2)
    rz2 = RZ(-pi/2)

    rz1_circ = Circuit(1)
    rz1_circ.add_bare_gate(x, 0)
    rz1_circ.add_bare_gate(rz1, 0)
    rz1_circ.add_bare_gate(x, 0)

    rz2_circ = Circuit(1)
    rz2_circ.add_bare_gate(rz2, 0)
    assert rz1_circ.get_matrix() == rz2_circ.get_matrix()


if __name__ == "__main__":
    test_cz()
    test_ccnot()
    test_in_gate_control()
    cz_h_cnot()
    test_rz()
