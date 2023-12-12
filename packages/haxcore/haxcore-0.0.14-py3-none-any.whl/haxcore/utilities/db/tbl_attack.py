"""Database operation related to the attacks"""
from haxcore.classes.attacks.attack import Attack
from haxcore.classes.attacks.enums import AttackType, RequestType
from haxcore.classes.db.enums import Table

from .base import Criteria
from .commands import run_sql, select_all, select_one_item


def insert_attack(url: str, request_type: RequestType, attack_type: AttackType, parameters: str):
  """insert setting into database"""
  command = "INSERT INTO setting (url, request_type, parameters, attack_type) values (?, ?, ?, ?)"
  args = (url, request_type, parameters, attack_type,)
  return run_sql(command, args)


def update_attack(item_id: int, url: str, request_type: RequestType, attack_type: AttackType, parameters: str):
  """update attack in the database"""
  command = """UPDATE attack SET
    url = ?,
    request_type = ?
    parameters = ?
    attack_type = ?
  WHERE id = ?"""
  args = (url, request_type, parameters, attack_type, item_id,)
  return run_sql(command, args)


def get_attack_by_url(url: str):
  """get attack from database using its url"""
  return select_one_item(Table.ATTACK, [Criteria("url", url, Criteria.Op.EQ)])


def get_all_attacks():
  """get all attacks from database"""
  result = select_all(Table.ATTACK)
  attacks = []
  for item in result:
    request_type = RequestType(item[2])
    attack_type = AttackType(item[4])
    attacks.append(Attack(item[1], request_type, item[3], attack_type))
  return attacks
