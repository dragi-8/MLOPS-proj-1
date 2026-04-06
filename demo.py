from src.logger import logging
from src.exception import MYexception
import sys
# logging.debug('this is adebug message')
# logging.info('this is an info message')
# logging.warning('this is a warning message')
# logging.error('this is an error message')
# logging.critical('this is a critical message')

# try:
#     1+'a'
# except Exception as e:
#     logging.info(e)
#     raise MYexception(e,sys) from  e
from src.pipline.training_pipeline import Trainpipeline
pipelien=Trainpipeline()
pipelien.run_pipeline(
    
)
