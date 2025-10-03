import logging
import auxiliary

# create logger instance with minimum of DEBUG
logger = logging.getLogger("global_logger")
logger.setLevel(logging.DEBUG)

# file handler with minimum of DEBUG level
fh = logging.FileHandler("spam.log")
fh.setLevel(logging.DEBUG)

# console handler with minimum of ERROR level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# add logging formatter to both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# adding both handlers to logger instance
logger.addHandler(fh)
logger.addHandler(ch)
