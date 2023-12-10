"""The menubar of the application"""
from tkinter import Menu


class MenuBar(Menu):
  """The menu bar for the application"""
  def __init__(self, root_window):
    super().__init__(root_window)
    self.root_window = root_window

  def init_items(self):
    """Init the menubar items"""
    filemenu = Menu(self, tearoff=0)
    filemenu.add_command(label="New", command={})
    filemenu.add_command(label="Open", command={})
    filemenu.add_command(label="Save", command={})
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=self.root_window.quit)
    self.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(self, tearoff=0)
    helpmenu.add_command(label="Help Index", command={})
    helpmenu.add_command(label="About...", command={})
    self.add_cascade(label="Help", menu=helpmenu)
