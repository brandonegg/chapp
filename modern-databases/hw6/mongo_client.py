from pymongo import MongoClient

class MongoDBClient():
  def __init__(self, uri: str, db_name: str):
    mongodb_client = MongoClient(uri)
    self.database = mongodb_client[db_name]

  def find_nearest(self, lat_lon: tuple[float, float], limit: int):
    pass
