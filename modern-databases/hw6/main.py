from dotenv import dotenv_values
from mongo_client import MongoDBClient
from cli_client import CLISession

config = dotenv_values(".env")

if __name__ == "__main__":
  db_client = MongoDBClient(config['ATLAS_URI'], config['DB_NAME'])
  cli_client = CLISession(db_client)
