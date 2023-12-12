import inspect
import logging
import re
from enum import Enum
from time import sleep

import requests

logger = logging.getLogger("d_npu_alli")


class Model(Enum):
    TENSORFLOW = "tensorflow"
    TORCH = "pytorch"


def run_federated_learning(server_address="http://localhost:8000", **kwargs):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno

    lines, _ = inspect.getsourcelines(caller_frame)
    call_start = line_number - 1
    call_end = call_start
    while call_end < len(lines) and not lines[call_end].strip().endswith(")"):
        call_end += 1
    caller_lines = "".join(lines[call_start : call_end + 1])

    variables = _parse_variables(caller_lines)
    model = kwargs["model"]
    framework = _get_framework_name(model).value

    response = requests.post(
        f"{server_address}/api/v1/federated-learning/tasks",
        json={
            **variables,
            "user_app": "\n".join(lines),
            "framework": framework,
        },
    )
    task_name = response.json()
    some_running = False
    while not some_running:
        response = requests.get(
            f"{server_address}/api/v1/federated-learning/tasks/{task_name}"
        )
        task_status = response.json()
        logger.info(task_status)
        pod_status = task_status.get("pod")
        some_running = pod_status and any(
            status == "Running" or status == "Succeeded"
            for status in pod_status.values()
        )
        sleep(2)
    for _ in range(10):
        print(". ", end="")
        sleep(1)
    with requests.get(
        f"{server_address}/api/v1/federated-learning/tasks/{task_name}/log",
        stream=True,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                logger.info(decoded_line)


def _get_framework_name(model: type):
    module = model.__class__.__bases__[0].__module__
    if "keras" in module:
        return Model.TENSORFLOW
    elif "torch" in module:
        return Model.TORCH
    else:
        raise NotImplementedError(f"{module} is not yet implemented!")


def _parse_variables(text):
    pattern = r"\b(\w+)\s*=\s*([\w\d_]+)"

    matches = re.findall(pattern, text)

    if not matches:
        raise ValueError("Failed to parse variable names!")

    return {k: v for k, v in matches}
