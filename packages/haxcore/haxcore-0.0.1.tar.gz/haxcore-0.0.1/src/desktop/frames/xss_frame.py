"""CrossSite Scripting injection frame"""
# pylint: disable=R0801
from tkinter import INSERT

from customtkinter import CTk

from desktop.frames.attack_frame import AttackFrame
from haxcore.classes.attacks.attack_manager import AttackManager
from haxcore.classes.attacks.enums import AttackType, RequestType


class XssFrame(AttackFrame):
  """CrossSite attack frame"""

  def __init__(self, root_window: CTk):
    super().__init__(root_window, "CrossSite Scripting (XSS) attack", "xss.txt")

  def __init_frame__(self):
    """Initialize frame components"""
    super().__init_frame__()

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=2)
    self.grid_rowconfigure(7, weight=1)

    self.add_label("URL (without GET params)").grid(row=0, column=0)
    self.input_url = self.add_entry()
    self.input_url.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

    self.add_label(text="Paramaters sep by comma (e.g. par1,par2)").grid(row=1, column=0)
    self.input_parameters = self.add_entry()
    self.input_parameters.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

    self.add_label("Placeholder Text (replaced in payloads)").grid(row=2, column=0)
    self.input_placeholder_text = self.add_entry()
    self.input_placeholder_text.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")

    self.add_label("Request type").grid(row=3, column=0)
    self.opt_request_type = self.add_option(*(RequestType.get_names()))
    self.opt_request_type.grid(row=3, column=1, padx=(10, 10), pady=(10, 10), sticky="w")

    self.add_button("Start Attack", self.init_attack).grid(row=4, column=0, columnspan=2)

    self.progbar_attacks = self.add_progressbar()
    self.progbar_attacks.grid(row=5, column=0, columnspan=2, padx=(30, 30), pady=(10, 10), sticky="news")

    self.txt_log = self.add_log()
    self.txt_log.grid(row=7, column=0, columnspan=2, sticky="news")

  def set_default_input(self):
    """default value for the input"""
    super().set_default_input()
    self.input_url.insert(INSERT, "https://google.com")
    self.input_parameters.insert(INSERT, "name")
    self.opt_request_type.set("POST")

  def init_attack(self):
    """prepare the request and start the attack"""
    url = self.input_url.get()
    request_type = RequestType[self.opt_request_type.get()]
    parameters = self.input_parameters.get().split(",")
    placeholder_text = self.input_placeholder_text.get()
    self.attack_manager = AttackManager(url, request_type, parameters, placeholder_text, AttackType.XSS)
    self.start_attack()
