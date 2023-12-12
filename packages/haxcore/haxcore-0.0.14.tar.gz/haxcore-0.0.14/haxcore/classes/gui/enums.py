"""All enums in the app"""
from enum import Enum


class Windows(Enum):
  """All frames available"""
  NONE = 0
  XSS = 1
  SQLI = 2
  CRACK_PASS = 10
  SETTING = 20
  GENERAL_SETTING = 21
  APPEARANCE_SETTING = 22
  CLOUD_SETTING = 23
  ABOUT = 30


class Color(Enum):
  """The application color types"""
  PRIMARY = 1
  SECONDARY = 2
  THIRD = 3
  FORTH = 4
  BORDER = 5
  HOVER = 6
