import os
import uuid
import traceback
import logging
from typing import Optional
from enum import Enum

class StatusCodes(Enum):
    """ This class is used to define the status code of the request """
    TECHNICAL_EXCEPTION = "TECHNICAL_EXCEPTION"

class StatusMessages(Enum):
    """ This class is used to define the status code of the request """
    ENV_VARIABLE_NOT_FOUND = "The environment variable '{variable_name}' is not found."
    RECORDS_NOT_FOUND = "No Records Found"

########################
### BASE EXCEPTION
########################

class CustomExceptionHandler(Exception):
    """Base exception class for GPT-related exceptions"""
    
    # Set default base componenet code as class instance, shared among all class instances amd objects
    error_source = 'ACMP'
    
    def __init__(self, error_message: str,
                 error_code: Optional[str] = StatusCodes.TECHNICAL_EXCEPTION.value,
                 actual_exception: Optional[Exception] = None,
                 **kwargs):
        # Set Exception variables, users can pass as many kwargs as needed
        self.__dict__.update({**kwargs, **{"error_code":error_code}})
        if actual_exception is not None:
            self.actual_exception_trace = list(traceback.TracebackException.from_exception(actual_exception).format())
            self.actual_exception = str(actual_exception)
        #Form error message
        error_message = error_message + ".Error Code: " + self.error_source + "_" + error_code+ ".Trace Id: " \
        + str(uuid.uuid4().hex) if error_code else error_message + ".Source Code: " \
        + self.error_source+ ".Trace Id: " + str(uuid.uuid4().hex)
        #Print stacktrace for tracing in logs
        logging.error(error_message + os.linesep + traceback.format_exc())
        super().__init__(error_message)

##########################
### GENERIC CORE EXCEPTION
##########################

class EnvironmentVariableNotFound(CustomExceptionHandler):
    """ Custom Exception class to handle exceptions when environment variables are not found """
    def __init__(self, variable_name: str, **kwargs):
        super().__init__(error_message = StatusMessages.ENV_VARIABLE_NOT_FOUND.value.format(variable_name=variable_name), **kwargs)

class NoRecordsFound(CustomExceptionHandler):
    """ Custom Exception class to handle exceptions when No Records are found in Cosmos DB """
    def __init__(self,**kwargs):
        super().__init__(error_message = StatusMessages.RECORDS_NOT_FOUND.value, **kwargs)

class GenericTechnicalIssue(CustomExceptionHandler):
    '''Custom Exception class to handle exceptions when cosmos steps fails'''
    def __init__(self,error_message:str, actual_exception: Exception, error_code: str = None, **kwargs):
        super().__init__(error_message = error_message, actual_exception = actual_exception, 
                         error_code = error_code if error_code else StatusCodes.TECHNICAL_EXCEPTION.value, **kwargs)
        

##########################
### CUSTOM EXCEPTION
##########################        