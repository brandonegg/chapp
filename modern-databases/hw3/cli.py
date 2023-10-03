from pgclient import PGClient
from exceptions import CommandNotFoundException, InvalidCommandFormatException

class Command:
  def __init__(self, label, description, callback):
    self.label = label
    self.description = description
    self.callback = callback

  def call(self):
    self.callback()

  def __repr__(self):
    return f"{self.label} - {self.description}"

class CLISession:
  def __init__(self, pg_client: PGClient):
    self.pg_client = pg_client
    self.commands = [Command("countries:list", "List all available countries", self.pg_client.print_all_countries),
                     Command("exit", "Exit the application", self.__exit)]
    
    self.__main_routine()

  def __main_routine(self):
    self.__output_commands()
    self.__await_response()
    self.__main_routine()

  def __await_response(self):
    user_input = input("| Select an option (index number or name) from the list above: ")
    print("------------------------------------")

    try:
      self.__call_command(self.__parse_command_str(user_input))
    except InvalidCommandFormatException:
      print("ERROR: Invalid format of command, please input either the index number or name of the command")
    except CommandNotFoundException:
      print("ERROR: No command found with the provided name/index")

    print("")

  def __parse_command_str(self, input: str):
    input = input.strip('')
    split_input = input.split(" ")

    if not len(split_input) == 1:
      raise InvalidCommandFormatException

    return split_input[0]

  def __call_command(self, parsed_cmd: str):
    for command in self.commands:
      if command.label == parsed_cmd:
        command.call()
        return
      
    try:
      cmd_index = int(parsed_cmd)
    except:
      raise CommandNotFoundException
    
    if cmd_index >= len(self.commands):
      raise CommandNotFoundException
    
    self.commands[cmd_index].call()

  def __output_commands(self):
    print("------------------------------------")
    print("| Command Table                    |")
    print("------------------------------------")

    print("|")

    for i, command in enumerate(self.commands):
      print(f"|- {i}. {command}")

    print("|")

  def __exit(self):
    print("Exiting application and closing the PostgreSQL connection")
    self.pg_client.connection.close()
    exit(0)