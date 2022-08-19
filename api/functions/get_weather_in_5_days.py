import requests

from functions.predict_weather import predict_weather
# from predict_weather import predict_weather

def get_weather_in_5_days(lat:int= None, lon:int= None, ):
    def_lat = 47
    def_lon = -122
    lat = def_lat if lat is None else lat
    lon = def_lon if lon is None else lon

    appid = 'ca71a8087da7cc4f650f5f104745c9d1'
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts,current&appid={appid}&units=metric"
    raw_data = requests.get(url).json()['daily'][1:6]

    params, input_list = [], []

    for i in range(len(raw_data)):
        temp = {} 
        if('rain' in raw_data[i].keys()):
            temp['precipitation'] = raw_data[i]['rain']
            list.app(raw_data[i]['rain'])
        elif('snow' in raw_data[i].keys()):
            temp['precipitation'] = raw_data[i]['snow']
        else: 
            temp['precipitation'] = 0

        temp['temp_max'] = raw_data[i]['temp']['max']
        temp['temp_min'] = raw_data[i]['temp']['min']
        temp['wind'] = raw_data[i]['wind_speed']        
        params.append(temp)
        input_list.append([temp['precipitation'], temp['temp_max'], temp['temp_min'], temp['wind']])

        i+=1

    predict_list = predict_weather(input_list)

    result = {}
    result['raw_data'] = raw_data
    result['params'] = params
    result["predict_weather"] = predict_list
    return result
