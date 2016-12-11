"""
ML CLASSIFIER class
"""

import logging

logger = logging.getLogger("ml_classifier logger")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger.debug("Hello world!")