import os
from datetime import datetime
import logging
import sys
import getpass
import config
import logstash

if not os.path.isdir(config.LOG_DIRECTORY_PATH):
    os.makedirs(config.LOG_DIRECTORY_PATH)


log_filename = datetime.strftime(datetime.now(), '%d-%m-%Y') + '_ground_truth.log'
logger = logging.getLogger('application')  # Creating an object
logger.setLevel(logging.DEBUG)  # Setting the threshold of logger to DEBUG
formatter = logging.Formatter(
    '%(asctime)s : %(module)s: %(lineno)d : %(levelname)s : %(message)s')

# file handler to see logs in file
fh = logging.FileHandler(filename=os.path.join(config.LOG_DIRECTORY_PATH, log_filename))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# system handler to logs in console
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)

#TCP handler to write logs in logstash
sh = logstash.TCPLogstashHandler(config.LOGSTASH_IP,config.LOGSTASH_PORT,tags=['ground-truth'])
logger.addHandler(sh)
