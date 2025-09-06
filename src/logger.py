import sys
from loguru import logger
from .config import config

# 默认 logger
logger.remove()
logger.add(
    sys.stderr,
    level=config['debug']['level']
)