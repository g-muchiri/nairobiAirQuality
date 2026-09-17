import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

base_url = os.getenv('BASE_URL')

my_key  = os.getenv('API_KEY')

location_url = f'{base_url}/locations'

sensors_url = f"{base_url}/locations/{{location_id}}/sensors"

measurements_url = f"{base_url}/sensors/{{sensors_id}}/measurements"


header = {
    "X-API-Key": my_key
}
extract_params = {
    "coordinates":"-1.278560,36.821249",
    "radius":25000,
    "limit":1000
}
yesterday = datetime.now() - timedelta(days=1)
date_from = datetime(yesterday.year, 1, 1, 0, 0, 0)
date_to = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59,59)


measurements_params = {
    "datetime_from":date_from,
    "datetime_to":date_to,
    "limit":1000,
    "page":1
}



