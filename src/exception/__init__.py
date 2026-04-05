import sys
import logging
from src.logger import logging as custom_logger

def configure_error_message(error:Exception,error_detail:sys):
    """
    it returns a more better error message for easy debugging
    """

    _,_,exc_tb=error_detail.exc_info()

    file_name=exc_tb.tb_frame.f_code.co_filename

    line_number = exc_tb.tb_lineno

    error_message=f'error occured in {file_name} at {line_number}:{str(error)}'

    custom_logger.error(error_message)
    return error_message

class MYexception(Exception):
    """
        it returns a more better error message for easy debugging

    
    """
     
    def __init__(self,error_message:str,error_detail:sys):

        super().__init__(error_message)
        self.error_message=configure_error_message(error_message,error_detail)

        

    def __str__(self):
        return self.error_message
       