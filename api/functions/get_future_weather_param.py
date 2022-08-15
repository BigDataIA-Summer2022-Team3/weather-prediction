import requests

def get_future_weather_param():
    url = "https://api.openweathermap.org/data/3.0/onecall?lat=47&lon=-122&exclude=minutely,hourly,alerts&appid=ca71a8087da7cc4f650f5f104745c9d1"
    data = requests.get(url)
    return data
