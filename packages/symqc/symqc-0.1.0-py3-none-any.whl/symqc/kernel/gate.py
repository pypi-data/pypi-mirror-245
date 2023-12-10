from math import log2
from numpy import matrix
import sympy
from symqc.kernel.utils import *


class Gate:
    def __init__(self, mat, num_ctrls: int = 0):
        self.matrix = sympy.Matrix(mat)
        self._full_matrix = None

        # the size of the original matrix size (excluding the control qubits)
        self.mat_size = self.matrix.cols

        # number of target qubits corresponding to the original matrix (excluding the
        # control qubits)
        self._num_targets = int(log2(self.mat_size))

        # number of control qubits specified by the user
        self._num_controls = num_ctrls

        if self.mat_size != self.matrix.rows or self.mat_size != 2**self._num_targets:
            raise ValueError("The matrix must be square with size 2^n")
    def __str__(self):
        return str(self.matrix)

    def __mul__(self, other):
        if self._num_targets == other._num_targets:
            return Gate(self.matrix * other.matrix)
        raise ValueError("The number of target qubits must be the same.")

    @property
    def num_total_qubits(self):
        """Return the number of total qubits, including the control qubits."""
        return self._num_targets + self._num_controls

    @property
    def num_controls(self):
        """Return the number of control qubits specified by the user."""
        return self._num_controls

    @property
    def num_targets(self):
        """Return the number of target qubits corresponding to the original matrix."""
        return self._num_targets

    # def get_full_matrix(self):
    #     if self._full_matrix is not None:
    #         return self._full_matrix

    #     if self.num_controls == 0:
    #         self._full_matrix = self.matrix
    #     else:
    #         # calculate the expanded matrix here.
    #         self._full_matrix = sympy.eye(2 ** (self.num_targets + self.num_controls))

    #     self._full_matrix

    def get_matrix(self, target_qubits: list = [], ctrl_qubits: list = [], n=0):
        target_qubits = list(target_qubits)
        ctrl_qubits = list(ctrl_qubits)

        if n == 0:
            n = self._num_targets

        if self._num_controls == 0:
            if not target_qubits:
                return self.matrix
        else:
            if ctrl_qubits == [] and target_qubits == []:
                return self.matrix

        res = sympy.ones(2**n, 2**n)

        matI = sympy.eye(2)

        for p in range(n):
            if p not in target_qubits:
                mark = get_inverse_mask([p], n)
                addr = gen_subset(mark)
                for i in range(matI.rows):
                    for j in range(matI.cols):
                        for si in addr:
                            mi = map_bit(i, si, [p])
                            for sj in addr:
                                mj = map_bit(j, sj, [p])
                                res[mi, mj] = res[mi, mj] * matI[i, j]

        mark = get_inverse_mask(target_qubits, n)
        ctrl_mark = get_mask(ctrl_qubits)
        addr = gen_subset(mark)

        for i in range(self.matrix.rows):
            for j in range(self.matrix.cols):
                for si in addr:
                    mi = map_bit(i, si, target_qubits)
                    for sj in addr:
                        mj = map_bit(j, sj, target_qubits)
                        if ctrl_qubits:
                            if mi & ctrl_mark and mj & ctrl_mark:
                                res[mi, mj] = res[mi, mj] * self.matrix[i, j]
                            else:
                                res[mi, mj] = res[mi, mj] * (i == j)
                        else:
                            res[mi, mj] = res[mi, mj] * self.matrix[i, j]
        return res


# SingleQubitGate, TwoQubitGate, MultiQubitGate


class ParametersGate(Gate):
    def __init__(self, mat, ctrl=0, parameters=None):
        Gate.__init__(self, mat, ctrl)
        if parameters is None:
            parameters = []
        self.parameters = parameters

    def get_matrix(
        self,
        target_qubits: list = [],
        ctrl_qubits: list = [],
        n=0,
        parameters: list = [],
    ):
        res = Gate.get_matrix(self, target_qubits, ctrl_qubits, n)
        res = res.subs(
            [(self.parameters[i], parameters[i]) for i in range(len(parameters))]
        )
        return res
