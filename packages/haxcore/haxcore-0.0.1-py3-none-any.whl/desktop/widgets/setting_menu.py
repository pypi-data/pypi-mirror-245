"""The main menu of the application"""
from customtkinter import CTkFrame

from desktop.widgets.classes.menu_item import MenuItem
from haxcore.classes.gui.enums import Windows


class SettingMenu(CTkFrame):
  """The setting menu of the application"""
  def __init__(self, root_window):
    self.root_window = root_window
    super().__init__(root_window, width=150, corner_radius=0)
    self.current_window = Windows.NONE

  def init_items(self, event_func):
    """Initialize the menu items"""
    self.menu_items = [
      MenuItem(self, "General", "xss.png", Windows.GENERAL_SETTING),
      MenuItem(self, "Appearance", "xss.png", Windows.APPEARANCE_SETTING),
      MenuItem(self, "Cloud backend", "xss.png", Windows.CLOUD_SETTING)
    ]

    row = 0
    for item in self.menu_items:
      self.create_menu_item(item, row, event_func)
      row = row + 1

  def mouse_click(self, event, window: Windows, click_event_func):
    """Call when a mouse click the menu item"""
    if self.current_window == window:
      return
    self.current_window = window
    click_event_func(event, window)

  def create_menu_item(self, item, row, click_event_func):
    """Create Button as menu item"""
    item.btn.bind("<Button-1>", lambda e: self.mouse_click(e, item.window, click_event_func))
    item.btn.grid(row=row, column=0, sticky="nsew")
