import requests
import json
from datetime import datetime

def get_today_weather_param():
    url = "https://api.openweathermap.org/data/3.0/onecall?lat=47&lon=-122&exclude=minutely,hourly,alerts,current&appid=ca71a8087da7cc4f650f5f104745c9d1&units=metric"
    data = requests.get(url).json()
    today = data['daily'][0]

    key_id = today['dt']
    tdatetime = datetime.fromtimestamp(today['dt'])

    precipitation = 0;
    if('rain' in today.keys()):
        precipitation = precipitation + today['rain']
    if('snow' in today.keys()):
        precipitation = precipitation + today['snow']

    temp_max = today['temp']['max']
    temp_min = today['temp']['min']
    wind = today['wind_speed']
    real_weather = today['weather'][0]['main']

    result = {}
    result['key_id'] = key_id;
    result['tdatetime'] = tdatetime
    result['precipitation'] = precipitation
    result['temp_max'] = temp_max
    result['temp_min'] = temp_min
    result['wind'] = wind
    result['real_weather'] = real_weather

    return result;

# today = get_today_weather_param()
# print(today)