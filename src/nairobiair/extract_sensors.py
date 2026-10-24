##This task  will apply dynamic task mapping
import requests
from nairobiair.basic_setup import sensors_url, header
from nairobiair.logger import nairobiAir_logger

extract_sensor_logger = nairobiAir_logger()

##For testing purposes

# from nairobiair.extract_locations import location_extractor
# locations= location_extractor()

def sensor_extractor (location):
    location_id = location.get('id')
    try:
        actual_sensors_url = sensors_url.format(location_id = location_id)
        sensor_response = requests.get(actual_sensors_url,headers=header,timeout=30)
        sensor_response.raise_for_status()
        extract_sensor_logger.info("Sensor Data successfully extracted")
    except Exception as e:
        extract_sensor_logger.error(f"Sensor data has not successfully pulled due to err {e}")
        raise

    
    #sensors_list = pd.json_normalize(sensor_response.json()['results'])

    sensors_list = sensor_response.json()['results']
    return sensors_list


# trial = sensor_extractor(locations[0])
# print(trial)


