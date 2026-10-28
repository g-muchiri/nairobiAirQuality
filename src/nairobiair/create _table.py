from nairobiair.db_connection import connect_and_verify

##This file was meant to be ran just once

## Create a cursor object that executes querries
create_sensor_table = """CREATE TABLE IF NOT EXISTS sensor_measurement_data(
entry_id serial PRIMARY KEY,
location_id int NOT NULL,
location_name varchar(100) NOT NULL,
sensor_id int NOT NULL,
parameter_name varchar(100),
parameter_units varchar(100),
value varchar(100),
loaded_timestamp timestamp,

CONSTRAINT idempotency_proof UNIQUE (sensor_id,parameter_units, loaded_timestamp)

);"""

## The command below helps that one may not have errors while creating a database
##conn.autocommit = True

## It is best practise to leave it as false and only turn it on when creating DB, Creating Indices and when altering types



def create_sensor_table_sql():
    conn = connect_and_verify()
    cursor = conn.cursor()
    try:
        cursor.execute(create_sensor_table)
        conn.commit()
        cursor.close()
        conn.close()

        db_logger.info("Table Successfully created")
    except Exception as e:
        db_logger.error(f"sensor table not created due to error {e}")
        raise
    finally:
        cursor.close()
        conn.close()

create_sensor_table_sql()