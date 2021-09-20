import logging as LOG
from datetime import datetime
from os.path import join, normpath

logs = normpath('logs')

log_file = f'TrueLayer_{datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")}.log'
# setting LOG configurations
# NOTE: Add filemode = 'w' if you want to overwrite the file at every run 
LOG.basicConfig(level=LOG.DEBUG, filename=join(logs, log_file), 
                format='%(asctime)s - %(levelname)s - %(message)s', 
                datefmt='%d-%b-%y %H:%M:%S')
