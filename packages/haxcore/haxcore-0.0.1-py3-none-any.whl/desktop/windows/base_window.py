"""Base class for child windows in the application"""
from customtkinter import CTk, CTkToplevel

from ..frames.base_frame import BaseFrame


class BaseWindow(CTkToplevel):
  """Base class for child windows in the application"""

  def __init__(self, root_window: CTk, width: int, height: int, title: str):
    self.root_window = root_window
    super().__init__(root_window)
    self.title(title)
    self.width = width
    self.height = height
    self.set_size_position()
    self.resizable(False, False)

    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)
    self._init_main_frame()

    self.set_default_input()
    self.is_ready = True

  def set_size_position(self):
    """set the window size and position"""
    x_cordinate = int(self.root_window.winfo_x() + (self.root_window.winfo_width()//2) - (self.width//2))
    y_cordinate = int(self.root_window.winfo_y() + (self.root_window.winfo_height()//2) - (self.height//2))
    self.geometry(f"{self.width}x{self.height}+{x_cordinate}+{y_cordinate}")
    self.lift()

  def _init_main_frame(self):
    self.main_frame = BaseFrame(self)
    self.main_frame.grid(row=0, column=0, sticky="news")

  def set_default_input(self):
    """Set default value for the window widgets"""
    if hasattr(self, "main_frame"):
      self.main_frame.set_default_input()
