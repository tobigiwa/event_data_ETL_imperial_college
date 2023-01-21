from typing import Union

def creating_log(script_name: str, log_folder_path: Union[str, None] = None):

    """ 
    Implements the logging and returns the logger object. 
    Takes a string positional parameter for log file name and a keyword parameter for log file path. 
    Default log file path folder 'log_folder' and each code run rewrites the last log.
    """
    import logging, os

    if not log_folder_path:
        log_folder_path: str = 'log_folder'

    if os.path.exists(log_folder_path):
        pass
    else:
        os.makedirs(log_folder_path)

    log_path = os.path.join(os.getcwd(), log_folder_path, f'{script_name}.log')

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)
    log_handler = logging.FileHandler(log_path)
    log_format = logging.Formatter(
        '\n %(asctime)s -- %(name)s -- %(levelname)s -- %(message)s \n')
    log_handler.setFormatter(log_format)
    logger.addHandler(log_handler)
    logger.info('Log reporting is instantiated.')

    return logger