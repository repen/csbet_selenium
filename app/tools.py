from Globals import WORK_DIR
import logging, hashlib

def hash_(string):
    return hashlib.sha1(string.encode()).hexdigest()

def log(*args):
    name_logger = args[0]
    path_file   = args[1]
    # создаём logger
    logger = logging.getLogger(name_logger)
    logger.setLevel(logging.DEBUG)

    # создаём консольный handler и задаём уровень
    # ch = logging.StreamHandler()
    ch = logging.FileHandler(WORK_DIR + path_file)

    ch.setLevel(logging.DEBUG)

    # создаём formatter
    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    # %(lineno)d :
    # добавляем formatter в ch
    ch.setFormatter(formatter)

    # добавляем ch к logger
    logger.addHandler(ch)

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    return logger