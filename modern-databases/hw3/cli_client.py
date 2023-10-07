from pg_client import PGClient
from exceptions import CommandNotFoundException, InvalidCommandFormatException
import time

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
  def __init__(self, pg_client: PGClient):
    self.pg_client = pg_client
    self.commands = [Command("countries:list", "List all available countries", self.pg_client.print_all_countries, None),
                     Command("cities:list", "List cities matching arguments", self.pg_client.list_cities_cli, {"postal": "postal code", "country": "country code", "name": "city name"}),
                     Command("cities:create", "Create a new city", self.pg_client.create_city, {"postal": "postal code", "country": "country code", "name": "city name"}),
                     Command("cities:update", "Update a city's name", self.pg_client.update_city, {"postal": "postal code", "country": "country code", "name": "city name"}),
                     Command("cities:delete", "Delete one or many cities", self.pg_client.delete_city_cli, {"postal": "postal code", "country": "country code", "name": "city name"}),
                     Command("venues:active:list", "List active venues based on search criteria", self.pg_client.list_venues_active_cli, {"country": "country code"}),
                     Command("venues:inactive:list", "List all inactive venues", self.pg_client.list_venues_inactive_cli, None),
                     Command("venues:delete", "Delete a venue by name", self.pg_client.delete_venue_confirm_cli, {"name": "Name of venue (case sensitive)"}),
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
    print("| Example: 'cities:list postal=52240,name=Iowa'")
    print("|")

    for i, command in enumerate(self.commands):
      print(f"|- {i}. {command}")

    print("|")

  def __exit(self):
    print("Exiting application and closing the PostgreSQL connection")
    self.pg_client.connection.close()
    exit(0)