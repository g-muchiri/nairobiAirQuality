from nairobiair.logger import nairobiAir_logger
import psycopg2
import os
from dotenv import load_dotenv
### Load_dotenv withoverride = true is used to kind of Decache after cahnging variables 
#Pertinent to connection in .env

load_dotenv(override=True)

##load_dotenv()
db_logger = nairobiAir_logger()

# DATABASE_NAME = os.getenv('DATABASE_NAME')
# DATABASE_USER = os.getenv('DATABASE_USER')
# DATABASE_HOST = os.getenv('DATABASE_HOST')
# DATABASE_PORT = os.getenv('DATABASE_PORT')
# DATABASE_PASSWORD =os.getenv('DATABASE_PASSWORD')

def connect_and_verify():
    try:
        DATABASE_NAME = os.getenv('DATABASE_NAME')
        DATABASE_USER = os.getenv('DATABASE_USER')
        DATABASE_HOST = os.getenv('DATABASE_HOST')
        DATABASE_PORT = os.getenv('DATABASE_PORT')
        DATABASE_PASSWORD =os.getenv('DATABASE_PASSWORD')
        conn = psycopg2.connect(database = DATABASE_NAME,user =  DATABASE_USER, 
                                host = DATABASE_HOST, port= DATABASE_PORT, password =DATABASE_PASSWORD)
        db_logger.info("database has successfully logged")
        return conn
    except psycopg2.DatabaseError:
        db_logger.error("Permision denied. Please check your credentials or syntax errors")
        conn.close()
        raise
    except psycopg2.InterfaceError:
        db_logger.error("Please check whether your connection is open")
        conn.close()
        raise
    except psycopg2.OperationalError:
        db_logger.error("The network or server seems to have a problem, please try again later")
        conn.close()
        raise
    except Exception as e:
        db_logger.error(f"The database connection is not successful {e}")
        conn.close()
        raise
