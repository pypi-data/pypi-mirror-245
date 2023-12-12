"""Perform password cracking using brute-force"""
from hashlib import md5, sha256
from itertools import product
from os import makedirs
from os.path import dirname, exists, join

import bcrypt

from haxcore.classes.crack.crack_base import CrackBase
from haxcore.classes.crack.enums import CrackType, HashAlgorithm
from haxcore.classes.crack.wordlist_rules import WordlistRules
from haxcore.utilities.config import CORE_DIR
from haxcore.utilities.wordlist import load_wordlist


class BruteForce(CrackBase):
  """Class to perform brute force password cracking"""
  def __init__(self, wordlist_file: str, wordlist_rules: WordlistRules):
    super().__init__(CrackType.BRUTE_FORCE)
    self.wordlist_file = join(CORE_DIR, "assets", ".wordlist", wordlist_file)
    self.wordlist: list = load_wordlist(self.wordlist_file, wordlist_rules)
    self.wordlist_rules = wordlist_rules

  def _generate_password_file(self, hash_pass):
    file_name = "crack.pass"
    file_path = join(CORE_DIR, "assets", ".brute_force", file_name)
    if not exists(dirname(file_path)):
      makedirs(dirname(file_path))
    with open(file_path, "w", encoding="UTF-8") as file:
      file.write(hash_pass)
    return file_path

  def get_all_rules(self, charset, count):
    """Rainbow table generation method"""
    rules_list = []
    perm = list(product(charset, repeat=count))
    rules_list = [(''.join(p).replace('', ' $'))[1:-2] for p in perm]
    return rules_list

  def _generate_rules_file(self, wordlist_rules: WordlistRules):
    file_name = "crack.rules"
    file_path = join(CORE_DIR, "assets", ".brute_force", file_name)
    if not exists(dirname(file_path)):
      makedirs(dirname(file_path))
    with open(file_path, "w", encoding="UTF-8") as file:
      if wordlist_rules.postfix_count > 0:
        rules_list = self.get_all_rules(wordlist_rules.postfix_charset, wordlist_rules.postfix_count)
        for rule in rules_list:
          file.write(rule + "\n")
      if wordlist_rules.prefix_count > 0:
        rules_list = self.get_all_rules(wordlist_rules.prefix_charset, wordlist_rules.prefix_count)
        for rule in rules_list:
          file.write(rule + "\n")
    return file_path

  def start(self, hash_pass, hash_algorithm: HashAlgorithm, stop_flag, update_status_func):
    """Start brute-force password cracking process"""
    password = self.find_hash(hash_pass, hash_algorithm, stop_flag)
    if password:
      update_status_func(0, 0, f"Password found, the password is: {password}")
    else:
      update_status_func(0, 0, "Password not found!")

  def find_hash(self, hash_pass, hash_algorithm: HashAlgorithm, stop_flag: bool):
    """Find hash based on wordlist"""
    with open(self.wordlist_file, "r", encoding="UTF-8") as file:
      wordlist = file.readlines()
    hash_pass_hexdigest = hash_pass.encode()
    for word in wordlist:
      if stop_flag:
        break
      word_bytes = word.strip().encode()
      if hash_algorithm == HashAlgorithm.MD5:
        hash_result = md5(word_bytes)
        hash_hexdigest = hash_result.hexdigest()
      elif hash_algorithm == HashAlgorithm.SHA256:
        hash_result = sha256(word_bytes)
        hash_hexdigest = hash_result.hexdigest()
      elif hash_algorithm == HashAlgorithm.BCRYPT:
        salt = bcrypt.gensalt()
        hash_hexdigest = bcrypt.hashpw(word_bytes, salt).decode()
      if hash_pass_hexdigest == hash_hexdigest:
        return word
    return None
