"""Database exceptions"""


class SQLException(Exception):
  """raise when sql command is not execuated as expected"""
  def __init__(self, command, *args):
    super().__init__(args)
    self.command = command


class DBException(Exception):
  """raise when db failed execuating command"""
  def __init__(self, message, *args):
    super().__init__(args)
    self.message = message
