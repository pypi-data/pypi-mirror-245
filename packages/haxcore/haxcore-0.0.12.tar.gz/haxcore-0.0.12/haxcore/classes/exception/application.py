"""general exceptions for teh application"""


class ConfigException(Exception):
  """raise when config not exist, or config load failed"""
  def __init__(self, config: str, *args):
    super().__init__(args)
    self.message = f"Failed retriving {config} configuration"
