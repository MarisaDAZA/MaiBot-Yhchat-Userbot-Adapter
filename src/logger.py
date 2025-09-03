import logging
from .config import config

logger = logging.getLogger('yhchat')
logger.setLevel(level=config['debug']['level'])