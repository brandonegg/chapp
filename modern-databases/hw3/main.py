from exceptions import InvalidCredentialFileException
from pg_client import PGClient
from psycopg2 import OperationalError
from cli_client import CLISession

CREDENTIALS_PATH = './credentials.txt'
DB_NAME = 'mdb_student06'
DB_ADDR = 's-l112.engr.uiowa.edu'
DB_PORT = '5432'

def run():
  pg_client = PGClient(CREDENTIALS_PATH, DB_ADDR, DB_PORT, DB_NAME)
  print("PostgreSQL database connection established successfully!")
  CLISession(pg_client)

if __name__ == '__main__':
  try:
    run()
  except (FileNotFoundError, IOError):
    print(f"The file {CREDENTIALS_PATH} does not exist or is corrupted.")
  except InvalidCredentialFileException:
    print("The credential file provided is invalid. There should be two lines, the first being a username and second being a password.")
  except OperationalError as e:
    print("PostgreSQL operation failed:")
    print(e)
