# coding:utf-8

import logging
import logging.handlers
import os, sys
from config import Config


class Log:
    logger = None

    @staticmethod
    def get_logger():
        if Log.logger is not None:
            return Log.logger
        Log.logger = logging.getLogger()
        Log.logger.setLevel(Config.LOG_LEVEL)
        rotating_file_handler = logging.handlers.RotatingFileHandler(
            Config.LOG_FILE_PATH,
            maxBytes=Config.LOG_MAX_SIZE,
            backupCount=Config.LOG_BACKUP_COUNT,
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s-[%(levelname)s][%(module)s][%(funcName)s]-%(message)s')
        rotating_file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        rotating_file_handler.setLevel(Config.FILE_LOG_LEVEL)
        stream_handler.setLevel(Config.STREAM_LOG_LEVEL)
        Log.logger.addHandler(rotating_file_handler)
        Log.logger.addHandler(stream_handler)
        return Log.logger


LOG = Log.get_logger()
