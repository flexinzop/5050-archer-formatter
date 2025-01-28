import logging

def init_logger():
    # Create the logger
    logger = logging.getLogger('archer_formatter')
    logger.setLevel(logging.DEBUG)

    # Create the file handler
    file_handler = logging.FileHandler('archer_formatter.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Create the logging format

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    
    return logger