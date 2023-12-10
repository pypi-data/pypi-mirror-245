"""Module of the main application form"""
from tkinter import PhotoImage

from customtkinter import CTk

from desktop.frames.crack_password_frame import CrackPasswordFrame
from desktop.frames.sqli_frame import SqliFrame
from desktop.frames.xss_frame import XssFrame
from desktop.widgets.main_menu import MainMenu
from desktop.widgets.menubar import MenuBar
from desktop.windows.about_window import AboutWindow
from desktop.windows.setting_window import SettingWindow
from haxcore.classes.gui.enums import Windows
from haxcore.utilities.config import get_app_initial_size, get_app_min_size, get_icon
from haxcore.utilities.log import LogLevel, log_msg


class App(CTk):
  """The main application window"""
  def __init__(self):
    super().__init__()
    self.main_menu = MainMenu(root_window=self)
    self.menubar = MenuBar(root_window=self)
    self.__init_components__()
    self.is_ready = True

  def __set_size_position(self):
    size = get_app_initial_size()
    window_height = size["height"]
    window_width = size["width"]

    x_cordinate = int((self.winfo_screenwidth()/2) - (window_width/2))
    y_cordinate = int((self.winfo_screenheight()/2) - (window_height/2))
    self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    min_size = get_app_min_size()
    self.minsize(min_size["width"], min_size["height"])

  def __init_components__(self):
    """Initialize the main form GUI components"""
    self.title("HaX Cybersecurity tool")
    self.__set_size_position()
    self.resizable(True, True)

    # Set the application icon
    photo = PhotoImage(file=get_icon())
    self.iconphoto(False, photo)

    # init the menubar and its components
    self.menubar.init_items()
    self.configure(menu=self.menubar)

    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=0)
    self.grid_rowconfigure(0, weight=1)

    # init the main menu and place it in hte main window
    self.main_menu.init_items(self._click_menu)
    self.main_menu.grid(column=0, row=0, sticky="nsew")

    # No frame is showing when app launch
    self.current_frame = None

  def is_window_open(self, window_type: type):
    """Check if a specific window type is open"""
    for _, child in self.children.items():
      if isinstance(child, window_type):
        return child
    return None

  def _click_menu(self, event, window: Windows, is_window=True):
    # pylint: disable=unused-argument
    """Fill a frame into the main window when the user click on main menu"""
    if is_window:
      self._fill_window(window)
    else:
      self._fill_frame(window)

    log_msg(f"{window} opened", LogLevel.INFO)

  def _fill_frame(self, window: Windows):
    """fill a frame into the main frame"""
    # destroy the old frame
    if self.current_frame:
      self.current_frame.destroy()
      self.current_frame = None
    # initialize the new frame
    if window == Windows.XSS:
      self.current_frame = XssFrame(self)
    elif window == Windows.SQLI:
      self.current_frame = SqliFrame(self)
    elif window == Windows.CRACK_PASS:
      self.current_frame = CrackPasswordFrame(self)
    else:
      raise NotImplementedError(f"The frame '{window}' hasn't implemented yet")
    # show the frame into the main window
    self.current_frame.grid(row=0, column=1, sticky="nsew")

  def _fill_window(self, window: Windows):
    """open a new window or re-position an opened window"""
    if window == Windows.SETTING:
      window = self.is_window_open(SettingWindow)
      if window:
        window.set_size_position()
      else:
        SettingWindow(self)
    elif window == Windows.ABOUT:
      window = self.is_window_open(AboutWindow)
      if window:
        window.set_size_position()
      else:
        AboutWindow(self)

  def run(self):
    """run the main application interface"""
    log_msg("Application Start")
    self.mainloop()
    log_msg("Application End")
