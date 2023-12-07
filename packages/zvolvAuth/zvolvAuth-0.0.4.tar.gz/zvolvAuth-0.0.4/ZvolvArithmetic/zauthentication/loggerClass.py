"""
    Logging module
"""
import logging
import logging.handlers
import socket
import json
import sys
import os
import traceback
import datetime
from ZvolvArithmetic.zauthentication.server_configuration import EnvVariables
from ZvolvArithmetic.zauthentication import user_defined_exceptions

def format_exception(e):
    """
    This function will format the exception message into a list and return it
    :param e: Exception
    :return:
    """
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
    # print exception_list
    return exception_list


class LoggerClass:
    """
    This class will create the singleton logger object with logger dictionary which will map the logger name with logging object

    Exmaple:
        -API Logging:
            api_log({"message":"API Logs","url":BASE_URL,"body":body,"method":method})

        -Queue Logging:
            queue_log({"message": "Queue Logs ","queue": "tube_WF", "zviceId":body['BusinessTag']})

        -python logging:
            pythonLog({"message": "Python Logs,"zviceId":body['BusinessTag']})

        -Business Specific Logging:
            log(body['BusinessTag'],{"message":"Business Logs","zviceID":body['BusinessTag']})
        This function has two parameters as it will create business.log file at runtime

    """
    __instance = None  # private variable

    def __init__(self):

        if LoggerClass.__instance:  # If instance is already present
            raise Exception("This class is a singleton!")
        else:
            LoggerClass.__instance = self
            LoggerClass.__instance.loggers = {}  # dictionary of logger_name and logging object as key and value


    @staticmethod
    def create_logger(app_name, log_level=logging.DEBUG, stdout=False, syslog=True, file=False):
        """
        create logging object with logging to syslog, file and stdout
        :param app_name app name
        :param log_level logging log level
        :param stdout log to stdout
        :param syslog log to syslog
        :param file log to file
        :return: logging object
        """
        # disable requests logging
        # logging.getLogger("requests").setLevel(logging.ERROR)
        # logging.getLogger("urllib3").setLevel(logging.ERROR)

        # create logger
        logger = logging.getLogger(app_name)
        logger.setLevel(log_level)

        # set log format to handlers
        formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
        path = "/var/log/script-logs/script-logs.log"
        if file:
            # create file logger handler
            fh = logging.FileHandler('my-sample-app.log')
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        if syslog:
            # create syslog logger handler
            env_syslog_hanlder_address, env_syslog_hanlder_port = EnvVariables.get_syslog_hanlder_address(), EnvVariables.get_syslog_hanlder_port()
            try:
                syslog_hanlder_address = (env_syslog_hanlder_address, int(
                    env_syslog_hanlder_port)) if env_syslog_hanlder_port else env_syslog_hanlder_address

            except (ValueError,TypeError):
                raise user_defined_exceptions.RsysLogConnectionFailed(message_details=
                                                                {"SYSLOG_HANDLER_ADDRESS":EnvVariables.get_syslog_hanlder_address(),
                                                                 "SYSLOG_HANDLER_PORT":EnvVariables.get_syslog_hanlder_port()})
            try:
                sh = logging.handlers.SysLogHandler(address=syslog_hanlder_address)
            except socket.error:
                raise user_defined_exceptions.RsysLogConnectionFailed(message_details={"SYSLOG_HANDLER_ADDRESS":env_syslog_hanlder_address})
            sh.setLevel(log_level)
            sf = logging.Formatter('%(name)s: %(message)s')
            sh.setFormatter(sf)
            logger.addHandler(sh)

        if stdout:
            # create stream logger handler
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        return logger

    @staticmethod
    def error(logger_name,log_message_dict):
        log = LoggerClass.get_log(logger_name)
        log_message_dict = update_log_message_dict(log_message_dict, "ERROR")
        message = (json.dumps(log_message_dict))[:127999] if len(json.dumps(log_message_dict)) > 128000 else (json.dumps(log_message_dict))
        log.error(message)

    @staticmethod
    def debug(logger_name,log_message_dict):
        log = LoggerClass.get_log(logger_name)
        log_message_dict = update_log_message_dict(log_message_dict, "DEBUG")
        message = (json.dumps(log_message_dict))[:127999] if len(json.dumps(log_message_dict)) > 128000 else (json.dumps(log_message_dict))
        log.debug(message)

    @staticmethod
    def warn(logger_name,log_message_dict):
        log = LoggerClass.get_log(logger_name)
        log_message_dict = update_log_message_dict(log_message_dict, "WARN")
        message = (json.dumps(log_message_dict))[:127999] if len(json.dumps(log_message_dict)) > 128000 else (json.dumps(log_message_dict))
        log.warn(message)

    @staticmethod
    def warning(logger_name,log_message_dict):
        """
        This function will print the str object of dict(logging message's dict) in given loggername's file
        :param logger_name: api_log,pythonLog,etc.,
        :param dict:
        :return:
        """
        log = LoggerClass.get_log(logger_name)
        log_message_dict = update_log_message_dict(log_message_dict, "WARNING")
        message = (json.dumps(log_message_dict))[:127999] if len(json.dumps(log_message_dict)) > 128000 else (json.dumps(log_message_dict))

        log.warning(message)

    @staticmethod
    def info(logger_name,log_message_dict):
        """
        This function will print the str object of dict(logging message's dict) in given loggername's file
        :param logger_name: api_log,pythonLog,etc.,
        :param dict:
        :return:
        """
        log = LoggerClass.get_log(logger_name)
        log_message_dict = update_log_message_dict(log_message_dict, "INFO")
        message = (json.dumps(log_message_dict))[:127999] if len(json.dumps(log_message_dict)) > 128000 else (json.dumps(log_message_dict))
        log.info(message)

    @staticmethod
    def exception_log(logger_name,log_message_dict):
        e = log_message_dict['exception']
        log_message_dict['exception'] = {  # formatting exception object to avoid json serializable error
            "error": e.__class__.__name__,
            "args": str(e.args),
            "message": str(e.message),
            "traceback": format_exception(e)
        }
        log = LoggerClass.get_log(logger_name)
        log_message_dict = update_log_message_dict(log_message_dict, "ERROR")
        message = (json.dumps(log_message_dict))[:127999] if len(json.dumps(log_message_dict)) > 128000 else (json.dumps(log_message_dict))
        log.error(message)

    @classmethod
    def get_log(cls, logger_name):
        """
        This function will search the logger name in logger dictionaries keys.
        If it is present then it will return the corresponding logger object
        else it will create object using setup_logger()
        :param logger_name: String
            Example : "root","api_log"
        :return:
        """
        if not cls.__instance:
            LoggerClass()
        if logger_name in cls.__instance.loggers.keys():  # the log object already exists in logger dict
            return cls.__instance.loggers[logger_name]
        logger = LoggerClass.create_logger(logger_name)
        cls.__instance.loggers[logger_name] = logger
        return logger


def update_log_message_dict(log_message_dict, log_level):
    """
    Returns updated log_message_dict
    :param log_message_dict: message dictionary
    :param log_level: logging level
    :return:
    """
    new_contents = {'log_level': log_level, 'DateCreated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"pid":os.getpid()}
    log_message_dict.update(new_contents)
    return log_message_dict