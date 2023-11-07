from exceptions import CommandNotFoundException, InvalidCommandFormatException
import time
from mongo_client import MongoDBClient

class Command:
  def __init__(self, label, description, callback, args: dict[str, str] | None):
    self.label = label
    self.description = description
    self.callback = callback
    self.args = args

  def call(self, args):
    try:
      self.callback(**args)
    except Exception as e:
      print(f"Error: {e}")

  def __repr__(self):
    base = f"{self.label} - {self.description}"

    if self.args is not None:
      base += "\n|         Arguments:"
      for name in self.args:
        description = self.args[name]
        base += f"\n|            - {name}={description}"

    return base

class CLISession:
  def __init__(self, db_client: MongoDBClient):
    self.db = db_client
    self.commands = [Command("nearest", "List nearest businesses to a given latitude longitude pair.", self.db.find_nearest, {"lat": "Latitude value", "lon": "Longitude value"}),
                     Command("exit", "Exit the application", self.__exit, None)]
    
    self.__main_routine()

  def __main_routine(self):
    self.__output_commands()
    self.__await_response()
    time.sleep(5)
    self.__main_routine()

  def __await_response(self):
    user_input = input("| Select an option (index number or name) from the list above: ")
    print("------------------------------------")

    try:
      self.__call_command(*self.__parse_command_str(user_input))
    except InvalidCommandFormatException:
      print("ERROR: Invalid format of command, please input either the index number or name of the command")
    except CommandNotFoundException:
      print("ERROR: No command found with the provided name/index")

    print("")

  def __parse_command_str(self, input: str):
    input = input.strip('')
    split_input = input.split(" ")

    args = {}

    if len(split_input) > 2:
      split_input[1] = ' '.join(split_input[1:])
    elif len(split_input) == 1:
      return (split_input[0], args)

    for arg_str in split_input[1].split(","):
      split_arg_str = arg_str.split("=")
      if not len(split_arg_str) == 2:
        raise InvalidCommandFormatException
      
      args[split_arg_str[0]] = split_arg_str[1]

    return (split_input[0], args) #command name, args

  def __call_command(self, parsed_cmd: str, args: dict[str, str]):    
    for command in self.commands:
      if command.label == parsed_cmd:
        command.call(args)
        return
      
    try:
      cmd_index = int(parsed_cmd)
    except:
      raise CommandNotFoundException
    
    if cmd_index >= len(self.commands):
      raise CommandNotFoundException
    
    self.commands[cmd_index].call(args)

  def __output_commands(self):
    print("------------------------------------")
    print("| Command Table                    |")
    print("------------------------------------")
    print("| Format:  {command name | index} {arg1=arg1_value},{arg2=arg2_value},...")
    print("| Example: 'nearest lat=41.661240,lon=-91.530128'")
    print("|")

    for i, command in enumerate(self.commands):
      print(f"|- {i}. {command}")

    print("|")

  def __exit(self):
    print("Exiting application and closing the MongoDB connection")
    self.db.close()
    exit(0)