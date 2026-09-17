##This task  will apply dynamic task mapping
import pandas as pd
import requests
import json
from src.nairobiair.basic_setup import sensors_url, header
from src.nairobiair.logger import nairobiAir_logger

extract_sensor_logger = nairobiAir_logger()

def sensor_extractor (location_id: int):
    try:
        actual_sensors_url = sensors_url.format(location_id = location_id)
        sensor_response = requests.get(actual_sensors_url,headers=header)
        sensor_response.raise_for_status
        if sensor_response.status_code == 200:
            extract_sensor_logger.info("Sensor Data successfully extracted")
        else:
            extract_sensor_logger.info(f"Please note the status code for the above is{sensor_response.status_code}")
    except Exception as e:
        extract_sensor_logger.error(f"Sensor data has not successfully pulled due to err {e}")

    sensors_list = pd.json_normalize(sensor_response.json()['results'])
    return sensors_list


#trial = sensor_extractor(6237507)
#print(trial)


