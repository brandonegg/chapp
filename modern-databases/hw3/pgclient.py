from exceptions import InvalidCredentialFileException
from queries import QueryBuilder
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

  def print_cities(self, postal=None, country=None, name=None):
    query = QueryBuilder()
    query.select("homework.cities", ["name", "postal_code", "country_code"])
      
    options = [("postal_code", postal), ("country_code", country), ("name", name)]
    for (column, value) in options:
      if value is None:
        continue
  
      query.where(f"{column} = '{value}'")

    query_str = query.end()
    print(query_str)

    with self.connection.cursor() as cursor:
      cursor.execute(query_str)
      cities = cursor.fetchall()

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

  def delete_city(self, postal=None, country=None, name=None):
    # TODO
    # select and display all effected rows then ask user to confirm with y/n prompt
    pass
