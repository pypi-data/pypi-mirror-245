import json
import logging
import os
import time
from pathlib import Path

import backoff
import requests
from qiskit import QuantumCircuit, qasm3
from qiskit.qasm2 import QASM2ExportError
from qiskit.transpiler import TranspileLayout
from qiskit.transpiler.layout import Layout

from .service_wrapper import AIService

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class AIRoutingService(AIService):
    """A helper class that covers some basic funcionality from the AIRouting plugin"""

    def __init__(self, url: str = None, token: str = None):
        if url is None:
            url = os.environ.get(
                "ROUTINGAI_URL",
                "https://routing-ai-experimental.quantum.ibm.com/",
            ).rstrip("/")

        super().__init__(url, token)

    def routing(
        self,
        circuit: QuantumCircuit,
        optimization_level: int = 1,
        check_result: bool = False,
        layout_mode: str = "OPTIMIZE",
        coupling_map: str = "ibm_sherbrooke",
    ):
        is_qasm3 = False
        try:
            qasm = circuit.qasm()
        except QASM2ExportError:
            qasm = qasm3.dumps(circuit)
            is_qasm3 = True

        json_args = {"qasm": qasm.replace("\n", " "), "coupling_map": coupling_map}

        params = {
            "check_result": check_result,
            "layout_mode": layout_mode,
            "optimization_level": optimization_level,
        }

        routing_resp = self.request_and_wait(
            endpoint="routing", body=json_args, params=params
        )

        if routing_resp.get("success"):
            routed_circuit = (
                qasm3.loads(routing_resp["qasm"])
                if is_qasm3
                else QuantumCircuit.from_qasm_str(routing_resp["qasm"])
            )
            # qubits = routed_circuit.qubits + routed_circuit.ancillas
            # final_layout_qiskit = Layout(
            #     # {q: i for i, q in enumerate(routing_resp["layout"]["final"])}
            #     dict(zip(routing_resp["layout"]["final"], qubits))
            # )
            # input_qubit_mapping = {q: i for i, q in enumerate(qubits)}
            # initial_layout_qiskit = Layout(
            #     dict(zip(routing_resp["layout"]["initial"], qubits))
            # )

            # routed_circuit._layout = TranspileLayout(
            #     initial_layout=initial_layout_qiskit,
            #     input_qubit_mapping=input_qubit_mapping,
            #     final_layout=final_layout_qiskit,
            #     _input_qubit_count=len(routing_resp["layout"]["final"]),
            #     _output_qubit_list=qubits,
            # )

            # logging.info(f"Initial: {routed_circuit.layout.initial_index_layout()}")
            # logging.info(f"Final: {routed_circuit.layout.final_index_layout()}")
            return (
                routed_circuit,
                routing_resp["layout"]["initial"],
                routing_resp["layout"]["final"],
            )

    def benchmark(
        self,
        circuit: QuantumCircuit,
        coupling_map: list[list[int]] = None,
        model: str = None,
        backend: str = None,
        topology: str = None,
        n_steps: int = None,
        keep_layout: bool = True,
    ):
        is_qasm3 = False
        try:
            qasm = circuit.qasm()
        except QASM2ExportError:
            qasm = qasm3.dumps(circuit)
            is_qasm3 = True

        json_args = {
            "qasm": qasm.replace("\n", " "),
        }

        params = {
            "keep_layout": keep_layout,
        }

        if coupling_map is not None:
            json_args["coupling_map"] = coupling_map

        params = {"keep_layout": keep_layout}

        if model is not None:
            params["model"] = model
        if backend is not None:
            params["backend"] = backend
        if topology is not None:
            params["topology"] = topology
        if n_steps is not None:
            params["n_steps"] = n_steps

        benchmark_resp = self.request_and_wait(
            endpoint="benchmark", body=json_args, params=params
        )

        if benchmark_resp.get("success"):
            routed_circuit = (
                qasm3.loads(benchmark_resp["qasm"])
                if is_qasm3
                else QuantumCircuit.from_qasm_str(benchmark_resp["qasm"])
            )
            layout = benchmark_resp["final_layout"]
            return routed_circuit, layout
