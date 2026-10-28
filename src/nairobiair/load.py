from nairobiair.logger import nairobiAir_logger
from nairobiair.db_connection import connect_and_verify
from dotenv import load_dotenv
load_dotenv()
db_load_logger = nairobiAir_logger()

load_data_sql = """
INSERT INTO sensor_measurement_data(location_id, location_name, sensor_id, parameter_name,
parameter_units, value, loaded_timestamp) 
VALUES(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (sensor_id, parameter_units, loaded_timestamp)
DO NOTHING;
"""

##For trial purposes
##data_to_be_loaded = (7,'trial_name',2,'trial_param_name', 'trial_param_unit',67,'2026-10-28T07:57:00Z')

def load_data(data_to_be_loaded):
    rows_data = [rows for s in data_to_be_loaded for rows in s]
    rows = [
        (d["location_id"], d["location_name"], d["sensor_id"],
         d["parameter_name"], d["parameter_units"], d["value"],
         d["loaded_timestamp"])
        for d in rows_data
    ]
    conn = connect_and_verify()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(load_data_sql, rows)
        db_load_logger.info("data has been successfully loaded both cursor and connection closed")
    except Exception as e:
        db_load_logger.error(f"Could not load data due to error {e}")
        raise
    finally:
        conn.close()

#For Trial Purposes
#load_sample_data()
        