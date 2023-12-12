"""Import the core methods and classes for HaX tool"""
# flake8: noqa

from pathlib import Path

import toml

from .classes.attacks.attack_manager import AttackManager
from .classes.attacks.enums import AttackType, RequestType
from .classes.crack.brute_force import BruteForce
from .classes.crack.crack_pass_manager import CrackPassManager
from .classes.crack.enums import CrackType, HashAlgorithm
from .classes.crack.password_rule import PasswordRule
from .classes.crack.rainbow import Rainbow
from .classes.crack.wordlist_rules import WordlistRules
from .classes.exception.database import SQLException
from .classes.gui.enums import Color, Windows
# import manager classes
from .utilities.config import CORE_DIR, GENERAL, get_app_initial_size, get_app_min_size, get_color, get_icon, get_image_path, get_logo
from .utilities.db.base import execuate, init_db
from .utilities.db.tbl_attack import get_all_attacks, get_attack_by_url, insert_attack, update_attack
from .utilities.db.tbl_setting import get_all_setting, get_setting_by_name, update_setting
from .utilities.log import LOGGER_FILE, LogLevel, init_log, log_msg


def get_version():
  """Get the package version from the toml file"""
  path = Path(__file__).resolve().parents[1] / 'pyproject.toml'
  with open(str(path), "r", encoding="utf-8") as toml_file:
    pyproject = toml.loads(toml_file.read())
    return pyproject['tool']['poetry']['version']

__version__ = get_version()
