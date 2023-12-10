"""All enums in the app"""
from enum import Enum


class ConfigType(Enum):
  """Different confiuration files"""
  DESIGN = "design.yml"
  GENERAL = "general.yml"
  DB = "db.yml"
  LOG = "log.yml"
