import requests
import pymongo
from time import sleep
from config import cta_api_key

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.cta_db
collection = db.train_locations

def parse_response_to_trains(response):
    timestamp = response['ctatt']['tmst']
    trains = []
    for route in response['ctatt']['route']:
        name = route['@name']
        if 'train' in route.keys():
            if(type(route['train']) is dict):
                route['train'] = [route['train']] # convert dict to singleton list
            for train in route['train']:
                train['line'] = name
                train['tmst'] = timestamp
                trains.append(train)
    return trains

while(True):
    response = requests.get(f'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={cta_api_key}&rt=red,blue,brn,org,p,pink,y&outputType=JSON').json()
    if(response['ctatt']['errCd'] != '0'):
        db.api_errors.insert_one(response)
    else:
        trains = parse_response_to_trains(response)
        db.train_locations.insert_many(trains)
    train_counts = [{'route':route['@name'], 'train_count':len(route['train'])} if 'train' in route.keys() else {'route':route['@name'],'train_count':0} for route in response['ctatt']['route']]
    print(response['ctatt']['tmst'], train_counts)
    sleep(5)