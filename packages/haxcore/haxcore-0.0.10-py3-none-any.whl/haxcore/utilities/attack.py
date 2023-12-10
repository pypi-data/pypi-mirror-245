"""different methods to support payloads files"""


def load_payloads(placeholder_text: str, file_path: str) -> list:
  """Load the attack payloads from a file"""
  with open(file_path, "r", encoding="UTF-8") as payloads_file:
    return [payload.strip("\n").replace("{{PLACEHOLDER}}", placeholder_text) for payload in payloads_file.readlines()]
