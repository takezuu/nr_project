import logging


class Logger:

    def __init__(self):
        self.logger = logging.getLogger("app")
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, filename='app_log/app.log', level=logging.DEBUG, encoding="UTF-8")


