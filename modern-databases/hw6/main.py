from dotenv import dotenv_values
from mongo_client import MongoDBClient
from cli_client import CLISession

config = dotenv_values(".env")

if __name__ == "__main__":
  if not 'ATLAS_URI' in config:
    print("Please supply a .env file with an ATLAS_URI value to connect to your MongoDB server")
    exit(-1)

  db_client = MongoDBClient(config['ATLAS_URI'], config['DB_NAME'])
  cli_client = CLISession(db_client)
