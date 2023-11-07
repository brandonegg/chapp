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

  def write_review(self, id: str, score: int):
    if not score in [str(i) for i in range(0, 6)]:
      print("Invalid score value. Score must be an integer between 0 and 5")
      return
    
    score_int = int(score)

    business = self.database['business'].find_one({"business_id": id})
    if (business is None):
      print("No business found with the provided ID")
      return

    new_stars = (business['stars'] * business['review_count'] + score_int) / (business['review_count'] + 1)

    self.database['business'].update_one({"business_id": id}, {
      '$set': {
        'review_count': business['review_count'] + 1,
        'stars': new_stars,
      }
    })

    self.database['reviews'].insert_one({
      'business_id': id,
      'score': score_int,
    })

    print("Review successfully added!")
    print(f"New business rating for {id} is {new_stars} stars")

  def close(self):
    self.mongodb_client.close()
