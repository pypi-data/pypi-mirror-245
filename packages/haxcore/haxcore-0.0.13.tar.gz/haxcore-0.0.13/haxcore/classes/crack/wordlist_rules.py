"""Class to define wordlist rules"""


# pylint: disable=too-few-public-methods
class WordlistRules:
  """Class to represent password rules"""
  def __init__(self, is_double, prefix_charset, prefix_count, postfix_charset, postfix_count):
    self.is_double = is_double
    self.prefix_charset = prefix_charset
    self.prefix_count = prefix_count
    self.postfix_charset = postfix_charset
    self.postfix_count = postfix_count
