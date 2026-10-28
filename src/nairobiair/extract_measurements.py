##This task will apply dynamic task mapping
import requests
from datetime import datetime, timedelta, timezone, time
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

def measurements_extractor(sensor_data, datetime_from: str | None = None, datetime_to: str|None = None, max_pages = 50, limit = 1000):
    sensors_id = sensor_data.get('sensor_id')
    if (datetime_from is None) != (datetime_to is None):
        raise ValueError("Please pass both date_from and date_to or none at all")
    if (datetime_from is None) and (datetime_to is None):
        datetime_from, datetime_to = yesterday_window_utc()

    all_results = []
    page = 1

    while page <= max_pages:
        current_params = dict(measurements_params)
        current_params['datetime_from'] = datetime_from
        current_params['datetime_to'] = datetime_to
        current_params['page']= page
        try:
            actual_measurements_url = measurements_url.format(sensors_id = sensors_id)
            measurements_response = requests.get(actual_measurements_url, headers=header, timeout=30, params=current_params)
            measurements_response.raise_for_status()

            normalized_measurements =measurements_response.json()['results']
            all_results.extend(normalized_measurements)
            measurements_logger.info(f"Our first Run has a length of {len(all_results)}")

            if len(all_results)<= limit:
                measurements_logger.info("We have fetched all results")
                break
            else:
                page += 1
                time.sleep(0.5)

            measurements_logger.info(f'Fetched {len(normalized_measurements)} measurements for sensor_id {sensors_id} from {datetime_from} to {datetime_to}')
        except Exception as e:
            measurements_logger.error(f"Measurement data has not been fetched due to error {e}")
            raise
    else:
        measurements_logger.warning(f"We have hit the maximum pages. Please confirm if you have more data")
            
    return all_results

# msmt_trial = measurements_extractor(sensor_data=sensors[0])
# print(msmt_trial)
