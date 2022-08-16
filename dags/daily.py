import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='get_weather_and_upload_dag',
    schedule_interval='0 5 * * *',
    start_date=datetime(2022, 8, 10),
    tags=['test'],
) as dag:
    def request():
        requests.get("") #fastapi url
    

    def save():
        requests.get("") #fastapi url
    
    
    request_task = PythonOperator(
        task_id="request_task",
        python_callable=request
    )
    
    save_task = PythonOperator(
        task_id="save_task",
        python_callable=save
    )
    
    request_task >> save_task
    
    

