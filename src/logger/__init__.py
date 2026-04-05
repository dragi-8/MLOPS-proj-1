import logging
from logging.handlers import RotatingFileHandler
#import datetime
import os
from datetime import datetime

from from_root import from_root

LOG_DIR='logs'
LOG_FILE=f'{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}.log'
max_bytes=5*1024*1024
backup_count=3

log_dir_path=os.path.join(from_root(),LOG_DIR)
os.makedirs(log_dir_path,exist_ok=True)
log_file=os.path.join(log_dir_path,LOG_FILE)

def configuire_log():
    logger=logging.getLogger('vehicle_logger')
    logger.setLevel(logging.DEBUG)

    formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler=RotatingFileHandler(log_file,maxBytes=max_bytes,backupCount=backup_count)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

configuire_log()



