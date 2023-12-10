from symqc import SymQC
from sympy import pprint


def test_symqc_matrix():
    qc = SymQC()
    prog = """
    X Q2
    X Q3
    TOFFOLI Q3 Q2 Q1
    """
    qc.compile(prog)
    qc.simulate()
    qubits, mat = qc.get_circ_matrix()
    print(qubits)
    pprint(mat)

def test_symqc_rz():
    qc = SymQC()
    prog = """
    RZ Q0 0
    """
    qc.compile(prog)

def test_toffoli_decompose():
    qc = SymQC()
    prog= """
    S    Q3
 CNOT    Q2           Q3
   RY    Q3   -0.7853982
 CNOT    Q2           Q3
   RY    Q3    0.7853982
   SD    Q3
    T    Q2
 CNOT    Q1           Q2
   SD    Q3
 CNOT    Q2           Q3
   RY    Q3   -0.7853982
 CNOT    Q2           Q3
   RY    Q3    0.7853982
    S    Q3
   TD    Q2
 CNOT    Q1           Q2
    S    Q3
 CNOT    Q2           Q3
   RY    Q3   -0.7853982
 CNOT    Q2           Q3
   RY    Q3    0.7853982
   SD    Q3
    T    Q2"""
    circ = qc.compile(prog)
    print(circ)
    mat = qc.get_circ_matrix()

if __name__ == "__main__":
    # test_symqc_matrix()
    # test_symqc_rz()
    test_toffoli_decompose()
