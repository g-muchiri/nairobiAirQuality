##This task will apply dynamic task mapping
import requests
import pandas as pd
from src.nairobiair.basic_setup import measurements_url, header, measurements_params
from src.nairobiair.logger import nairobiAir_logger

measurements_logger = nairobiAir_logger()

def measurements_extractor(sensors_id):
    try:
        actual_measurements_url = measurements_url.format(sensors_id = sensors_id)
        measurements_response = requests.get(actual_measurements_url, headers=header)
        measurements_response.raise_for_status
        if measurements_response.status_code == 200:
            measurements_logger.info("Measurements data has been successfully fetched")
        else:
            measurements_logger.info(f"Please note the status code is {measurements_response.status_code}")
    except Exception as e:
        measurements_logger.error(f"Measurement data has not been fetched due to error {e}")

    normalized_measurements =pd.json_normalize(measurements_response.json()['results'])

    return normalized_measurements

#msmt_trial = measurements_extractor(15427116)
#print(msmt_trial)