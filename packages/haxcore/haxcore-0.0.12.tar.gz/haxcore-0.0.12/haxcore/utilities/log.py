"""All logging operations"""
import logging
from datetime import datetime
from enum import Enum
from os import listdir, makedirs, remove, stat
from os.path import isdir, join
from time import time

from haxcore.utilities.config import CORE_DIR, LOG


class LogLevel(Enum):
  """Different log level"""
  INFO = logging.INFO
  WARN = logging.WARNING
  ERR = logging.ERROR
  CRIT = logging.CRITICAL


LOGS_DIR = join(CORE_DIR, "assets", LOG['folder'])


def get_new_log_file():
  """get new file for logging and add header"""
  if not isdir(LOGS_DIR):
    makedirs(LOGS_DIR)
  file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log.csv")
  log_file_path = join(LOGS_DIR, file_name)
  return log_file_path


LOGGER_FILE = get_new_log_file()
LOGGER = logging.getLogger()


def init_log():
  """init logging"""
  delete_old_logs()
  LOGGER.setLevel(LOG["level"])
  file_handler = logging.FileHandler(LOGGER_FILE, mode="w")
  file_handler.setLevel(LOG["level"])
  formatter = logging.Formatter(LOG["format"], LOG["date_format"])
  file_handler.setFormatter(formatter)
  LOGGER.addHandler(file_handler)


def log_msg(msg: str, level: LogLevel = LogLevel.INFO):
  """log message with a specific level"""
  sanitized_msg = msg.strip().replace("\n", " ")
  LOGGER.log(msg=sanitized_msg, level=level.value)


def delete_old_logs():
  """delete old log file that older than expiry date"""
  expiry_days = LOG['expiry_days']
  for file in listdir(LOGS_DIR):
    now = time()
    expiry_date = now - (expiry_days * 86400)
    file_path = join(LOGS_DIR, file)
    if stat(file_path).st_mtime < expiry_date:
      remove(file_path)
