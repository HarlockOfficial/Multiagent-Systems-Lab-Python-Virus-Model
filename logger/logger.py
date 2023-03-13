import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('')
logger.setLevel(logging.NOTSET)


def log(msg, level=logger.info):
    level(msg)
    with open('log.txt', 'a') as f:
        f.write(msg + '\n')
