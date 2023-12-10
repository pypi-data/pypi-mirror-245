"""Database operation related to the setting"""
from haxcore.classes.db.enums import Table

from .base import Criteria
from .commands import run_sql, select_all, select_one_item


def update_setting(name: str, value: str):
  """insert setting into database"""
  item = get_setting_by_name(name)
  args: tuple = tuple()
  if item:
    command = "UPDATE setting SET name = ?, value = ? WHERE id = ?"
    item_id = item[0]
    args = (name, value, item_id)
  else:
    command = "INSERT INTO setting (name, value) values (?, ?)"
    args = (name, value)
  return run_sql(command, args)


def get_setting_by_name(name: str):
  """get specific setting value from database"""
  return select_one_item(Table.SETTING, [Criteria("name", name, Criteria.Op.EQ)])


def get_all_setting():
  """get setting value from database"""
  result = select_all(Table.SETTING)
  setting = {}
  for item in result:
    setting[item[1]] = item[2]
  return setting
