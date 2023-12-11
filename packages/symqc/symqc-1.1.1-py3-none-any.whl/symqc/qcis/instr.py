from enum import Enum, auto


class QCISOpCode(Enum):
    # The first single-qubit operation
    RZ = auto()
    XYARB = auto()
    XY = auto()
    XY2P = auto()
    XY2M = auto()
    X = auto()
    X2P = auto()
    X2M = auto()
    Y = auto()
    Y2P = auto()
    Y2M = auto()
    Z = auto()
    Z2P = auto()
    Z2M = auto()
    Z4P = auto()
    Z4M = auto()
    S = auto()
    SD = auto()
    T = auto()
    TD = auto()
    H = auto()
    RX = auto()
    RY = auto()
    RXY = auto()
    # The last single-qubit operation

    # The first two-qubit operation
    CZ = auto()
    CNOT = auto()
    SWP = auto()
    SSWP = auto()
    ISWP = auto()
    SISWP = auto()
    CP = auto()
    FSIM = auto()
    # The last two-qubit operation

    # The first three-qubit operation
    Toffoli = auto()
    Fredkin = auto()
    # the last three-qubit operation

    # The first measurement operation
    MEASURE = auto()
    M = auto()
    # The last measurement operation

    B = auto()

    def is_single_qubit_op(self):
        return self.RZ.value <= self.value <= self.RXY.value

    def is_two_qubit_op(self):
        return self.CZ.value <= self.value <= self.FSIM.value

    def is_three_qubit_op(self):
        return self.Toffoli.value <= self.value <= self.Fredkin.value

    def is_measure_op(self):
        return self.MEASURE.value <= self.value <= self.M.value


class QCIS_instr(object):
    def __init__(self, op_code, **kwargs):
        """
        Data structure for representing QCIS instructions.

        Attributes:
            op_code: The operation code of the QCIS instruction.
            azimuth: The angle between the axis to rotate along and z-axis.
            altitude: The angle of rotation along a given axis.

        Single-qubit operation only attributes:
            qubit: The name string of target qubit.

        Two-qubit operation only attributes:
            control_qubit: The name string of control qubit.
            target_qubit: The name string of target qubit.

        Measurement operation only attributes:
            qubits_list: The names of all qubits to be measured.
        """
        self.op_code = op_code

        if op_code.is_two_qubit_op():
            if self.op_code == QCISOpCode.CP or self.op_code == QCISOpCode.FSIM:
                self.azimuth = kwargs["azimuth"]
            self.control_qubit = kwargs["control_qubit"]
            self.target_qubit = kwargs["target_qubit"]
            return

        if op_code.is_single_qubit_op():
            self.qubit = kwargs["qubit"]

            if self.op_code == QCISOpCode.XYARB or self.op_code == QCISOpCode.RXY:
                self.azimuth = kwargs["azimuth"]
                self.altitude = kwargs["altitude"]
                return

            if (
                self.op_code == QCISOpCode.XY
                or self.op_code == QCISOpCode.XY2P
                or self.op_code == QCISOpCode.XY2M
                or self.op_code == QCISOpCode.RZ
            ):
                self.azimuth = kwargs["azimuth"]
                return

            if self.op_code == QCISOpCode.RX or self.op_code == QCISOpCode.RY:
                self.altitude = kwargs["altitude"]
                return

            return

        if op_code.is_three_qubit_op():
            if op_code == QCISOpCode.Toffoli:
                self.control_qubit1 = kwargs["control_qubit1"]
                self.control_qubit2 = kwargs["control_qubit2"]
                self.target_qubit = kwargs["target_qubit"]
                return

            if op_code == QCISOpCode.Fredkin:
                self.control_qubit = kwargs["control_qubit"]
                self.target_qubit1 = kwargs["target_qubit1"]
                self.target_qubit2 = kwargs["target_qubit2"]
                return

            raise ValueError(
                "Unrecognized three-qubiut instruction: {}.".format(op_code)
            )

        if op_code.is_measure_op():
            # Should be a list even measuring only one qubit
            self.qubits_list = kwargs["qubits_list"]
            self.qubits_list.sort()
            return

        if op_code == QCISOpCode.B:
            self.qubits_list = kwargs["qubits_list"]
            self.qubits_list.sort()
            return

        raise ValueError("Found unrecognized opcode: ", op_code)

    def _qasm(self):
        opcode_str = str(self.op_code).split(".")[1]
        if self.op_code.is_two_qubit_op():
            return "{:10s} {:5s} {:5s}".format(
                opcode_str, self.control_qubit, self.target_qubit
            )

        if self.op_code.is_single_qubit_op():
            params_str = ""
            if self.op_code == QCISOpCode.XYARB:
                params_str = " {}  {}".format(self.azimuth, self.altitude)
            return "{} {}{}".format(opcode_str, self.qubit, params_str)

        if self.op_code.is_measure_op():
            qubits_list_str = " ".join([qubit for qubit in self.qubits_list])
            return "M {}".format(qubits_list_str)

        raise ValueError("Unrecognized instruction.")

    def __str__(self):
        if self.op_code.is_three_qubit_op():
            if self.op_code == QCISOpCode.Toffoli:
                return "Toffoli controls: [{} {}], target: {}".format(
                    self.control_qubit1, self.control_qubit2, self.target_qubit
                )

            if self.op_code == QCISOpCode.Fredkin:
                return "Fredkin control: {}, targets: [{} {}]".format(
                    self.control_qubit, self.target_qubit1, self.target_qubit2
                )

        if self.op_code.is_two_qubit_op():
            return "Two-qubit op: {}, control: {}, target: {}".format(
                self.op_code, self.control_qubit, self.target_qubit
            )

        if self.op_code.is_single_qubit_op():
            params_str = ""
            if self.op_code == QCISOpCode.XYARB:
                params_str = ", azimuth: {}, altitude: {}".format(
                    self.azimuth, self.altitude
                )
            return "Single-qubit op: {}, qubit: {}{}".format(
                self.op_code, self.qubit, params_str
            )

        if self.op_code.is_measure_op():
            qubits_list_str = " ".join([qubit for qubit in self.qubits_list])
            return "Measure op: {}, qubits list: {}".format(
                self.op_code, qubits_list_str
            )

        raise ValueError("Unrecognized instruction.")

    def __eq__(self, other):
        # Two QCISInst instances with same values of attributes will be identical
        return self.__dict__ == other.__dict__
