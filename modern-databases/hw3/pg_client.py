from exceptions import InvalidCredentialFileException
from queries import QueryBuilder
from helpers import cli_user_confirm_action
import psycopg2

class Credentials:
  def __init__(self, cred_path: str):
    self.__read_credentials(cred_path)

  def __read_credentials(self, cred_path: str):
    with open(cred_path, 'r') as file:
      file_contents = file.read().split('\n')
      if len(file_contents) < 2:
        raise InvalidCredentialFileException
      
      self.username = file_contents[0]
      self.password = file_contents[1]

class PGClient:
  def __init__(self, cred_path: str, host: str, port: int, db_name: str):
    self.credentials = Credentials(cred_path)

    self.connection = psycopg2.connect(user = self.credentials.username,
                                       password = self.credentials.password,
                                       host = host,
                                       port = port,
                                       database = db_name)
    
    self.connection.autocommit = True

  def print_all_countries(self):
    with self.connection.cursor() as cursor:
      cursor.execute('SELECT country_code, country_name FROM homework.countries')
      countries = cursor.fetchall()
      formatted_country_str = [f"{country_name} ({country_code})" for (country_code, country_name) in countries]
      
      print("List of countries {name (code)}:")
      print("")
      print(', '.join(formatted_country_str))

  def select_cities(self, postal=None, country=None, name=None):
    query = QueryBuilder()
    query.select("homework.cities", ["name", "postal_code", "country_code"])
      
    options = [("postal_code", postal), ("country_code", country), ("name", name)]
    for (column, value) in options:
      if value is None:
        continue
  
      query.where(f"{column} = '{value}'")

    query_str = query.end()

    with self.connection.cursor() as cursor:
      cursor.execute(query_str)
      cities = cursor.fetchall()
      return cities

  def list_cities_cli(self, postal=None, country=None, name=None):
    cities = self.select_cities(postal, country, name)

    print("Cities:")
    print("")
    if len(cities) == 0:
      print("No matches found for criteria")
    print(', '.join([str(city) for city in cities]))

  def create_city(self, postal, country, name):
    print(len(country))
    with self.connection.cursor() as cursor:
      cursor.execute(f"INSERT INTO homework.cities (name, country_code, postal_code) VALUES ('{name}', '{country}', '{postal}')")

      print(f"Success! New city added: ({name}, {country}, {postal})")

  def update_city(self, postal, country, name):
    with self.connection.cursor() as cursor:
      cursor.execute(f"UPDATE homework.cities SET name = '{name}' WHERE (country_code = '{country}' AND postal_code = '{postal}')")

      print(f"Successfully updated name to: {name}")

  def delete_city_cli(self, postal=None, country=None, name=None):
    '''
    Delete city with confirmation prompt
    '''
    delete_cities = self.select_cities(postal, country, name)
    if len(delete_cities) == 0:
      raise "No cities found with provided criteria"

    print("The following cities will be deleted:")
    print(', '.join([str(city) for city in delete_cities]))

    should_delete = cli_user_confirm_action("Confirm deletion of the cities above?")
    if not should_delete:
      raise Exception('User cancelled')

    self.delete_city(postal, country, name)
    print(f"successfully deleted {len(delete_cities)} entries")

  def delete_city(self, postal=None, country=None, name=None):
    query = QueryBuilder()
    query.delete("homework.cities")

    options = [("postal_code", postal), ("country_code", country), ("name", name)]
    for (column, value) in options:
      if value is None:
        continue
  
      query.where(f"{column} = '{value}'")

    query_str = query.end()

    with self.connection.cursor() as cursor:
      cursor.execute(query_str)

  def list_venues_active_cli(self, country: str):
    venues = self.list_venues(True, country)
    print("Venues:")
    print("")
    if len(venues) == 0:
      print("No matches found for criteria")
    print(', '.join([str(venue) for venue in venues]))

  def list_venues_inactive_cli(self):
    venues = self.list_venues(False, None)
    print("Venues:")
    print("")
    if len(venues) == 0:
      print("No inactive venues found")
    print(', '.join([str(venue) for venue in venues]))

  def list_venues(self, active: bool, country: str | None = None):
    query = QueryBuilder()
    query.select("homework.venues", ["venue_id", "name", "street_address", "type", "postal_code", "country_code"])

    if country is not None:
      query.where(f"country_code = '{country}'")

    if active:
      query.where(f"NOT inactive")
    else:
      query.where(f"inactive")

    query_str = query.end()

    with self.connection.cursor() as cursor:
      cursor.execute(query_str)

      return cursor.fetchall()

  def delete_venue_confirm_cli(self):
    pass

  def delete_venue(self):
    pass
