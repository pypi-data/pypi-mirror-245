import sympy
from symqc.qcis.instr import QCISOpCode, QCIS_instr
from symqc.kernel.gate import Gate


sigma_x = sympy.Matrix([[0, 1], [1, 0]])
sigma_y = sympy.Matrix([[0, -sympy.I], [sympy.I, 0]])
sigma_z = sympy.Matrix([[1, 0], [0, -1]])


def R(axis, theta):
    n1 = axis[0]
    n2 = axis[1]
    n3 = axis[2]
    sigma = sigma_x * n1 + sigma_y * n2 + sigma_z * n3
    return Gate(sympy.exp(-sympy.I * theta * sigma / 2))


def X():
    return Gate(sigma_x)


def Y():
    return Gate(sigma_y)


def Z():
    return Gate(sigma_z)


def RX(theta):
    return Gate(
        sympy.Matrix(
            [
                [sympy.cos(theta / 2), -sympy.I * sympy.sin(theta / 2)],
                [-sympy.I * sympy.sin(theta / 2), sympy.cos(theta / 2)],
            ]
        )
    )


def RY(theta):
    return Gate(
        sympy.Matrix(
            [
                [sympy.cos(theta / 2), -sympy.sin(theta / 2)],
                [sympy.sin(theta / 2), sympy.cos(theta / 2)],
            ]
        )
    )


def RZ(theta):
    return Gate(
        sympy.Matrix(
            [[sympy.exp(-sympy.I * theta / 2), 0], [0, sympy.exp(sympy.I * theta / 2)]]
        )
    )


def X2P():
    return Gate(sympy.Matrix([[1, -sympy.I], [-sympy.I, 1]]) * (1 / sympy.sqrt(2)))


def X2M():
    return Gate(sympy.Matrix([[1, sympy.I], [sympy.I, 1]]) * (1 / sympy.sqrt(2)))


def Y2P():
    return Gate(sympy.Matrix([[1, -1], [1, 1]]) * (1 / sympy.sqrt(2)))


def Y2M():
    return Gate(sympy.Matrix([[1, 1], [-1, 1]]) * (1 / sympy.sqrt(2)))


def RXY(phi, theta):
    axis = sympy.Matrix([sympy.cos(phi), sympy.sin(phi), 0])
    return R(axis, theta)


def XY(phi):
    return RXY(phi, sympy.pi)


def XY2P(phi):
    return RXY(phi, sympy.pi / 2)


def XY2M(phi):
    return RXY(phi, -sympy.pi / 2)


def S():
    return Gate(sympy.Matrix([[1, 0], [0, sympy.I]]))


def SD():
    return Gate(sympy.Matrix([[1, 0], [0, -sympy.I]]))


def T():
    return Gate(sympy.Matrix([[1, 0], [0, sympy.exp(sympy.I * sympy.pi / 4)]]))


def TD():
    return Gate(sympy.Matrix([[1, 0], [0, sympy.exp(-sympy.I * sympy.pi / 4)]]))


def CZ():
    return Gate(sympy.Matrix([[1, 0], [0, -1]]), 1)


def H():
    return Gate(sympy.Matrix([[1, 1], [1, -1]]) * (1 / sympy.sqrt(2)))


def CNOT():
    """Create a CNOT gate.

    Note, when applying a CNOT gate, the qubit pair must be in the order as
    (target_qubit, ctrl_qubit). This is also in consistency with the
    convention of the entire SymQC, i.e., all control qubits comes later.
    """
    return Gate(sympy.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))
    # return Gate(sympy.Matrix([[0, 1], [1, 0]]), 1)


def Toffoli():
    """Create a Toffoli gate.

    Note, when applying a Toffoli gate, the qubit triple must be in the order as
    (target_qubit, ctrl_qubit1, ctrl_qubit2). This is also in consistency with the
    convention of the entire SymQC, i.e., all control qubits comes later.
    """

    return Gate(
        sympy.Matrix(
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
    )


def SWP():
    """Create a Swap gate."""
    return Gate(sympy.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]))


def Fredkin():
    """Create a Fredkin gate."""
    return Gate(
        sympy.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]), 1
    )


