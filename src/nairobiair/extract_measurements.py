##This task will apply dynamic task mapping
import requests
from datetime import datetime, timedelta, timezone
from nairobiair.basic_setup import measurements_url, header, measurements_params
from nairobiair.logger import nairobiAir_logger

# ##For Testing purposes
# from nairobiair.extract_locations import location_extractor
# from nairobiair.extract_sensors import sensor_extractor

# locations= location_extractor()
# sensors = sensor_extractor(locations[0])

measurements_logger = nairobiAir_logger()

ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"

def yesterday_window_utc()-> tuple[str, str]:
    today = datetime.now(timezone.utc).replace(hour=0,minute=0, second=0, microsecond=0)
    start = today - timedelta(days=1)
    stop = today - timedelta(seconds=1)
    return start.strftime(ISO_FMT), stop.strftime(ISO_FMT)

def measurements_extractor(sensor_data, date_from: str | None = None, date_to: str|None = None):
    sensors_id = sensor_data.get('id')
    if (date_from is None) != (date_to is None):
        raise ValueError("Please pass both date_from and date_to or none at all")
    if (date_from is None) and (date_to is None):
        date_from, date_to = yesterday_window_utc()

    current_params = dict(measurements_params)
    current_params['datetime_from'] = date_from
    current_params['datetime_to'] = date_to
    try:
        actual_measurements_url = measurements_url.format(sensors_id = sensors_id)
        measurements_response = requests.get(actual_measurements_url, headers=header, timeout=30, params=current_params)
        measurements_response.raise_for_status()
    except Exception as e:
        measurements_logger.error(f"Measurement data has not been fetched due to error {e}")
        raise

   
    normalized_measurements =measurements_response.json()['results']
    
    return normalized_measurements

# msmt_trial = measurements_extractor(sensor_data=sensors[0])
# print(msmt_trial)
