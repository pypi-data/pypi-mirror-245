import datetime
import logging
import os
import shutil
from typing import Optional


def check_log_file(logs_path: str, file_name: str, size: int) -> None:
    log_file = os.path.join(logs_path, file_name)
    if not os.path.exists(log_file):
        return

    if os.path.getsize(log_file) >= size:
        mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
        mod_date = mod_date.strftime("%Y-%m-%d_%H-%M-%S")
        name = file_name.split(".")[0]
        old_log = os.path.join(logs_path, name + "_" + mod_date + ".log")

        shutil.copy2(log_file, old_log)
        # Clear contents
        open(log_file, "w").close()


def get_module_logger(
        mod_name: str,
        config: str,
        log_path: Optional[str] = "",
        log_file_name: Optional[str] = "",
        use_file_handler: bool = True,
        use_stream_handler: bool = True,
) -> logging.Logger:
    """
        To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-5s %(message)s')

    config = config.lower()
    if use_file_handler:
        if "prod" in config and not log_file_name:
            log_file_name = "logs/prod.log"
        elif "dev" in config and not log_file_name:
            log_file_name = "logs/test.log"
        else:
            raise ValueError(f"Unexpected config")

        base_path = os.path.dirname(__file__)
        if not log_path:
            log_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", log_file_name))
        check_log_file(log_path, log_file_name, size=1000000)  # Size in mb

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if use_stream_handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if "dev" in config:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger

