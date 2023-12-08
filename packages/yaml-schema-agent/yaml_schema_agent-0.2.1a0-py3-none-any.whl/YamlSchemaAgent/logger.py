import logging
from datetime import datetime
from pathlib import Path


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;5;15m"
    yellow = "\x1b[38;5;11m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[38;5;196m"
    reset = "\x1b[0m"
    turquoise = '\x1b[38;5;14m'
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: turquoise + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(verbose=False, simple_report=False, report_location='logs'):
    logger = logging.getLogger("YamlSchemaAgent")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    Path(report_location).mkdir(parents=True, exist_ok=True)
    log_file = datetime.now().strftime('log_%m-%Y-%d_%H-%M-%S.log')
    logger.info(f'Writing logs to {report_location}/{log_file}.log')
    fh = logging.FileHandler(f'{report_location}/{log_file}.log')
    fh.setLevel(logging.DEBUG)

    if not logger.handlers:
        if not verbose:
            ch.setLevel(logging.INFO)
        if simple_report:
            fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger
