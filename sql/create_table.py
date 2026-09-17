from nairobiair.logger import nairobiAir_logger
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
db_logger = nairobiAir_logger()

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_PASSWORD =os.getenv('DATABASE_PASSWORD')

try:
    conn = psycopg2.connect(database = DATABASE_NAME,user =  DATABASE_USER, 
                            host = DATABASE_HOST, port= DATABASE_PORT, password =DATABASE_PASSWORD)
    db_logger.info("database has successfully logged")
except psycopg2.DatabaseError:
    db_logger.error("Permision denied. Please check your credentials or syntax errors")
    raise
except psycopg2.InterfaceError:
    db_logger.error("Please check whether your connection is open")
    raise
except psycopg2.OperationalError:
    db_logger.error("The network or server seems to have a problem, please try again later")
    raise
except Exception:
    db_logger.error("The database connection is not successful")




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
cursor = conn.cursor()


def create_sensor_table_sql():
    try:
        cursor.execute(create_sensor_table)
        conn.commit()
        cursor.close()
        conn.close()

        db_logger.info("Table Successfully created")
    except Exception as e:
        db_logger.error(f"sensor table not created due to error {e}")
        raise

create_sensor_table_sql()