"""Base class to crack password"""
from haxcore.classes.crack.enums import CrackType


# pylint: disable=too-few-public-methods
class CrackBase:
  """Class represents Cyber Attack"""
  def __init__(self, crack_type: CrackType):
    self.crack_type = crack_type

  # pylint: disable=unused-argument
  def start(self, hash_pass, hash_algorithm, stop_flag, update_status_func):
    """Start cracking process"""
    if not stop_flag():
      return
    update_status_func()
