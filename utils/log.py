import logging
import os

from dotenv import load_dotenv

load_dotenv()

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter.datefmt = '%Y-%m-%d %H:%M:%S'
logger = logging.getLogger('sa')
logger.setLevel(os.getenv('LOG_LEVEL', logging.INFO))
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
