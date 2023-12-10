"""Class represent menu item"""
from customtkinter import CTkButton, CTkImage
from PIL import Image

from haxcore.classes.gui.enums import Windows
from haxcore.utilities.config import get_image_path


class MenuItem:
  """Class represent one menu item in the app"""
  # pylint: disable=too-few-public-methods
  def __init__(self, parent, name="", image="", window=Windows.NONE):
    self.parent = parent
    self.name = name
    self.image = image
    self.window = window

    self.img = CTkImage(dark_image=Image.open(get_image_path(image)), size=(25, 25))
    self.btn = CTkButton(parent, image=self.img, width=200, height=40, text=self.name, compound='left', anchor="w",
                         corner_radius=0, border_spacing=10, fg_color="transparent",
                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),)
