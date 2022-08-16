import requests
'''
API 1 预测天气: 访问open API获取气象信息，将数据输入模型进行预测天气，返回降雨量，最高温，最低温，风速和预测的天气，没有输入参数

API 2 过去7天的天气：读取MySQL数据，并返回，没有输入参数

API 3 过去7天的降雨：读取MySQL数据，并返回，没有输入参数

API 4 每日读取open api：访问open API获取气象信息，上传到MySQL，没有输入参数

Note：API 1在notebook里；API 4的数据筛选与1相似，上传到MySQL的部分在notebook里也有；API 2和3筛选出前7天数据的代码也在notebook里
'''
def get_past_weather_param():
    url = "https://api.openweathermap.org/data/3.0/onecall?lat=47&lon=-122&exclude=minutely,hourly,alerts&appid=ca71a8087da7cc4f650f5f104745c9d1"
    data = requests.get(url)
    return data
