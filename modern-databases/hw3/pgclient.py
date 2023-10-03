from exceptions import InvalidCredentialFileException
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

  def print_all_countries(self):
    with self.connection.cursor() as cursor:
      cursor.execute('SELECT country_code, country_name FROM homework.countries')
      countries = cursor.fetchall()
      formatted_country_str = [f"{country_name} ({country_code})" for (country_code, country_name) in countries]
      
      print("List of countries {name (code)}:")
      print("")
      print(', '.join(formatted_country_str))

  def print_cities(self, postal=None, country=None, name=None):
    use_and = False
    query = 'SELECT name, postal_code, country_code FROM homework.cities'

    options = [("postal_code", postal), ("country_code", country), ("name", name)]
    for (column, value) in options:
      if value is None:
        continue

      if use_and:
        query += ' AND'
      else:
        query += ' WHERE'
        use_and = True

      query += f" {column} = '{value}'"

    with self.connection.cursor() as cursor:
      cursor.execute(query)
      cities = cursor.fetchall()

      print("Cities:")
      print("")
      print(cities)
