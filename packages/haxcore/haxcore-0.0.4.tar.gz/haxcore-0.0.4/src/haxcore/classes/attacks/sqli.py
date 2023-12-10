"""Module providing SQLI injection attack"""
from requests import Response

from .attack import Attack


class SqliAttack(Attack):
  """Class represent a normal SQL injection attack"""
  # pylint: disable=too-few-public-methods

  def is_attack_succeeded(self, response: Response) -> bool:
    """Examine the response status code to identify whether the SQL injection attack was successful"""
    return bool(response.status_code == 200)
