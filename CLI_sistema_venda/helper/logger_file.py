import logging
import sys
from colorama import init, Fore, Style

init(autoreset=True, strip=False)

class ColorLogFormatter(logging.Formatter):
    COLOR_MAP = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLOR_MAP.get(record.levelno, "")
        level = record.levelname.upper().center(10)
        msg = super().format(record)
        base = f"{color}[{level}]{Style.RESET_ALL}"
        return f"{base} › {msg}"

def get_logger(name="logger"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColorLogFormatter('%(message)s'))
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

logger = get_logger()