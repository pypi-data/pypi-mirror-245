import logging
import os
from typing import List, Union

import numpy as np
from qiskit import QuantumCircuit, qasm3
from qiskit.qasm2 import QASM2ExportError, QASM2ParseError
from qiskit.transpiler import TranspileLayout
from qiskit.transpiler.layout import Layout

from qiskit_transpiler_service.ai.service_wrapper import AIService

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class BackendTaskError(Exception):
    def __init__(self, status: str, msg: str):
        self.status = status
        self.msg = msg


class TranspilerServiceAPI(AIService):
    """A helper class that covers some basic funcionality from the Qiskit Transpiler API"""

    def __init__(self, url: str = None, token: str = None):
        # If it does not recive URL or token, the function tries to find your Qiskit
        # token from the QISKIT_IBM_TOKEN env var
        # If it couldn't find it, it will try to get it from your ~/.qiskit/qiskit-ibm.json file
        # If it couldn't find it, it fails

        if url is None:
            url = os.environ.get(
                "QISKIT_TRANSPILER_SERVICE_URL",
                "https://cloud-transpiler-experimental.quantum-computing.ibm.com/",
            )
        super().__init__(url, token)

    def transpile(
        self,
        circuits: Union[
            Union[List[str], str], Union[List[QuantumCircuit], QuantumCircuit]
        ],
        optimization_level: int = 1,
        backend: Union[str, None] = None,
        coupling_map: Union[List[List[int]], None] = None,
        ai: bool = True,
        qiskit_transpile_options: dict = None,
        ai_layout_mode: str = None,
    ):
        if isinstance(circuits, list):
            qasm = []
            for circ in circuits:
                qasm.append(_input_to_qasm(circ))
        else:
            qasm = _input_to_qasm(circuits)

        json_args = {
            "qasm_circuits": qasm,
        }

        if qiskit_transpile_options is not None:
            json_args["qiskit_transpile_options"] = qiskit_transpile_options
        if coupling_map is not None:
            json_args["backend_coupling_map"] = coupling_map

        params = {
            "backend": backend,
            "optimization_level": optimization_level,
            "use_ai": ai,
        }

        if ai_layout_mode is not None:
            params["ai_layout_mode"] = ai_layout_mode

        transpile_resp = self.request_and_wait(
            endpoint="transpile", body=json_args, params=params
        )

        logging.info(f"transpile_resp={transpile_resp}")

        transpiled_circuits = []
        for res in transpile_resp:
            transpiled_circuits.append(_get_circuit_from_result(res, params["use_ai"]))
        return (
            transpiled_circuits
            if len(transpiled_circuits) > 1
            else transpiled_circuits[0]
        )

    def benchmark(
        self,
        circuits: Union[
            Union[List[str], str], Union[List[QuantumCircuit], QuantumCircuit]
        ],
        backend: str,
        optimization_level: int = 1,
        qiskit_transpile_options: dict = None,
    ):
        raise Exception("Not implemented")


def _input_to_qasm(input_circ: Union[QuantumCircuit, str]):
    if isinstance(input_circ, QuantumCircuit):
        try:
            qasm = input_circ.qasm().replace("\n", " ")
        except QASM2ExportError:
            qasm = qasm3.dumps(input_circ).replace("\n", " ")
    elif isinstance(input_circ, str):
        qasm = input_circ.replace("\n", " ")
    else:
        raise TypeError("Input circuits must be QuantumCircuit or qasm string.")
    return qasm


def _get_circuit_from_result(transpile_resp, use_ai):
    try:
        transpiled_circuit = QuantumCircuit.from_qasm_str(transpile_resp["qasm"])
    except QASM2ParseError:
        transpiled_circuit = qasm3.loads(transpile_resp["qasm"])

    qubits = transpiled_circuit.qubits
    init_layout = transpile_resp["layout"]["initial"]
    final_layout = transpile_resp["layout"]["final"]

    full_initial_layout = init_layout + sorted(
        set(range(len(qubits))) - set(init_layout)
    )
    full_final_layout = final_layout + list(range(len(final_layout), len(qubits)))

    if use_ai:
        full_final_layout = [
            full_final_layout[i] for i in np.argsort(full_initial_layout)
        ]

    initial_layout_qiskit = Layout(dict(zip(full_initial_layout, qubits)))
    final_layout_qiskit = Layout(dict(zip(full_final_layout, qubits)))
    input_qubit_mapping = {q: i for i, q in enumerate(qubits)}
    transpile_layout = TranspileLayout(
        initial_layout=initial_layout_qiskit,
        input_qubit_mapping=input_qubit_mapping,
        final_layout=final_layout_qiskit,
        _input_qubit_count=len(final_layout_qiskit),
        _output_qubit_list=qubits,
    )
    transpiled_circuit._layout = transpile_layout
    return transpiled_circuit
