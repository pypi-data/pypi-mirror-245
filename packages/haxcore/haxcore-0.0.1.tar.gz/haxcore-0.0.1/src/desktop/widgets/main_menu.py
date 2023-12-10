"""The main menu of the application"""
from customtkinter import CTkFont, CTkFrame, CTkImage, CTkLabel
from PIL import Image

from desktop.widgets.classes.menu_item import MenuItem
from haxcore.classes.gui.enums import Windows
from haxcore.utilities.config import get_icon


class MainMenu(CTkFrame):
  """The main menu of the application"""
  def __init__(self, root_window):
    self.root_window = root_window
    super().__init__(root_window, width=150, corner_radius=0)
    self.current_window = Windows.NONE

  def init_items(self, event_func):
    """Initialize the menu items"""
    self.menu_items_top = [
      MenuItem(self, "XSS Attack", "xss.png", Windows.XSS),
      MenuItem(self, "SQLi Attack", "sqli.png", Windows.SQLI),
      MenuItem(self, "Crack Password", "password.png", Windows.CRACK_PASS),
    ]
    self.menu_items_down = [
      MenuItem(self, "Setting", "setting.png", Windows.SETTING),
      MenuItem(self, "About HaX", "about.png", Windows.ABOUT)
    ]
    self.grid_rowconfigure(len(self.menu_items_top)+1, weight=1)

    logo = CTkImage(dark_image=Image.open(get_icon()), size=(40, 40))
    lbl_logo = CTkLabel(self, text=" HaX Tool", image=logo, compound="left", font=CTkFont(size=20, weight="bold"))
    lbl_logo.grid(row=0, column=0, padx=0, pady=10, sticky="ew")
    row = 1
    for item in self.menu_items_top:
      self.create_menu_item(item, row, event_func)
      row = row + 1
    row = row + 1
    for item in self.menu_items_down:
      self.create_menu_item(item, row, event_func)
      row = row + 1

  def mouse_click(self, event, window: Windows, click_event_func):
    """Call when a mouse click the menu item"""
    is_window = window in (Windows.ABOUT, Windows.SETTING)
    if not is_window:
      if self.current_window == window:
        return
      self.current_window = window
    click_event_func(event, window, is_window)

  def create_menu_item(self, item, row, click_event_func):
    """Create Button as menu item"""
    item.btn.bind("<Button-1>", lambda e: self.mouse_click(e, item.window, click_event_func))
    item.btn.grid(row=row, column=0, sticky="nsew")
