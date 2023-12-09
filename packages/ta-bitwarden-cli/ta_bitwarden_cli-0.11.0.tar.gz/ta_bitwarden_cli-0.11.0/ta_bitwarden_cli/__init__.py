"""Top-level package for ta-bitwarden-cli."""
import os
import sys
import logging
import requests

from datetime import datetime

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "__version__ = '0.11.0'"


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)
        try:
            response = requests.get("https://api.ipify.org?format=json")
            data = response.json()
            self.host_ip = data["ip"]
        except Exception:
            self.host_ip = "0.0.0.0"

    def format(self, record):
        record.host_ip = self.host_ip
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        tzinfo = ct.astimezone().tzinfo
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
        tz = tzinfo.tzname(None) or tzinfo.zone
        return f"{s} {tz}"


log_level = logging.DEBUG
logger = logging.getLogger("ta-bitwarden-cli")
if logger.hasHandlers():
    logger.handlers = []
logger.setLevel(log_level)
logger.propagate = False

format = "[%(asctime)s] %(host_ip)-12s %(levelname)-6s %(name)-12s %(message)s"
log_format = CustomFormatter(format)

if os.path.exists("output"):
    logs_path = "output/ta-bitwarden-cli.log"
else:
    logs_path = "ta-bitwarden-cli.log"
handler = logging.FileHandler(logs_path)
handler.setLevel(logging.DEBUG)
handler.addFilter(lambda record: record.levelno in {logging.DEBUG, logging.ERROR})
handler.setFormatter(log_format)
logger.addHandler(handler)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_format)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
