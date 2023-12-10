from symqc.kernel.qubit import Qsim, StateVectorSimulator, Qubit
from symqc.kernel.gate import Gate, ParametersGate
from symqc.kernel.circuit import Circuit
from symqc.kernel.gates_lib import *
from symqc.simulator import SymQC
import sympy as sp


def circuit_mat_from_file(fn):
    qc = SymQC()
    qc.compile_file(fn)
    return sp.simplify(qc.get_circ_matrix()[1]).evalf(7).rewrite(sp.exp)


def circuit_mat(prog):
    qc = SymQC()
    qc.compile(prog)
    return sp.simplify(qc.get_circ_matrix()[1]).evalf(7).rewrite(sp.exp)
