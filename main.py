import logging
from cta_api import CTA
from config import cta_api_key
import datetime as dt
import pymongo


logger = logging.getLogger('cta_train_collector')
fh = logging.FileHandler('cta_train_collector.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.cta_db

cta = CTA(cta_api_key)

while(True):
    response = cta.get_train_data()
    db.cta_raw_responses.insert_one(response)
    trains = cta.parse_train_response(response)
    db.cta_trains.insert_many(trains)
    print(f"{len(trains)} trains collected at {dt.datetime.now()}")
    sleep(5)