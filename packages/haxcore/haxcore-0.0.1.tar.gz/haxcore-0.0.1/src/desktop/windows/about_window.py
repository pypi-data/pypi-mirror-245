"""About window to show information about the application"""
from desktop.windows.base_window import BaseWindow
from haxcore.utilities.config import GENERAL, get_logo


class AboutWindow(BaseWindow):
  """About window to show information about the application"""
  def __init__(self, root_window):
    super().__init__(root_window, 600, 400, "About HaX")

  def _init_main_frame(self):
    super()._init_main_frame()
    link = GENERAL["domain"]
    about = GENERAL["about"]

    self.main_frame.columnconfigure(0, weight=1)
    self.main_frame.rowconfigure((0, 1, 2), weight=1)

    img_logo = self.main_frame.add_image(get_logo(), size=(300, 125))
    img_logo.grid(row=0, column=0, sticky="news")
    self.main_frame.add_label(about, justify="center").grid(row=1, column=0)
    self.main_frame.add_link(link, link).grid(row=2, column=0)
