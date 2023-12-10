"""Attack manager module to perform and manage a series attacks on sepecific target"""

from threading import Thread
from time import sleep

import requests

from haxcore.classes.attacks.enums import AttackType, RequestType
from haxcore.classes.exception.connection import ConnectionFailedException
from haxcore.utilities.attack import load_payloads

from .attack import Attack
from .sqli import SqliAttack
from .xss import XssAttack


class AttackManager:
  """Class to manage performing a specific attack on a website"""
  attack: Attack

  def __init__(self, url: str = "", request_type: RequestType = RequestType.GET,
               paramaters=None, placeholder_text: str = "", attack_type: AttackType = AttackType.XSS):
    if attack_type is AttackType.XSS:
      self.attack = XssAttack(url, request_type, paramaters, attack_type)
    elif attack_type is AttackType.SQLI:
      self.attack = SqliAttack(url, request_type, paramaters, attack_type)
    else:
      self.attack = Attack(url, request_type, paramaters, attack_type)
    self.placeholder_text = placeholder_text

  def start(self, payloads_file: str, add_result_func):
    """Start the attack in separate thread"""
    payloads: list = load_payloads(self.placeholder_text, payloads_file)
    self.total_attacks = len(payloads)
    self.is_finish = False
    self.attack_thread = Thread(
        target=self._start_attack,
        args=(
            self.attack,
            payloads,
            add_result_func,
        ),
    )
    self.attack_thread.start()

  def _start_attack(self, attack: Attack, payloads: str, add_result_func):
    """Initiate the attack using all provided payloads"""
    self.stop_flag = False
    for payload in payloads:
      # for each payload, get the request ready and then send it to the server
      with self._send_http_request(attack, payload) as response:
        # get the attack result
        if self.stop_flag:
          return
        is_success = attack.is_attack_succeeded(response)
        result = self.summarize_response(payload, response, is_success)
        add_result_func(result, is_success)
        sleep(0.1)
    self.is_finish = True

  def stop(self):
    """Stop the attack"""
    self.stop_flag = True

  def _send_http_request(self, attack: Attack, attack_payload: str) -> requests.Response:
    """initialize HTTP request and return response"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
      if attack.request_type == RequestType.POST:
        payload = {parameter: attack_payload for parameter in attack.paramaters}
        response = requests.post(url=attack.url, headers=headers, data=payload, timeout=30)
      elif attack.request_type == RequestType.GET:
        form_data = []
        for parameter in attack.paramaters:
          form_data.append(f"{parameter}={attack_payload}")
        request_url = f"{attack.url.split('?', 1)[0]}?{'&'.join(form_data)}"
        response = requests.get(url=request_url, headers=headers, timeout=30)
      return response
    except requests.exceptions.ConnectTimeout as ex:
      raise ConnectionFailedException(attack.url, "Timeout", ex.args) from ex
    except requests.exceptions.ConnectionError as ex:
      raise ConnectionFailedException(attack.url, "Connection Error", ex.args) from ex
    except Exception as ex:
      raise ConnectionFailedException(attack, "Unkown", ex.args) from ex

  def summarize_response(self, payload: str, response: requests.Response, is_success: bool):
    """get attack response text"""
    response_result = ""
    response_result += f"PAYLOAD: {payload}\n"
    response_result += f"REQUEST URL: {response.request.url}\n"
    response_result += f"REQUEST HEADERS: {response.request.headers}\n"
    req_body = str(response.request.body)
    response_result += f"REQUEST BODY: {req_body}\n"
    if is_success:
      response_result += "The attack has succeded\n"
    else:
      response_result += "The attack has failed\n"
    response_result += "-" * 50
    response_result += "\n" * 2
    return response_result
