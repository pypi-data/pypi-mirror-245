import logging
import os
from pathlib import Path

# Create the directory for the log file
path = "/tmp/d_npu_alli"
Path(path).mkdir(exist_ok=True, parents=True)

# Configure logger
logger = logging.getLogger("d_npu_alli")
logger.setLevel(int(os.environ.get("LOG_LEVEL", logging.INFO)))

# Formatter with time in ISO format and file name, line number, and function name
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

# File handler for writing logs to a file
logFilePath = f"{path}/d_npu_alli.log"
file_handler = logging.FileHandler(filename=logFilePath, mode="a+")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Stream handler for printing logs to STDOUT
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
