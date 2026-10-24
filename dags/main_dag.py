from datetime import datetime, timezone #,timedelta
from airflow.sdk import dag, task
import os
from nairobiair.extract_locations import location_extractor
from nairobiair.extract_sensors import sensor_extractor
from nairobiair.extract_measurements import measurements_extractor
from nairobiair.logger import nairobiAir_logger

dag_logger = nairobiAir_logger()
requirements_path = os.path.join(os.path.dirname(__file__),"..","requirements.txt")

## We need to define a function to ensure all time is set to UTC
# def to_utc(x:datetime):
#     if hasattr(x, "in_timezone"):
#         return x.in_timezone(timezone.utc)
#     if x.tzinfo is None:
#         return x.replace(tzinfo=timezone.utc)
    
@dag(dag_id = "nairobi_air_quality",
     start_date = datetime(2026,1,1, tzinfo=timezone.utc),
     schedule = "@daily",
     catchup = False
)
def nairobi_air_dag():
        
    @task
    def get_locations():
        try:
            locations = location_extractor()
            dag_logger.info("Locations data has been fetched successfully")
            return locations
        except Exception as e:
            dag_logger.error(f"Location data has failed to load due to error {e}")
            raise

    @task #This one here will use dynamic task mapping
    def get_sensors(location: dict) -> list[dict]:
        try:
            sensors = sensor_extractor(location_id=location)
            sensor_data =[
                {"location_id":location.get('id'),
                 "location_name":location.get('name'),
                 "sensor_id":sensor.get('id'),
                 "parameter_name": sensor.get('parameter',{}).get('name'),
                 "parameter_units": sensor.get('parameter',{}).get('units')} 
            for sensor in sensors]
            dag_logger.info("sensors data has been successfully fetched and modified")

            return sensor_data
        
        except Exception as f:
            dag_logger.error(f"Sensor data couldnt be fetched due to error {f}")
            raise
    # The above will return a dictionary of sensors as a list for each location id
    # Its therefore important to flatten the list[list[dict]]
    # this informs the next task

    @task
    def flattening_sensors(sensor_not_flattened: list[list[dict]]) -> list[dict]:
       return [flattened_sensors for location in sensor_not_flattened for flattened_sensors in location]
    
    @task
    def get_measurements(sensor: dict) -> list[dict]:
        try:
            measurements = measurements_extractor(sensor)
            recorded_measurements=[
                {"location_id":sensor["location_id"],
                 "location_name":sensor["location_name"],
                 "sensor_id":sensor['sensor_id'],
                 "parameter_name": sensor['parameter_name'],
                 "parameter_units": sensor['parameter_units'],
                 "value": measure.get('value'),
                 "loaded_timestamp": measure.get('period',{}).get('datetimeTo',{}).get('utc')
                 }
            for measure in (measurements or [])
            ]
            dag_logger.info("Measurements data fetched and modified")

            return recorded_measurements
        
        except Exception as g:
            dag_logger.error(f"Measurements data could not fetch due to error {g}")
            raise
    

    locations= get_locations()
    nested_sensors = get_sensors.expand(location=locations)
    flattened_sensors = flattening_sensors(nested_sensors)
    measurements = get_measurements.expand(sensor=flattened_sensors)
    
nairobi_air_dag()