from symqc.kernel.utils import *


def test_extract_qubit_res():
    qubits = [1, 2, 5]
    basis = 0b000000
    assert extract_qubit_res(qubits, basis) == [(1, 0), (2, 0), (5, 0)]

    basis = 0b000001
    assert extract_qubit_res(qubits, basis) == [(1, 0), (2, 0), (5, 0)]

    basis = 0b000010
    assert extract_qubit_res(qubits, basis) == [(1, 1), (2, 0), (5, 0)]

    basis = 0b000100
    assert extract_qubit_res(qubits, basis) == [(1, 0), (2, 1), (5, 0)]

    basis = 0b100100
    assert extract_qubit_res(qubits, basis) == [(1, 0), (2, 1), (5, 1)]

    basis = 0b001111
    assert extract_qubit_res(qubits, basis) == [(1, 1), (2, 1), (5, 0)]


if __name__ == "__main__":
    test_extract_qubit_res()