def SSWP():
    return Gate(
        sympy.Matrix(
            [
                [1, 0, 0, 0],
                [0, (1 + sympy.I) / 2, (1 - sympy.I) / 2, 0],
                [0, (1 - sympy.I) / 2, (1 + sympy.I) / 2, 0],
                [0, 0, 0, 1],
            ]
        )
    )


def ISWP():
    return Gate(
        sympy.Matrix(
            [[1, 0, 0, 0], [0, 0, sympy.I, 0], [0, sympy.I, 0, 0], [0, 0, 0, 1]]
        )
    )


def SISWP():
    return Gate(
        sympy.Matrix(
            [
                [1, 0, 0, 0],
                [0, 1 / sympy.sqrt(2), sympy.I / sympy.sqrt(2), 0],
                [0, sympy.I / sympy.sqrt(2), 1 / sympy.sqrt(2), 0],
                [0, 0, 0, 1],
            ]
        )
    )


def P(phi):
    return Gate(
        sympy.Matrix(
            [
                [1, 0],
                [0, sympy.exp(sympy.I * phi)],
            ]
        )
    )


def CP(phi):
    return Gate(
        sympy.Matrix(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, sympy.exp(sympy.I * phi)],
            ]
        )
    )


# delta_plus = 0
# delta_minus = 0
# delta_minus_off = 0


# def FSIM(*argv):
#     if len(argv) != 2:
#         raise ValueError("error argv input")

#     phi = argv[0]
#     theta = argv[1]
#     a_11 = sympy.exp(sympy.I * (delta_plus + delta_minus)) * sympy.cos(theta)
#     a_12 = (
#         -sympy.I
#         * sympy.exp(sympy.I * (delta_plus - delta_minus_off))
#         * sympy.sin(theta)
#     )
#     a_21 = sympy.exp(sympy.I * (delta_plus + delta_minus_off)) * sympy.sin(theta)
#     a_22 = sympy.exp(sympy.I * (delta_plus - delta_minus)) * sympy.cos(theta)
#     a_33 = sympy.exp(sympy.I * (2 * delta_plus - phi))
#     return Gate(
#         sympy.Matrix(
#             [1, 0, 0, 0], [0, a_11, a_12, 0], [0, a_21, a_22, 0], [0, 0, 0, a_33]
#         )
#     )


QCIS_gate = {
    QCISOpCode.X: X,
    QCISOpCode.Y: Y,
    QCISOpCode.X2P: X2P,
    QCISOpCode.X2M: X2M,
    QCISOpCode.Y2P: Y2P,
    QCISOpCode.Y2M: Y2M,
    QCISOpCode.XY: XY,
    QCISOpCode.XY2P: XY2P,
    QCISOpCode.XY2M: XY2M,
    QCISOpCode.Z: Z,
    QCISOpCode.S: S,
    QCISOpCode.SD: SD,
    QCISOpCode.T: T,
    QCISOpCode.TD: TD,
    QCISOpCode.RZ: RZ,
    QCISOpCode.CZ: CZ,
    QCISOpCode.H: H,
    QCISOpCode.RX: RX,
    QCISOpCode.RY: RY,
    QCISOpCode.RXY: RXY,
    QCISOpCode.CNOT: CNOT,
    QCISOpCode.SWP: SWP,
    QCISOpCode.SSWP: SSWP,
    QCISOpCode.ISWP: ISWP,
    QCISOpCode.SISWP: SISWP,
    QCISOpCode.CP: CP,
    QCISOpCode.Toffoli: Toffoli,
    QCISOpCode.Fredkin: Fredkin,
    # QCISOpCode.FSIM: FSIM,
}


def lib_gate(instr: QCIS_instr):
    if instr.op_code == QCISOpCode.RXY:
        return QCIS_gate[instr.op_code](instr.altitude, instr.azimuth)

    elif (
        instr.op_code == QCISOpCode.XY
        or instr.op_code == QCISOpCode.XY2P
        or instr.op_code == QCISOpCode.XY2M
        or instr.op_code == QCISOpCode.RZ
    ):
        return QCIS_gate[instr.op_code](instr.azimuth)

    elif (
        instr.op_code == QCISOpCode.RX
        or instr.op_code == QCISOpCode.RY
    ):

        return QCIS_gate[instr.op_code](instr.altitude)

    else:
        return QCIS_gate[instr.op_code]()
