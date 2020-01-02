# coding: utf-8
"""
log设置
"""
import os
import logging
import platform
from logging import handlers


def singleton(cls):
    instances = {}

    def wrapper(*args, **kargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kargs)
        return instances[cls]

    return wrapper


@singleton
class Logger:

    def __init__(self,
                 logpath='/var/log',
                 logname='system.log',
                 logmaxsize=1*1024*512,
                 consolelog=True):
        self._path = logpath
        self._name = logname
        self._max_size = logmaxsize
        self._stdout = consolelog

        self._level = logging.DEBUG
        self._formatter = logging.Formatter("%(asctime)s %(levelname)s %(process)d-%(thread)d [%(pathname)s] "
                                            "[%(filename)s-%(funcName)s] Line: %(lineno)s - %(message)s")
        self._logger = logging.getLogger()

        if not os.path.exists(self._path):
            os.makedirs(self._path)

        self._filename = os.path.join(self._path, self._name)
        self._filehandler = handlers.RotatingFileHandler(filename=self._filename,
                                                         encoding="utf-8",
                                                         maxBytes=self._max_size,
                                                         backupCount=1)
        self._filehandler.setFormatter(self._formatter)

        self._logger.setLevel(self._level)
        self._logger.addHandler(self._filehandler)

        if platform.system() == 'Windows':
            self._stdout = True
        else:
            self._stdout = False

        if self._stdout:
            self._consolehandler = logging.StreamHandler()
            self._consolehandler.setFormatter(self._formatter)
            self._logger.addHandler(self._consolehandler)

    def get_logger(self):
        return self._logger

    def debug(self, message, *args, optionsmsg=""):
        """
        调试日志
        :param message:
        :param optionsmsg:
        :return:
        """
        try:
            for msg in args:
                message += " |%s" % (str(msg))
            message += " |%s" % (str(optionsmsg))
            self._logger.debug(msg=message)
        except Exception as err:
            print("err", err)
            return False

    def info(self, message, *args, optionsmsg=""):
        """
        一般日志
        :param message:
        :param optionsmsg:
        :return:
        """
        try:
            for msg in args:
                message += " |%s" % (str(msg))
            message += " |%s" % (str(optionsmsg))
            self._logger.info(msg=message)
        except Exception as err:
            print("err", err)
            return False

    def warring(self, message, *args, optionsmsg=""):
        """
        警告日志
        :param message:
        :param optionsmsg:
        :return:
        """
        try:

            for msg in args:
                message += " |%s" % (str(msg))
            message += " |%s" % (str(optionsmsg))
            self._logger.warning(msg=message)
        except Exception as err:
            print("err", err)
            return False

    def error(self, message, *args, optionsmsg=""):
        """
        错误日志
        :param message:
        :param optionsmsg:
        :return:
        """
        try:
            for msg in args:
                message += " |%s" % (str(msg))
            message += " |%s" % (str(optionsmsg))
            self._logger.error(msg=message)
        except Exception as err:
            print("err", err)
            return False
