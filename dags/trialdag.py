from airflow.sdk import dag, task
from datetime import datetime


@dag(
    dag_id="170926",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example", "week4"]
)
def my_first_dag():

    @task
    def extract():
        print("Extracting data...")
        
    @task
    def transform(data: dict):
        print(f"Transforming ")
        

    @task
    def load(data: dict):
        print(f"Loading ")

    # Define dependencies using >> operator
    raw_data = extract()
    clean_data = transform(raw_data)
    load(clean_data)


# Instantiate the DAG
my_first_dag()