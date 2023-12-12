import json
import logging
import os
import time
from http import HTTPStatus
from pathlib import Path

import backoff
import requests
from qiskit.transpiler.exceptions import TranspilerError

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class BackendTaskError(Exception):
    def __init__(self, status: str, msg: str):
        self.status = status
        self.msg = msg


def _get_token_from_system():
    token = os.environ.get("QISKIT_IBM_TOKEN")

    if not token:
        with open(Path.home() / ".qiskit" / "qiskit-ibm.json", "r") as _sc:
            creds = json.loads(_sc.read())
        token = creds.get("default-ibm-quantum", {}).get("token")
        if token is None:
            logging.warning("The token is undefined")
    return token


class AIService:
    """A helper class that covers some common basic funcionality AIServices"""

    def __init__(self, url: str = None, token: str = None):
        # If it does not recive URL or token, the function tries to find your Qiskit
        # token from the QISKIT_IBM_TOKEN env var
        # If it couldn't find it, it will try to get it from your ~/.qiskit/qiskit-ibm.json file
        # If it couldn't find it, it fails

        self.url = url.rstrip("/")

        token = token if token else _get_token_from_system()

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get_versions(self):
        url = f"{self.url}/version"
        resp = requests.get(
            url,
            headers=self.headers,
        ).json()

        return resp

    def get_supported_backends(self):
        url = f"{self.url}/backends"
        resp = requests.get(
            url,
            headers=self.headers,
        ).json()

        return resp

    @backoff.on_predicate(
        backoff.constant,
        lambda res: res.get("state") not in ["SUCCESS", "FAILURE"],
        jitter=None,
        interval=1,  # TODO: Define by config or circuit?
        max_time=120,  # TODO: Define by config or circuit?
    )
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.JSONDecodeError,
        ),
        max_time=120,  # TODO: Define by config or circuit?
    )
    def request_status(self, endpoint, task_id):
        logging.info(f"Getting status of task {task_id} ...")
        res = requests.get(url=f"{self.url}/{endpoint}/{task_id}", headers=self.headers)
        res.raise_for_status()
        return res.json()

    def request_and_wait(self, endpoint: str, body: dict, params: dict):
        try:
            return self._request_and_wait(endpoint, body, params)
        except requests.exceptions.HTTPError as exc:
            _raise_transpiler_error_and_log(_get_error_msg_from_response(exc))
        except BackendTaskError:
            # TODO: Do we want to give the user the internal error: "The background task df86e449-8bb5-43fb-92a9-c23818ee8ce7 FAILED"
            _raise_transpiler_error_and_log("Service error.")
        except Exception as exc:
            _raise_transpiler_error_and_log(f"Error: {exc}")

    def _request_and_wait(self, endpoint: str, body: dict, params: dict):
        resp = requests.post(
            f"{self.url}/{endpoint}",
            headers=self.headers,
            json=body,
            params=params,
        )
        resp.raise_for_status()
        resp = resp.json()
        task_id = resp.get("task_id")

        result = BackendTaskError(
            status="PENDING", msg=f"The background task {task_id} timed out"
        )

        resp = self.request_status(endpoint, task_id)
        if resp.get("state") == "SUCCESS":
            result = resp.get("result")
        elif resp.get("state") == "FAILURE":
            logging.error("The request FAILED")
            result = BackendTaskError(
                status="FAILURE", msg=f"The background task {task_id} FAILED"
            )

        if isinstance(result, BackendTaskError):
            # TODO: Shall we show this  "The background task 99cf52d2-3942-4ae5-b2a7-d672af7f1216 FAILED" to the user?
            logging.error(f"Failed to get a result for {endpoint}: {result.msg}")
            raise result
        else:
            return result


def _raise_transpiler_error_and_log(msg: str):
    logging.error(msg)
    raise TranspilerError(msg)


def _get_error_msg_from_response(exc: requests.exceptions.HTTPError):
    if exc.response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value:
        # Default message
        msg = "Internal error."
        resp = exc.response.json()
        if detail := resp.get("detail"):
            if isinstance(detail, str):
                msg = detail
            elif isinstance(detail, list):
                # Try to get err msg from
                # raw validation error
                if "input" in resp["detail"][0] and "msg" in resp["detail"][0]:
                    msg = f"Wrong input '{resp['detail'][0]['input']}'. {resp['detail'][0]['msg']}"
    else:
        msg = f"Service error: {str(exc)}"
    return msg
