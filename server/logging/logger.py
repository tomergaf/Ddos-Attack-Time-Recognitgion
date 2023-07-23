import logging
from io import StringIO


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("shared_logger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        log_file = "logs.txt"

        if log_file:
            file_handler = logging.FileHandler(log_file, mode='w')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        log_stream = StringIO()

        # Create a stream handler with the StringIO object
        stream_handler = logging.StreamHandler(log_stream)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.log_stream = log_stream

    def log(self, message, verbosity=logging.INFO):
        if verbosity == logging.DEBUG:
            self.logger.debug(message)
        elif verbosity == logging.INFO:
            self.logger.info(message)
        elif verbosity == logging.WARNING:
            self.logger.warning(message)
        elif verbosity == logging.ERROR:
            self.logger.error(message)
        elif verbosity == logging.CRITICAL:
            self.logger.critical(message)

    def get_logs(self):
        return self.log_stream.getvalue()


logger = Logger()
