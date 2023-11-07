from pymongo import MongoClient

class MongoDBClient():
  def __init__(self, uri: str, db_name: str):
    self.mongodb_client = MongoClient(uri)
    self.database = self.mongodb_client[db_name]

  def find_nearest(self, lat: float, lon: float):
    try:
      lat_float = float(lat)
      lon_float = float(lon)
    except:
      print("Error: Invalid latitude or longitude value(s). Inputs must be valid floating point numbers!")
      return
      

    print("Here are the 3 nearest business to:")
    print(f"--- {lat}, {lon} ---")
    print("")
    
    limit = 3

    business_results = self.database['business'].find({
      "location": {
        "$near": {
			    "$geometry": { "type": "Point", "coordinates": [lon_float, lat_float]}
		    }
      }
    }, {
      "_id": 0,
      "name": 1,
      "address": 1,
      "city": 1,
      "state": 1,
      "categories": 1,
      "stars": 1,
      "review_count": 1,
    }, limit=limit)

    for i in business_results:
      print(i)
      print("")

  def close(self):
    self.mongodb_client.close()
