import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='get_weather_and_upload_dag',
    schedule_interval='58 22 * * *',
    start_date=datetime(2022, 8, 10),
    tags=['test'],
) as dag:
    key_id = '',
    tdatetime = '',
    precipitation = 0.0,
    temp_max = 0.0,
    temp_min = 0.0,
    wind = 0.0,
    real_weather = ''

    def request():
        data = requests.get("https://damg-weather.herokuapp.com/today/weather").json() #fastapi url
        # data = requests.get("http://172.19.253.187:8000/today/weather").json() #fastapi url
        print(data)
        print('here####################################################')
        key_id = data['key_id']
        tdatetime = data['tdatetime']
        precipitation = data['precipitation']
        temp_max = ['temp_max']
        temp_min = ['temp_min']
        wind = ['wind']
        real_weather = ['real_weather']


    def save():
        testnum = requests.get("https://damg-weather.herokuapp.com/db/record/today?key_id={key_id}&tdatetime={tdatetime}&precipitation={precipitation}&temp_max={temp_max}&temp_min={temp_min}&wind={wind}&real_weather={real_weather}") #fastapi url
        # requests.get("http://172.19.253.187:8000/db/record/today?key_id={key_id}&tdatetime={tdatetime}&precipitation={precipitation}&temp_max={temp_max}&temp_min={temp_min}&wind={wind}&real_weather={real_weather}")
        print(testnum)
        print('############################################')

    request_task = PythonOperator(
        task_id="request_task",
        python_callable=request
    )
    
    save_task = PythonOperator(
        task_id="save_task",
        python_callable=save
    )
    
    request_task >> save_task
    
    

