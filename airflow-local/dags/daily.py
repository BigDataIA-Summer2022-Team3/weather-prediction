import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='get_weather_and_upload_dag',
    schedule_interval='0 5 * * *',
    start_date=datetime(2022, 8, 10),
    tags='Daily_read_weather',
) as dag:
    key_id = '',
    tdatetime = '',
    precipitation = 0.0,
    temp_max = 0.0,
    temp_min = 0.0,
    wind = 0.0,
    real_weather = ''

    def request_daily_data(ti):
        data = requests.get("https://damg-weather.herokuapp.com/today/weather").json() #fastapi url
        # data = requests.get("http://172.19.253.187:8000/today/weather").json() #fastapi url
        print(data)
        print('here####################################################')
        request_result = {}
        request_result['key_id'] = data['key_id']
        request_result['tdatetime'] = data['tdatetime']
        request_result['precipitation'] = data['precipitation']
        request_result['temp_max'] = data['temp_max']
        request_result['temp_min'] = data['temp_min']
        request_result['wind'] = data['wind']
        request_result['real_weather'] = data['real_weather']
        ti.xcom_push(key='request_result', value=request_result)
        print(request_result)


    def save_into_db(ti):
        request_result = ti.xcom_pull(task_ids='request_task', key='request_result')
        print(request_result)

        key_id = request_result['key_id'] 
        tdatetime = request_result['tdatetime']
        precipitation = request_result['precipitation']
        temp_max = request_result['temp_max']
        temp_min = request_result['temp_min']

        wind = request_result['wind'] 
        real_weather = request_result['real_weather']

        # print(type(key_id))
        
        testnum = requests.post(f"https://damg-weather.herokuapp.com/db/record/today?key_id={key_id}&tdatetime={tdatetime}&precipitation={precipitation}&temp_max={temp_max}&temp_min={temp_min}&wind={wind}&real_weather={real_weather}") #fastapi url
        # requests.get("http://172.19.253.187:8000/db/record/today?key_id={key_id}&tdatetime={tdatetime}&precipitation={precipitation}&temp_max={temp_max}&temp_min={temp_min}&wind={wind}&real_weather={real_weather}")
        print(testnum)
        print('############################################')

    request_task = PythonOperator(
        task_id="request_task",
        python_callable=request_daily_data
    )
    
    save_task = PythonOperator(
        task_id="save_task",
        python_callable=save_into_db
    )
    
    request_task >> save_task
    
    

