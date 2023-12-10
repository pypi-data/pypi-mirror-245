import logging

# Define the format for the logger
FORMATTER = '%(asctime)s - %(funcName)s - %(filename)s - %(levelname)s - %(message)s'

def get_logger(logger_name):
    """
    Configures and returns a logger with the given name.

    Args:
        logger_name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger object.
    """
    # Get the logger with the specified name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Check if the logger already has handlers configured
    if not logger.handlers:
        # Configure logging basics with the defined format
        logging.basicConfig(format=FORMATTER, level=logging.DEBUG)

    return logger
