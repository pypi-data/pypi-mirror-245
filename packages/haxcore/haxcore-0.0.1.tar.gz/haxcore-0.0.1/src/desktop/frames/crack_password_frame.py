"""CrossSite Scripting injection frame"""
# pylint: disable=R0801
from tkinter import END, INSERT, StringVar

from customtkinter import CTk

from desktop.frames.base_frame import BaseFrame
from haxcore.classes.crack.brute_force import BruteForce
from haxcore.classes.crack.crack_pass_manager import CrackPassManager
from haxcore.classes.crack.enums import CrackType, HashAlgorithm
from haxcore.classes.crack.password_rule import PasswordRule
from haxcore.classes.crack.rainbow import Rainbow
from haxcore.classes.crack.wordlist_rules import WordlistRules


class CrackPasswordFrame(BaseFrame):
  """Crack password frame"""

  def __init__(self, root_window: CTk):
    super().__init__(root_window, "Crack Password")
    self.crack_manager = CrackPassManager()

  def _clear_frame(self):
    for widgets in self.winfo_children():
      widgets.destroy()

  def __init_frame__(self):
    """Initialize frame components"""
    super().__init_frame__()

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=2)
    self.grid_rowconfigure(4, weight=1)

    self.add_label("Hash password").grid(row=0, column=0)
    self.hash_password = self.add_entry()
    self.hash_password.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

    self.add_label("Hash Algorithm").grid(row=1, column=0)
    self.opt_hash_algorithm = self.add_option(*(HashAlgorithm.get_names()))
    self.opt_hash_algorithm.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="w")

    self.add_label("Crack Type").grid(row=2, column=0)
    self.opt_crack_type = self.add_option(*(CrackType.get_names()),
                                          callback=self.select_crack_type)
    self.opt_crack_type.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="w")

    self.options_frame = BaseFrame(self)
    self.init_options_frame(CrackType.RAINBOW.name)
    self.options_frame.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="news", columnspan=2)

    self.add_button("Crack Password", self.crack_password).grid(row=4, column=0, columnspan=2)

    self.progbar_crack = self.add_progressbar()
    self.progbar_crack.grid(row=5, column=0, columnspan=2, padx=(30, 30), pady=(10, 10), sticky="news")

    self.txt_log = self.add_log()
    self.txt_log.grid(row=6, column=0, columnspan=2, sticky="news")

  def select_crack_type(self, crack_type: str):
    """Event when select crack type"""
    self.init_options_frame(crack_type)
    self.set_default_input()

  def init_options_frame(self, crack_type: str):
    """Init all options widget based on the cracking type"""
    for widgets in self.options_frame.winfo_children():
      widgets.destroy()
    self.options_frame.grid_columnconfigure((0, 2), weight=1)
    self.options_frame.grid_columnconfigure((1, 3), weight=2)

    if crack_type == CrackType.BRUTE_FORCE.name:
      self.options_frame.add_label("Wordlist file").grid(row=0, column=0)
      self.options_frame.wordlist_file = self.options_frame.add_entry()
      self.options_frame.wordlist_file.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew", columnspan=3)

      self.options_frame.add_label("Prefix count").grid(row=1, column=0)
      self.options_frame.prefix_count = self.options_frame.add_num_entry()
      self.options_frame.prefix_count.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.options_frame.add_label("Prefix character set").grid(row=1, column=2)
      self.options_frame.prefix_charset = self.options_frame.add_entry()
      self.options_frame.prefix_charset.grid(row=1, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.options_frame.add_label("Postfix count").grid(row=2, column=0)
      self.options_frame.postfix_count = self.options_frame.add_num_entry()
      self.options_frame.postfix_count.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.options_frame.add_label("Postfix character set").grid(row=2, column=2)
      self.options_frame.postfix_charset = self.options_frame.add_entry()
      self.options_frame.postfix_charset.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.check_double_wordlist = StringVar(self.options_frame, "off")
      self.options_frame.double_wordlist = self.options_frame.add_checkbox("Double Wordlist", self.check_double_wordlist)
      self.options_frame.double_wordlist.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

    elif crack_type == CrackType.RAINBOW.name:
      self.options_frame.add_label("Character set").grid(row=1, column=0)
      self.options_frame.character_set = self.options_frame.add_entry()
      self.options_frame.character_set.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="ew", columnspan=3)

      self.options_frame.add_label("Minimum length").grid(row=2, column=0)
      self.options_frame.min_length = self.options_frame.add_num_entry()
      self.options_frame.min_length.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.options_frame.add_label("Maximum length").grid(row=2, column=2)
      self.options_frame.max_length = self.options_frame.add_num_entry()
      self.options_frame.max_length.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.options_frame.add_label("Rainbow table length").grid(row=3, column=0)
      self.options_frame.rainbow_length = self.options_frame.add_num_entry()
      self.options_frame.rainbow_length.grid(row=3, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

      self.options_frame.add_label("Rainbow table depth").grid(row=3, column=2)
      self.options_frame.rainbow_depth = self.options_frame.add_num_entry()
      self.options_frame.rainbow_depth.grid(row=3, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")

  def set_default_input(self):
    """default value for the input"""
    super().set_default_input()
    crack_type = self.opt_crack_type.get()
    crack_method = CrackType[crack_type] if crack_type else CrackType.RAINBOW.name
    self.hash_password.delete(0, END)
    if crack_method is CrackType.BRUTE_FORCE:
      self.hash_password.insert(INSERT, "$2b$12$ufSkYpr8Q8AKvCYRNs3ISuCSyTK1AoD25iA/5U2y/5JBtNm11HCom")
      self.opt_hash_algorithm.set(HashAlgorithm.BCRYPT.name)
      self.options_frame.wordlist_file.insert(INSERT, "wordlist.txt")
      self.options_frame.prefix_count.insert(INSERT, "3")
      self.options_frame.prefix_charset.insert(INSERT, "+-*&@")
      self.options_frame.postfix_count.insert(INSERT, "0")
    elif crack_method is CrackType.RAINBOW:
      self.hash_password.insert(INSERT, "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4")
      self.opt_hash_algorithm.set(HashAlgorithm.SHA256.name)
      self.options_frame.character_set.insert(INSERT, "0-9")
      self.options_frame.min_length.insert(INSERT, 4)
      self.options_frame.max_length.insert(INSERT, 4)
      self.options_frame.rainbow_length.insert(INSERT, 6000)
      self.options_frame.rainbow_depth.insert(INSERT, 10)

  def crack_password(self):
    """prepare the crack and start the cracking the password"""
    hash_pass = self.hash_password.get()
    crack_method = CrackType[self.opt_crack_type.get()]

    hash_algo = HashAlgorithm[self.opt_hash_algorithm.get()]

    if crack_method is CrackType.BRUTE_FORCE:
      wordlist_file = self.options_frame.wordlist_file.get()
      is_double = self.check_double_wordlist.get() == "on"
      pref_charset = self.options_frame.prefix_charset.get()
      pref_count = int(self.options_frame.prefix_count.get())
      post_charset = self.options_frame.postfix_charset.get()
      post_count = int(self.options_frame.postfix_count.get())
      wordlist_rules = WordlistRules(is_double, pref_charset, pref_count, post_charset, post_count)
      crack = BruteForce(wordlist_file, wordlist_rules)
    elif crack_method is CrackType.RAINBOW:
      char_set = self.options_frame.character_set.get()
      min_pass_len = int(self.options_frame.min_length.get())
      max_pass_len = int(self.options_frame.max_length.get())
      rainbow_len = int(self.options_frame.rainbow_length.get())
      rainbow_dep = int(self.options_frame.rainbow_depth.get())
      rule = PasswordRule(char_set, min_pass_len, max_pass_len)
      crack = Rainbow(rule, rainbow_len, rainbow_dep)

    self.crack_num = 0
    self.txt_log.delete("1.0", END)
    self.crack_manager.start(crack, hash_pass, hash_algo, self.update_status)

  def update_status(self, total, index, message):
    """Update the form status"""
    self.progbar_crack.set((index / total) if total else 0)
    if message:
      self.txt_log.insert(END, message + "\n")
