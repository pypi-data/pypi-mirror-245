"""Attack manager module to perform and manage a series attacks on sepecific target"""

from threading import Thread

from haxcore.classes.crack.crack_base import CrackBase
from haxcore.classes.crack.enums import HashAlgorithm


class CrackPassManager:
  """Class to manage performing a crack password"""
  def start(self, crack: CrackBase, hash_pass, hash_algo: HashAlgorithm, update_status_func):
    """Start the cracking operation in separate thread"""
    self.crack_thread = Thread(
        target=self._start_crack,
        args=(
          crack,
          hash_pass,
          hash_algo,
          update_status_func,
        ),
    )
    self.crack_thread.start()

  def _start_crack(self, crack: CrackBase, hash_pass, hash_algo: HashAlgorithm, update_status_func):
    """Initiate the attack using all provided payloads"""
    self.stop_flag = False
    crack.start(hash_pass, hash_algo, lambda: self.stop_flag, update_status_func)
    self.is_finish = True

  def stop(self):
    """Stop the crack"""
    self.stop_flag = True
