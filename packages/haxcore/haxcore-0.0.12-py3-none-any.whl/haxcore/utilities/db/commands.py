"""Database operation related to the setting"""


from haxcore.classes.db.enums import Table
from haxcore.classes.exception.database import SQLException

from .base import Criteria, fetch, run


def run_sql(command: str, args: tuple = ()):
  """run SQL command and return result"""
  if command.lower().strip().startswith("select"):
    result = fetch(command, args)
  else:
    result = run(command, args)  # type: ignore
    if not result:
      raise SQLException(f"Failed execuation SQL command [{command}]")
  return result


def select_all(table: Table):
  """Select all records from a table"""
  command = f"SELECT * FROM {Table(table).name}"  # noqa: S608
  return run_sql(command)


def select_one_item(table: Table, criteria: list[Criteria]):
  """Select ONLY one record from a table using criteria"""
  result = select_items(table, criteria)
  if len(result) > 1:
    raise SQLException("select_one_item return more than an item")
  return result[0] if result else None


def select_items(table: Table, criteria: list[Criteria]):
  """Select records from a table using criteria"""
  args: tuple = ()
  conditions = []
  for item in criteria:
    args += (item.value,)
    conditions.append(f"{item.name}{item.ops.value}?")
  condition = ",".join(conditions)
  command = f"SELECT * FROM {Table(table).name} WHERE {condition}"  # noqa: S608
  result = run_sql(command, args)
  return result
