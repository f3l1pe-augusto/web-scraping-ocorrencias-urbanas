import logging
import colorlog
import os


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

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        os.makedirs('../log', exist_ok=True)

        file_handler = logging.FileHandler('../log/news_data.log', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        self.logger = logging.getLogger()
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)


    def get_logger(self):
        return self.logger
