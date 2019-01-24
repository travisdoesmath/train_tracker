import requests
import pymongo
from time import sleep
from config import cta_api_key

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.cta_db
collection = db.train_locations

while(True):
    response = requests.get(f'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={cta_api_key}&rt=red,blue,brn,org,p,pink,y&outputType=JSON').json()
    db.train_locations.insert_one(response)
    train_counts = [{'route':route['@name'], 'train_count':len(route['train'])} if 'train' in route.keys() else {'route':route['@name'],'train_count':0} for route in response['ctatt']['route']]
    print(response['ctatt']['tmst'], train_counts)
    sleep(5)