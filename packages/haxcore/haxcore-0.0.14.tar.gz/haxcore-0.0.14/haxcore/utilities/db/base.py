""""Database base operations"""
from dataclasses import dataclass
from enum import Enum
from sqlite3 import DatabaseError, IntegrityError, connect

from haxcore.classes.exception.database import DBException
from haxcore.utilities.config import DB, get_db_path
from haxcore.utilities.log import LogLevel, log_msg

DATABASE_PATH = get_db_path()


def execuate(command: str, args, with_commit: bool = False):
  """Execuate SQL command"""
  try:
    with connect(DATABASE_PATH) as con:
      cur = con.cursor()
      if args:
        cur.execute(command, args)
      else:
        cur.execute(command)
      if with_commit:
        con.commit()
    log_msg(f"command [{command}] execuated successfully", LogLevel.INFO)
    return cur
  except IntegrityError as ex:
    message = f"Can not insert [{args}] twice"
    log_msg(message, LogLevel.CRIT)
    raise DBException(message, ex.args) from ex
  except DatabaseError as ex:
    message = f"Database error while execuating command [{command}] with args: [{args}]"
    log_msg(message, LogLevel.CRIT)
    raise DBException(message, ex.args) from ex
  except Exception as ex:
    message = f"Failed execuating command [{command}] with args: [{args}]"
    log_msg(message, LogLevel.CRIT)
    raise DBException(message, ex.args) from ex


def run(command: str, args: tuple) -> bool:
  """Execuate non-select database command"""
  is_succ = False
  try:
    cur = execuate(command, args, True)
    is_succ = cur.rowcount > 0
    cur.close()
  except DBException:
    is_succ = False
  return is_succ


def fetch(command: str, args: tuple) -> list:
  """Execuate select database command"""
  try:
    cur = execuate(command, args)
    result: list = cur.fetchall()
    cur.close()
    return result
  except DBException:
    return []


def init_db():
  """Initilaize database tables"""
  run(DB["attack"], None)
  run(DB["setting"], None)


@dataclass
class Criteria:
  """WHERE clousre criteria parameters"""
  class Op(Enum):
    """Different criteria operations in the SQL query"""
    EQ = "="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    LIKE = "LIKE"

  name: str
  value: str
  ops: Op = Op.EQ
