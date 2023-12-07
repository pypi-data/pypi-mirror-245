import os
import platform
import shutil
import sys
import logging
from typing import List

from dotenv import load_dotenv

from cast_ai.se.constants import (LINUX_GET_DEPLOYMENTS_CMD, SECRETS_ENV_FILE, LINUX_GET_NONZERO_DEPLOYMENTS_CMD, WIN_GET_NONZERO_DEPLOYMENTS_CMD,
                                  WIN_GET_DEPLOYMENTS_CMD, REQUIRED_TOOLS)
from cast_ai.se.services.logging_svc import setup_logging


def get_get_deployments_command(kill_deployments: bool = False, log_level: str = "INFO") -> str:
    os_system = platform.system()
    logger = setup_logging(__name__, log_level)
    if os_system == "Windows":
        logger.debug("Running on Windows...")
        if kill_deployments:
            return WIN_GET_NONZERO_DEPLOYMENTS_CMD
        return WIN_GET_DEPLOYMENTS_CMD

    elif os_system == "Linux":
        logger.debug("Running on Linux...")
        if kill_deployments:
            return LINUX_GET_NONZERO_DEPLOYMENTS_CMD
        return LINUX_GET_DEPLOYMENTS_CMD
    else:
        logger.debug(f"Unsupported OS={os_system}")
        raise RuntimeError(f"Unsupported OS={os_system}")


def init(input_value: List[str], log_level: str = "INFO") -> None:
    logger = setup_logging(__name__, log_level)
    input_validate(input_value)
    load_dotenv(dotenv_path=SECRETS_ENV_FILE)
    logger.info(f"{'=' * 200}")
    logger.info(f"Starting executing SE CLI Command Sequencer with the following inputs: {input_value}")
    logger.debug(f"{get_system_info()}")


def valid_local_env(log_level: str = "INFO"):
    logger = logger = setup_logging(__name__, log_level)
    for tool in REQUIRED_TOOLS:
        validate_tool_exists(logger, tool)


def validate_tool_exists(logger, tool: str) -> None:
    if not shutil.which(tool):
        logger.critical(f"{tool} was not found (possibly not in PATH)")
        raise RuntimeError(f"{tool} was not found (possibly not in PATH)")


def input_validate(input_value: List[str]) -> None:
    if len(input_value) != 2 or input_value[1] not in ["on", "off"]:
        print("Invalid option. Use only 'on' or 'off'.")
        sys.exit(1)


def get_system_info():
    return {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
    }


def get_environment_variable(variable_name: str) -> str:
    value = os.getenv(variable_name)
    if not value:
        logging.critical(f"Environment variable {variable_name} is not set or empty.")
        raise RuntimeError(f"Environment variable {variable_name} is not set or empty.")
    return value
