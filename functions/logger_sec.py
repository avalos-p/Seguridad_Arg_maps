import logging

def logger_sec_project(log_name):

    # Creating logger for current session
    logger = logging.getLogger(log_name)
    handler_consola = logging.StreamHandler()

    # Adding Handler
    logger.addHandler(handler_consola)

    # Adding format to logger
    # Setting lvl to Debug
    format = logging.Formatter(
        fmt='%(asctime)s - nombre_logger - %(message)s',
        datefmt ='%d-%m-%Y')

    handler_consola.setFormatter(format)

    return logger        