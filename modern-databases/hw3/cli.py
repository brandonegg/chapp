from pgclient import PGClient

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
    self.commands = [Command("exit", "Exit the application", self.__exit)]
    self.__main_routine()

  def __main_routine(self):
    self.__output_commands()
    self.__await_response()

  def __await_response(self):
    user_input = input("Select an option (index number or name) from the list above: ")
    self.__call_command(self.__parse_command_str(user_input))

  def __parse_command_str(self, input: str):
    # TODO:
    return input

  def __call_command(self, parsed_str: str):
    # TODO:
    pass

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