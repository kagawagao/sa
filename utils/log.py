import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter.datefmt = '%Y-%m-%d %H:%M:%S'
logger = logging.getLogger('sa')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
