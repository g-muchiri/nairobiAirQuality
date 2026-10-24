import os
from dotenv import load_dotenv

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

measurements_params = {    
    "limit":1000,
    "page":1
}



