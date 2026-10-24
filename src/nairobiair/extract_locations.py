import requests
from nairobiair.basic_setup import location_url, header, extract_params
from nairobiair.logger import nairobiAir_logger

extract_location_logger = nairobiAir_logger()
def location_extractor():
    try:
        location_response = requests.get(location_url, params=extract_params, headers=header, timeout=30)
        location_response.raise_for_status()
        if location_response.status_code == 200:
            extract_location_logger.info("Location data successfully extracted")
        else:
            extract_location_logger.info(f"The status code is {location_response.status_code}")
    except Exception as e:
        extract_location_logger.error(f"Data has not fetched from the API due to error {e}")
        raise

    return location_response.json()['results']

# trial1=location_extractor()
# print(trial1)
#print(trial1[0].get('id'))




