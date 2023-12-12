"""pyscreech __init__.py"""

import sys

from loguru import logger

def setup_logger(level: int = 0):
    """Set up a loguru logger instance

    Args:
        level (int): The logging level.  Default to 0 (INFO), set to larger numbers for more logging,
                                         more negative numbers will reduce the amount of logging
    """
    logger.remove(None)
    if level > 1:
        logger.add(sys.stderr, level="TRACE")
    elif level > 0:
        logger.add(sys.stderr, level="DEBUG")
    elif level < -1:
        logger.add(sys.stderr, level="ERROR")
    elif level < 0:
        logger.add(sys.stderr, level="WARNING")
    else:
        logger.add(sys.stderr, level="INFO")

