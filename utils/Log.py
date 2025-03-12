import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

def DEBUG(log : str):
    logging.debug(log)

def INFO(log : str):
    logging.info(log)

def WARNING(log : str):
    logging.warning(log)

def ERROR(log : str):
    logging.error(log)
