##This task will apply dynamic task mapping
import requests

from nairobiair.basic_setup import measurements_url, header, measurements_params
from nairobiair.logger import nairobiAir_logger

# ##For Testing purposes
# from nairobiair.extract_locations import location_extractor
# from nairobiair.extract_sensors import sensor_extractor

# locations= location_extractor()
# sensors = sensor_extractor(locations[0])

measurements_logger = nairobiAir_logger()

def measurements_extractor(sensor_data):
    sensors_id = sensor_data.get('id')
    try:
        actual_measurements_url = measurements_url.format(sensors_id = sensors_id)
        measurements_response = requests.get(actual_measurements_url, headers=header, timeout=30)
        # measurements_response.raise_for_status()
        if measurements_response.status_code == 200:
            measurements_logger.info("Measurements data has been successfully fetched")
        else:
            measurements_logger.info(f"Please note the status code is {measurements_response.status_code}")
    except Exception as e:
        measurements_logger.error(f"Measurement data has not been fetched due to error {e}")
        raise

   
    normalized_measurements =measurements_response.json()['results']
    
    return normalized_measurements

# msmt_trial = measurements_extractor(sensor_data=sensors[0])
# print(msmt_trial)
