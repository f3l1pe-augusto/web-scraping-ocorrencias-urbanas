import logging
import colorlog

class LoggerConfig:
    def __init__(self):
        log_colors = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            log_colors=log_colors
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        return self.logger
