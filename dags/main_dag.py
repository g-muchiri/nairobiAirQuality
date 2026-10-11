from datetime import timedelta, datetime, timezone
from airflow.sdk import dag, task, task_group
import os
from src.nairobiair.extract_locations import location_extractor
from src.nairobiair.extract_sensors import sensor_extractor
from src.nairobiair.extract_measurements import measurements_extractor
from src.nairobiair.logger import nairobiAir_logger

dag_logger = nairobiAir_logger()
requirements_path = os.path.join(os.path.dirname(__file__),"..","requirements.txt")

## We need to define a function to ensure all time is set to UTC
def to_utc(x:datetime):
    if hasattr(x, "in_timezone"):
        return x.in_timezone(timezone.utc)
    if x.tzinfo is None:
        return x.replace(tzinfo=timezone.utc)
    
@dag(dag_id = "Nairobi_air_quality",
     start_date = datetime(2026,1,1),
     schedule = "@daily",
     catchup = False
)
def nairobi_air_dag():
        
    @task
    def get_locations():
        try:
            locations = location_extractor()
            modified_location = [
                {"location_id":loc.get('id'),"location_name":loc.get('name')} 
                for loc in locations]
            dag_logger.info("Locations data has been fetched and modified")
            return modified_location
        
        except Exception as e:
            dag_logger.error(f"Location data has failed to load due to error {e}")
            raise

    @task
    def get_sensors(location: dict) -> list[dict]:
        try:
            sensors = sensor_extractor(location_id=location['location_id'])
            modified_sensors_data =[
                {"location_id":location["location_id"],
                 "location_name":location["location_name"],
                 "sensor_id":sensor['id'],
                 "parameter_name": sensor['parameter']['name'],
                 "parameter_units": sensor['parameter']['units']} 
            for sensor in sensors]
            dag_logger.info("sensors data has been successfully fetched and modified")

            return modified_sensors_data
        
        except Exception as f:
            dag_logger.error(f"Sensor data couldnt be fetched due to error {f}")
            raise
    @task
    def flatten_sensors(sensor_data: list[list[dict]]) -> list[dict]:
        final_sensor_data = [normalized_sensor_data for line1 in sensor_data for normalized_sensor_data in line1]
        return final_sensor_data


    @task
    def get_measurements(sensor: dict) -> list[dict]:
        try:
            measurements = measurements_extractor(sensor=sensor['id'])
            modified_measurements=[
                {"location_id":location["location_id"],
                 "location_name":location["location_name"],
                 "sensor_id":sensor['id'],
                 "parameter_name": sensor['parameter']['name'],
                 "parameter_units": sensor['parameter']['units'],
                 "value": measurements['value'],
                 "loaded_timestamp": measurements['coverage']['datetimeTo.utc']}
            ]
            dag_logger.info("Measurements data fetched and modified")

            super_modified_measurements = [measures for list1 in modified_measurements for measures in list1]

            return super_modified_measurements
        
        except Exception as g:
            dag_logger.error(f"Measurements data could not fetch due to error {g}")
            raise

    locale= get_locations()
    actual_sensors = get_sensors.expand(location=locale)
    flattenned_sensor_data = flatten_sensors(actual_sensors)
    actual_measurements = get_measurements.expand(sensor=flattenned_sensor_data)
    print(actual_measurements)
nairobi_air_dag()