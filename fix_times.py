import pymongo

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.cta_db

db.cta_trains.aggregate([
    { "$addFields" : {
        "time": { '$dateFromString': {'dateString': '$tmst'} }
    }},
    { "$out": "cta_trains"}
])