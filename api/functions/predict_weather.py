import pickle

model = pickle.load(open('functions/weather_model.pkl', 'rb'))

def predict_weather(input_list:list):
    try:
        # tmp = [[0, 26.64, 16.11, 2.94]]
        # print(type(tmp))
        result_list = model.predict(input_list).tolist()
        # result_list = model.predict(input_list)
    except Exception as e:
        print(e)
        return "Failed to Infer with this input "
    # finally:
        # print(result_list)
    return result_list

