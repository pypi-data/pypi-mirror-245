"""Module providing CrossSite Scripting injection attack"""
from re import IGNORECASE, search

from requests import Response

from .attack import Attack

XSS_SUCCESS_PATTEREN = r"<script[^\n]*>[^\n]*(`|\(\"|\(\')xss(`|\"\)|'\))[^\n]*<\/script[^\n]*>"


class XssAttack(Attack):
  """Class represent a CrossSite attack"""
  # pylint: disable=too-few-public-methods

  def is_attack_succeeded(self, response: Response) -> bool:
    """Examine the response content to identify whether the CrossSite Scripting attack was successful"""
    response_body = response.content.decode()
    result = search(pattern=XSS_SUCCESS_PATTEREN, string=response_body, flags=IGNORECASE)
    return bool(result)
