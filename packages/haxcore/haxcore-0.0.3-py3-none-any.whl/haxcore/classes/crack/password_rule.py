"""Class to define password rules"""
from hashlib import md5


class PasswordRule:
  """Class to represent password rules"""
  def __init__(self, character_set: str, min_length: int, max_length: int, number_count: int = 0,
               uppercase_count: int = 0, lowercase_count: int = 0, symbols_count: int = 0):
    # pylint: disable=too-many-boolean-expressions, chained-comparison
    if (not character_set) or \
        (max_length < min_length) or \
        (min_length < 1 and min_length > 30) or \
        (max_length < 1 and max_length > 30) or \
        (number_count < 0 and number_count > max_length) or \
        (uppercase_count < 0 and uppercase_count > max_length) or \
        (lowercase_count < 0 and lowercase_count > max_length) or \
        (symbols_count < 0 and symbols_count > max_length):
      raise ValueError("Password rules are not valid")

    self.character_set = character_set
    self.min_length = min_length
    self.max_length = max_length
    self.number_count = number_count
    self.uppercase_count = uppercase_count
    self.lowercase_count = lowercase_count
    self.symbols_count = symbols_count

  def __str__(self) -> str:
    str_representation = f"{self.character_set}{self.min_length}" + \
      f"{self.max_length}{self.number_count}{self.uppercase_count}" + \
      f"{self.lowercase_count}{self.symbols_count}"
    return str(md5(str_representation.encode()).hexdigest())

  def check_if_follow(self, password: str):
    """Check if password follow the rules"""
    return bool(password)
