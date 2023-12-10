"""base class for all attacks"""
from os.path import join
from tkinter import END

from desktop.frames.base_frame import BaseFrame
from haxcore.classes.attacks.attack_manager import AttackManager
from haxcore.utilities.config import CORE_DIR


class AttackFrame(BaseFrame):
  """base class for the attack forms"""

  attack_num = 0

  def __init__(self, root_window, title: str, payloads_file: str):
    super().__init__(root_window=root_window, title=title)
    self.payloads_path = join(CORE_DIR, "assets", ".payloads", payloads_file)
    self.attack_manager: AttackManager = AttackManager()

  def __init_frame__(self):
    """Initialize frame components"""
    super().__init_frame__()
    self.progbar_attacks = self.add_progressbar()
    self.txt_log = self.add_log()

  def set_default_input(self):
    """default value for the input"""
    # configuring the log tags to colorize output
    super().set_default_input()
    self.txt_log.tag_config("SUCCESS", background="green")
    self.txt_log.tag_config("FAILED", background="red")

  def destroy(self) -> None:
    """destroy the frame and its components"""
    if self.attack_manager:
      self.attack_manager.stop()
    super().destroy()

  def start_attack(self):
    """Start the attack"""
    if not self.attack_manager:
      return
    self.txt_log.delete(1.0, END)  # clear text
    self.attack_num = 0
    self.attack_manager.start(self.payloads_path, self.add_result)

  def add_result(self, result, is_success):
    """Add result to the log text component"""
    self.txt_log.insert(END, result)
    row = (self.attack_num * 7) + 5
    # add tag using indices for the part of text to be highlighted
    self.txt_log.tag_add("SUCCESS" if is_success else "FAILED", f"{row}.0", f"{row}.100")
    self.txt_log.see(END)
    self.attack_num += 1
    self.progbar_attacks.set(self.attack_num / self.attack_manager.total_attacks)
