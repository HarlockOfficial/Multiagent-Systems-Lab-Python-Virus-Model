import logging
logging.basicConfig(level=logging.DEBUG, format='%[(asctime)s] %(filename)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
