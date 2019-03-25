import logging
import requests
import datetime as dt

module_logger = logging.getLogger('cta_train_collector')

class CTA:
    def __init__(self, cta_api_key):
        self.logger = logging.getLogger('cta_train_collector.cta_api.CTA')
        self.logger.info('creating an instance of CTA')
        self.api_key = cta_api_key

    def parse_train_response(self, response):
        trains = []
        try:
            timestamp = response['ctatt']['tmst']
            time = parse(timestamp) 
            for route in response['ctatt']['route']:
                name = route['@name']
                if 'train' in route.keys():
                    if(type(route['train']) is dict):
                        route['train'] = [route['train']] # convert dict to singleton list
                    for train in route['train']:
                        train['line'] = name
                        train['tmst'] = timestamp
                        train['time'] = time
                        trains.append(train)
        except ValueError as e:
            self.logger.error(e)
        return trains

    def get_train_data(self):
        logging.basicConfig(filename="logfile")
        response = {}
        url = f'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={self.api_key}&rt=red,blue,brn,org,p,pink,y&outputType=JSON'
        try:
            response = requests.get(url).json()
        except requests.exceptions.RequestException as e:  
            logging.exception(e)
        except requests.exceptions.HTTPError as e:
            logging.exception(e)
        return response
