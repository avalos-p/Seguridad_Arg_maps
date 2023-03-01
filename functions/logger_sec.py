import logging

def logger_project(log_name):

    # Creating logger for current session
    logger = logging.getLogger(log_name)

    # Setting lvl to INFO
    logger.setLevel(logging.DEBUG)



    # Adding format to logger
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')


    # Creating handler
    handler_consola = logging.StreamHandler()
    handler_consola.setLevel(logging.DEBUG)
    handler_consola.setFormatter(formatter)


    # Adding Handler
    logger.addHandler(handler_consola)
    print("done")
    return logger       