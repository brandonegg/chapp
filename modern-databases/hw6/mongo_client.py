from pymongo import MongoClient

class MongoDBClient():
  def __init__(self, uri: str, db_name: str):
    self.mongodb_client = MongoClient(uri)
    self.database = self.mongodb_client[db_name]

  def find_nearest(self, lat: float, lon: float):
    print("Here are the 3 nearest business to:")
    print(f"--- {lat}, {lon} ---")
    print("")
    
    limit = 3

    business_results = self.database['business'].find({
      "location": {
        "$near": {
			    "$geometry": { "type": "Point", "coordinates": [lon, lat]}
		    }
      }
    }, limit=limit)

    for i in business_results:
      print(i)

  def close(self):
    self.mongodb_client.close()
