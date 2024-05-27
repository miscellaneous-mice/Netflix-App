import logging

# Setting our Logger name
logger = logging.getLogger(__name__)
# Setting our Logger logging-level to DEBUG
logger.setLevel(logging.DEBUG)

# Formatter for our logging details
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# File handler to register the logs to 'sample.log'
file_handler = logging.FileHandler('logs/import.log')
# Setting formatter for our logs written to 'sample.log'
file_handler.setFormatter(formatter)

# To incorporate file_handler logging-level ("Error") to 'sample.log' and 'console' and logger logging-level ("Debug") to 'console'
stream_handler = logging.StreamHandler()
# Setting the formatter for file_handler logging-level ("Error") and logger logging-level ("Debug") to 'console'
stream_handler.setFormatter(formatter)

# Setting our Logger to write logs to our file handler
logger.addHandler(file_handler)
# Incorporating our logger and file_handler logging-levels to our logger.
logger.addHandler(stream_handler)