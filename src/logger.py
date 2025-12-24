import os
import logging
import datetime

today = datetime.datetime.now().strftime("%Y-%m-%d")

# Setting up the logging configuration
log_file = f'logs\cryptor_{today}.log'
log_dir = os.path.dirname(log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


class SingletonLogger:
    _instance = None

    @staticmethod
    def get_instance(log_name, log_file="app.log", log_level=logging.DEBUG, file_log_level=logging.DEBUG, stream_log_level=logging.INFO):
        """
        Static method to retrieve the singleton instance of the logger.
        
        Parameters:
        - log_file (str): The name of the log file. Defaults to 'app.log'.
        - log_level (int): The logging level for the logger. Defaults to logging.DEBUG.
        - file_log_level (int): The logging level for the file handler. Defaults to logging.DEBUG.
        - stream_log_level (int): The logging level for the stream handler. Defaults to logging.INFO.
        
        Returns:
        - logger (logging.Logger): Configured logger.
        """
        if SingletonLogger._instance is None:
            SingletonLogger._instance = SingletonLogger(log_name, log_file, log_level, file_log_level, stream_log_level)
        return SingletonLogger._instance.logger

    def __init__(self, log_name, log_file="app.log", log_level=logging.DEBUG, file_log_level=logging.DEBUG, stream_log_level=logging.INFO):
        if SingletonLogger._instance is not None:
            raise Exception("Logger instance already created. Use get_instance() to get the singleton logger.")

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        # Create a formatter for log messages
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # File handler with log rotation (if required)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(formatter)

        # Stream handler for console logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_log_level)
        stream_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
# Usage of SingletonLogger
def logger(log_name, log_file=log_file, log_level=logging.DEBUG, file_log_level=logging.DEBUG, stream_log_level=logging.INFO):
    return SingletonLogger.get_instance(log_name, log_file, log_level, file_log_level, stream_log_level)
