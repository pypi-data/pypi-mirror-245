from tequila import *
from pyqcisim.QCIS_inst import QCISOpCode
import numpy as np

SINGLE_QUBIT_CODE_TENSOR_DICT = {
    QCISOpCode.RX: lambda inst: [
        np.cos(inst.altitude / 2),
        -1j * np.sin(inst.altitude / 2),
        -1j * np.sin(inst.altitude / 2),
        np.cos(inst.altitude / 2),
    ],
    QCISOpCode.RY: lambda inst: [
        np.cos(inst.altitude / 2),
        -np.sin(inst.altitude / 2),
        np.sin(inst.altitude / 2),
        np.cos(inst.altitude / 2),
    ],
    QCISOpCode.RZ: lambda inst: [1, 0, 0, np.exp(1j * inst.azimuth)],
    QCISOpCode.H: lambda inst: TENSOR_BASE_GATE_H,
    QCISOpCode.S: lambda inst: TENSOR_BASE_GATE_S,
    QCISOpCode.SD: lambda inst: [1, 0, 0, -1j],
    QCISOpCode.T: lambda inst: TENSOR_BASE_GATE_T,
    QCISOpCode.TD: lambda inst: [1, 0, 0, np.exp(-1j * np.pi / 4)],
    QCISOpCode.X: lambda inst: TENSOR_BASE_GATE_X,
    QCISOpCode.Z: lambda inst: TENSOR_BASE_GATE_Z,
    QCISOpCode.X2P: lambda inst: [i / (2**0.5) for i in [1, -1j, -1j, 1]],
}

TWO_QUBIT_CODE_TENSOR_DICT = {
    QCISOpCode.CNOT: TENSOR_BASE_GATE_CX,
}


class CircuitExecutorTequila:
    def __init__(self, names):
        self._names = names

        # build <qubit_name, qubit_number> map
        self._qubit_name_number_dict = dict()
        for i, name in enumerate(self._names):
            self._qubit_name_number_dict[name] = i

    def reset(self):
        pass

    def execute(self, instructions, num_shots):
        # prepare qubits
        q = qubit(len(self._names))

        msmt_qubits = []

        # apply gates
        for inst in instructions:
            if inst.op_code.is_single_qubit_op():
                gate_tensor = SINGLE_QUBIT_CODE_TENSOR_DICT[inst.op_code](inst)
                _gate = gate(1)
                _gate.mat2mpo(gate_tensor)
                q.apply_1(self._qubit_name_number_dict[inst.qubit], _gate)

            if inst.op_code.is_two_qubit_op():
                gate_tensor = TWO_QUBIT_CODE_TENSOR_DICT[inst.op_code]
                _gate = gate(2)
                _gate.mat2mpo(gate_tensor)

                q.apply_2(
                    self._qubit_name_number_dict[inst.control_qubit],
                    self._qubit_name_number_dict[inst.target_qubit],
                    _gate,
                )

            if inst.op_code.is_measure_op():
                msmt_qubits.extend(
                    list(
                        map(lambda q: self._qubit_name_number_dict[q], inst.qubits_list)
                    )
                )
        num_msmt_qubits = len(msmt_qubits)
        msmt_qubit_names = list(map(lambda q: self._names[q], msmt_qubits))
        msmts = []
        for i in range(num_shots):
            """meas_rej returns result in a dict format: {'11000': 2, '00100': 3}"""
            bit_str_res = list(q.meas_rej(msmt_qubits, 1).keys())[0]
            res = [int(bit_str_res[i], 2) for i in range(num_msmt_qubits)]
            msmts.append(res)
        return (msmt_qubit_names, msmts)
