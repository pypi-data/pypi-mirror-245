"""Appearance config frame"""
# pylint: disable=R0801
from customtkinter import CTk

from desktop.frames.base_frame import BaseFrame


class AppearanceSettingFrame(BaseFrame):
  """Appearance setting frame"""

  def __init__(self, root_window: CTk):
    super().__init__(root_window, "Appearance Configuration")

  def __init_frame__(self):
    """Initialize frame components"""
    super().__init_frame__()

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=2)

    save_btn = self.add_button("Save", self.save_setting)
    save_btn.grid(row=2, column=0)

  def save_setting(self):
    """Save setting"""
