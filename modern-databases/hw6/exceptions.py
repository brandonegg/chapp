class InvalidCredentialFileException(Exception):
  pass

class InvalidCommandFormatException(Exception):
  pass

class CommandNotFoundException(Exception):
  pass

class NoEntityResultsFound(Exception):
  def __init__(self, entity:str):
    self.message = f"No {entity} found with provided criteria"
    super().__init__(self.message)