"""Perform password cracking using Rainbow table"""
from hashlib import md5, sha256
from itertools import product
from os import makedirs
from os.path import dirname, exists, join

import bcrypt
import pandas as pd

from haxcore.classes.crack.crack_base import CrackBase
from haxcore.classes.crack.enums import CrackType, HashAlgorithm
from haxcore.classes.crack.password_rule import PasswordRule
from haxcore.utilities.config import CORE_DIR


class Rainbow(CrackBase):
  """Class to perform rainbow password cracking"""
  def __init__(self, password_rule: PasswordRule, length: int, depth: int):
    super().__init__(CrackType.RAINBOW)
    self.password_rule = password_rule
    self.length = length
    self.depth = depth

  def get_all_passwords(self):
    """Rainbow table generation method"""
    all_chars = self._get_all_allowed_chars()
    passwords = []
    for length in range(self.password_rule.min_length, self.password_rule.max_length+1):
      perm = list(product(all_chars, repeat=length))
      passwords = [''.join(p) for p in perm]
    return passwords

  def _get_all_allowed_chars(self) -> str:
    """get the allowed characters in the password"""
    all_chars = ""
    char_sets = self.password_rule.character_set.split(",")
    for char_set in char_sets:
      if "-" in char_set and len(char_set) == 3:
        start = ord(char_set[0])
        end = ord(char_set[2])
        for i in range(start, end+1):
          all_chars = all_chars + chr(i)
      elif len(char_set) == 1:
        all_chars = all_chars + char_set
      else:
        raise ValueError("Not valid char_set")
    return all_chars

  def _get_rainbow_table_file(self):
    file_name = f"rainbow-{self.length}-{self.depth}-{self.hash_algorithm.name}-{self.password_rule}.csv"
    file_path = join(CORE_DIR, "assets", ".rainbow_tables", file_name)
    if not exists(dirname(file_path)):
      makedirs(dirname(file_path))
    return file_path

  def generate_rainbow_table(self, passwords: list[str], stop_flag, update_status_func):
    """generate the rainbow table"""
    records_length = 0
    rainbow_file = self._get_rainbow_table_file()
    if exists(rainbow_file):
      update_status_func(0, 0, "Rainbow table already exist, no need to generate a new one.")
      return
    update_status_func(0, 0, "Rainbow table NOT exist, generating it now.")
    with open(rainbow_file, "w", encoding="UTF-8") as rainbow_table:
      loop_count = len(passwords)
      rainbow_table.write("password,hash\n")
      rainbow_records: list[str] = []
      for i in range(loop_count):
        password = passwords[i].encode()
        if password in rainbow_records:
          continue
        chain = self._get_chain(password)
        passwords_chain = [pair[0] for pair in chain]
        rainbow_records.extend(passwords_chain)
        hash_end = chain[self.depth-1][1]
        rainbow_table.write(f"{passwords[i]},{hash_end}\n")
        records_length = records_length + 1

        if records_length > self.length or stop_flag():
          break
        update_status_func(loop_count, i, None)
    update_status_func(0, 0, "Rainbow table has been generate successfully")
    del rainbow_records[:]

  def _get_chain(self, password):
    chain = []
    hash_result = None
    for _ in range(self.depth):
      if chain:
        hash_digest = int.from_bytes(hash_result.digest(), byteorder="big")
        pass_to_hash = str(hash_digest % 10000).zfill(4).encode()
      else:
        pass_to_hash = password

      if self.hash_algorithm == HashAlgorithm.MD5:
        hash_result = md5(pass_to_hash)
        hash_hexdigest = hash_result.hexdigest()
      elif self.hash_algorithm == HashAlgorithm.SHA256:
        hash_result = sha256(pass_to_hash)
        hash_hexdigest = hash_result.hexdigest()
      elif self.hash_algorithm == HashAlgorithm.BCRYPT:
        salt = bcrypt.gensalt()
        hash_hexdigest = bcrypt.hashpw(pass_to_hash, salt)
      chain.append((pass_to_hash, hash_hexdigest))
    return chain

  def find_hash(self, hash_pass):
    """Crack the password hased in a specific algorithm"""
    rainbow_file = self._get_rainbow_table_file()
    chunksize = 10 ** 6
    dtype = {"password": str, "hash": str}

    with pd.read_csv(rainbow_file, chunksize=chunksize, dtype=dtype) as reader:
      for chunk in reader:
        for _, row in chunk.iterrows():
          hash_val = row[1]
          if hash_val == hash_pass:
            return row[0]
    return None

  def crack_password(self, hash_pass, update_status_func):
    """Crack hashed password"""
    update_status_func(0, 0, "Searching into the rainbow table...")
    chain_start = self.find_hash(hash_pass)
    if chain_start:
      update_status_func(0, 0, "The hash found into the rainbow table")
      chain = self._get_chain(chain_start.encode())
      return chain[self.depth-1][0].decode()

    update_status_func(0, 0, "The hash NOT found into the rainbow table, checking the hash chain...")
    chain_start = str(int(hash_pass, 16) % 10000).zfill(4)
    chain = self._get_chain(chain_start.encode())
    for pair in chain:
      chain_start = self.find_hash(pair[1])
      if chain_start:
        new_chain = self._get_chain(chain_start.encode())
        for pair in new_chain:
          if pair[1] == hash_pass:
            return pair[0].decode()
    return None

  def start(self, hash_pass, hash_algorithm: HashAlgorithm, stop_flag, update_status_func):
    """Start rainbow cracking process"""
    self.hash_algorithm = hash_algorithm
    all_passwords = self.get_all_passwords()
    self.generate_rainbow_table(all_passwords, stop_flag, update_status_func)
    password = self.crack_password(hash_pass, update_status_func)
    if password:
      update_status_func(0, 0, f"Password found, the password is: {password}")
    else:
      update_status_func(0, 0, "Password not found!")
