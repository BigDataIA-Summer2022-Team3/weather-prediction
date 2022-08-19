import streamlit as st
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from datetime import datetime
import streamlit_authenticator as stauth
import requests
import time

usernames = ["zhijie", "yijun", "team4", "parth", "srikanth"]

file_path = Path(__file__).parent.parent / "streamlitUserPW.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, "Login", "abcdef", cookie_expiry_days=0)


if st.session_state["authentication_status"]:
    token = st.session_state["token"] 
    # st.warning("token: " + token) # Debug
    username = st.session_state["name"]
    # st.warning("username: " + username)


    header = {"Authorization": "Bearer "+ token, "accept": "application/json"}

    authenticator.logout('Logout', 'sidebar')

    st.sidebar.markdown("## Function Page")

    def api1():
        st.header("Function 1: Predict next 5 days Weather")
        # st.sidebar.subheader("Predict Weather")
        if st.button("predict"):
            st.write('function 1')
            # run function
            url = "https://damg-weather.herokuapp.com/predict/5days"
            res = requests.get(url=url, headers = header)
            meta = res.json()
            #st.write(meta)

            weather_arr = []
            for w in meta['predict_weather']:
                if(w==0):
                    weather_arr.append("Drizzle")
                elif(w==1):
                    weather_arr.append("Fog")
                elif(w==2):
                    weather_arr.append("Rain")
                elif(w==3):
                    weather_arr.append("snow")
                else:
                    weather_arr.append("Sun")

            date_col = ['day1','day2','day3','day4','day5']
            prcp = []
            temp_max = []
            temp_min = []
            wind = []

            prcp_num = 0.0

            for line in meta['params']:
                prcp.append(line['precipitation'])
                prcp_num = prcp_num + float(line['precipitation'])
                temp_max.append(line['temp_max'])
                temp_min.append(line['temp_min'])
                wind.append(line['wind'])

            data = {
                'precipitation(mm)': prcp,
                'temp_max(C)': temp_max,
                'temp_min(C)': temp_min,
                'wind(m/s)': wind,
                'weather': weather_arr
            }
            datadf = pd.DataFrame(data)

            st.write(datadf)

            # temp graph
            st.markdown('## Temp')
            temp_df = pd.DataFrame({
                'date': date_col,
                'max_temp(C)': temp_max,
                'min_temp(C)': temp_min
                })
            temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
            st.line_chart(temp_df)

            # prcp graph
            if(prcp_num != 0):
                st.markdown('## Prcp')
                prcp_df = pd.DataFrame({
                    'date': date_col,
                    'precipitation(mm)': prcp
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

            # wind graph
            st.markdown('## wind')
            wind_df = pd.DataFrame({
                'date': date_col,
                'wind(m/s)': wind
                })
            wind_df = wind_df.rename(columns={'date':'index'}).set_index('index')
            st.line_chart(wind_df)

            

    def api2():
        st.header("Function 2: Meteorological data in the past 7 days")
        if st.button("Select"):
            url = "https://damg-weather.herokuapp.com/last7days/weather"
            res = requests.get(url=url, headers = header)
            meta = res.json()

            # st.write(meta)

            date_col = []
            day_prcp = []
            day_max = []
            day_min = []
            day_wind = []

            prcp_num = 0

            for daily in meta:
                date_col.append(daily[0].split('T')[0])
                day_prcp.append(daily[1])
                prcp_num = prcp_num + float(daily[1])
                day_max.append(daily[2])
                day_min.append(daily[3])
                day_wind.append(daily[4])

            # st.write(date_col)
            # st.write(type(date_col))

            # temp graph
            st.markdown('## Temp')
            temp_df = pd.DataFrame({
                'date': date_col,
                'max_temp(C)': day_max,
                'min_temp(C)': day_min
                })
            temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
            st.line_chart(temp_df)

            # prcp graph
            if(prcp_num != 0):
                st.markdown('## Precipitation')
                prcp_df = pd.DataFrame({
                    'date': date_col,
                    'precipitation(mm)': day_prcp
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

            # wind graph
            st.markdown('## Average wind speed')
            wind_df = pd.DataFrame({
                'date': date_col,
                'wind(m/s)': day_wind
                })
            wind_df = wind_df.rename(columns={'date':'index'}).set_index('index')
            st.line_chart(wind_df)
            


    def api3():
        st.header("Function 3: Past data search")
        input_year = st.selectbox(
            'Please choose a year',
            (2015, 2016, 2017, 2018, 2019, 2020,2021, 2022))
        if st.button("Select"):
            # run function
            url = f"https://damg-weather.herokuapp.com/history?input_year={input_year}"
            res = requests.get(url=url, headers = header)
            meta = res.json()
            # st.write(meta)

            m1 = []
            m2 = []
            m3 = []
            m4 = []
            m5 = []
            m6 = []
            m7 = []
            m8 = []
            m9 = []
            m10 = []
            m11 = []
            m12 = []
            month_arr = []

            for daily in meta:
                if daily[1] == '01':
                    m1.append(daily)
                elif daily[1] == '02':
                    m2.append(daily)
                elif daily[1] == '03':
                    m3.append(daily)
                elif daily[1] == '04':
                    m4.append(daily)
                elif daily[1] == '05':
                    m5.append(daily)
                elif daily[1] == '06':
                    m6.append(daily)
                elif daily[1] == '07':
                    m7.append(daily)
                elif daily[1] == '08':
                    m8.append(daily)
                elif daily[1] == '09':
                    m9.append(daily)
                elif daily[1] == '10':
                    m10.append(daily)
                elif daily[1] == '11':
                    m11.append(daily)
                elif daily[1] == '12':
                    m12.append(daily)

            monthes = [m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12]
            for month in monthes:
                date_col = []
                day_prcp = []
                day_max = []
                day_min = []
                # day_wind = []

                avhtemp = 0
                hesttemp = 0
                avltemp = 0
                lesttemp = 99
                totalprcp = 0
                daycount = 0
                for day in month:
                    daycount = daycount + 1
                    date_col.append(day[0])
                    day_prcp.append(day[2])
                    totalprcp = totalprcp + day[2]
                    day_max.append(day[3])
                    avhtemp = avhtemp + day[3]
                    if(day[3]>hesttemp):
                        hesttemp = day[3]
                    day_min.append(day[4])
                    avltemp = avltemp + day[4]
                    if(day[4]<lesttemp):
                        lesttemp = day[4]
                    # day_wind.append(daily[5])
                # data = {'date':date_col, 'prcp':day_prcp, 'temp_max':day_max, 'temp_min':day_min, 'wind':day_wind}
                data = {'date':date_col, 'prcp':day_prcp, 'temp_max':day_max, 'temp_min':day_min,
                        'ave_htemp':round(avhtemp/daycount,2), 'ave_ltemp':round(avltemp/daycount,2),
                        'totalprcp':round(totalprcp,2), 'hesttemp':round(hesttemp,2), 'lesttemp':round(lesttemp,2)}

                month_arr.append(data)

            # temp graph
            st.markdown('## Monthly Meteorological data graph')

            if(m1 != []):
                st.markdown('## January')
                st.markdown('### Temp')

                temp_df = pd.DataFrame({
                    'date': month_arr[0]['date'],
                    'max_temp(C)': month_arr[0]['temp_max'],
                    'min_temp(C)': month_arr[0]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[0]['date'],
                    'precipitation(mm)': month_arr[0]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[0]['hesttemp']) + '°C and the lowest is ' + str(month_arr[0]['lesttemp']) + '°C.')
                st.write('The average higest temperature is ' + str(month_arr[0]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[0]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[0]['totalprcp']) + 'mm.')

            
            if(m2 != []):
                st.markdown('## February')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[1]['date'],
                    'max_temp(C)': month_arr[1]['temp_max'],
                    'min_temp(C)': month_arr[1]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[1]['date'],
                    'precipitation(mm)': month_arr[1]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[1]['hesttemp']) + '°C and the lowest is ' + str(month_arr[1]['lesttemp']) + '°C.')
                st.write('The average higest temperature is ' + str(month_arr[1]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[1]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[1]['totalprcp']) + 'mm.')


            if(m3 != []):
                st.markdown('## March')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[2]['date'],
                    'max_temp(C)': month_arr[2]['temp_max'],
                    'min_temp(C)': month_arr[2]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[2]['date'],
                    'precipitation(mm)': month_arr[2]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[2]['hesttemp']) + '°C and the lowest is ' + str(month_arr[2]['lesttemp']) + '°C.')
                st.write('The average higest temperature is ' + str(month_arr[2]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[2]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[2]['totalprcp']) + 'mm.')


            if(m4 != []):
                st.markdown('## April')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[3]['date'],
                    'max_temp(C)': month_arr[3]['temp_max'],
                    'min_temp(C)': month_arr[3]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[3]['date'],
                    'precipitation(mm)': month_arr[3]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[3]['hesttemp']) + '°C and the lowest is ' + str(month_arr[3]['lesttemp']) + '°C.')
                st.write('The average higest temperature is ' + str(month_arr[3]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[3]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[3]['totalprcp']) + 'mm.')


            if(m5 != []):
                st.markdown('## May')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[4]['date'],
                    'max_temp(C)': month_arr[4]['temp_max'],
                    'min_temp(C)': month_arr[4]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[4]['date'],
                    'precipitation(mm)': month_arr[4]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[4]['hesttemp']) + '°C and the lowest is ' + str(month_arr[4]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[4]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[4]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[4]['totalprcp']) + 'mm.')


            if(m6 != []):
                st.markdown('## June')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[5]['date'],
                    'max_temp(C)': month_arr[5]['temp_max'],
                    'min_temp(C)': month_arr[5]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[5]['date'],
                    'precipitation(mm)': month_arr[5]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[5]['hesttemp']) + '°C and the lowest is ' + str(month_arr[5]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[5]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[5]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[5]['totalprcp']) + 'mm.')


            if(m7 != []):
                st.markdown('## July')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[6]['date'],
                    'max_temp(C)': month_arr[6]['temp_max'],
                    'min_temp(C)': month_arr[6]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[6]['date'],
                    'precipitation(mm)': month_arr[6]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[6]['hesttemp']) + '°C and the lowest is ' + str(month_arr[6]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[6]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[6]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[6]['totalprcp']) + 'mm.')


            if(m8 != []):
                st.markdown('## August')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[7]['date'],
                    'max_temp(C)': month_arr[7]['temp_max'],
                    'min_temp(C)': month_arr[7]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[7]['date'],
                    'precipitation(mm)': month_arr[7]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[7]['hesttemp']) + '°C and the lowest is ' + str(month_arr[7]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[7]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[7]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[7]['totalprcp']) + 'mm.')


            if(m9 != []):
                st.markdown('## September')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[8]['date'],
                    'max_temp(C)': month_arr[8]['temp_max'],
                    'min_temp(C)': month_arr[8]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[8]['date'],
                    'precipitation(mm)': month_arr[8]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[8]['hesttemp']) + '°C and the lowest is ' + str(month_arr[8]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[8]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[8]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[8]['totalprcp']) + 'mm.')


            if(m10 != []):
                st.markdown('## October')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[9]['date'],
                    'max_temp(C)': month_arr[9]['temp_max'],
                    'min_temp(C)': month_arr[9]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[9]['date'],
                    'precipitation(mm)': month_arr[9]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[9]['hesttemp']) + '°C and the lowest is ' + str(month_arr[9]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[9]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[9]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[9]['totalprcp']) + 'mm.')


            if(m11 != []):
                st.markdown('## November')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[10]['date'],
                    'max_temp(C)': month_arr[10]['temp_max'],
                    'min_temp(C)': month_arr[10]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[10]['date'],
                    'precipitation(mm)': month_arr[10]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[10]['hesttemp']) + '°C and the lowest is ' + str(month_arr[10]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[10]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[10]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[10]['totalprcp']) + 'mm.')


            if(m12 != []):
                st.markdown('## December')
                st.markdown('### Temp')
                temp_df = pd.DataFrame({
                    'date': month_arr[11]['date'],
                    'max_temp(C)': month_arr[11]['temp_max'],
                    'min_temp(C)': month_arr[11]['temp_min']
                    })
                temp_df = temp_df.rename(columns={'date':'index'}).set_index('index')
                st.line_chart(temp_df)

                st.markdown('### Precipitation')
                prcp_df = pd.DataFrame({
                    'date': month_arr[11]['date'],
                    'precipitation(mm)': month_arr[11]['prcp']
                    })
                prcp_df = prcp_df.rename(columns={'date':'index'}).set_index('index')
                st.bar_chart(prcp_df)

                st.write('This month highest temperature is ' + str(month_arr[11]['hesttemp']) + '°C and the lowest is ' + str(month_arr[11]['lesttemp']) + '°C.')
                st.write('The average highest temperature is ' + str(month_arr[11]['ave_htemp']) + '°C and the average lowest is ' + str(month_arr[11]['ave_ltemp']) + '°C.')
                st.write('The total precipitation is ' + str(month_arr[11]['totalprcp']) + 'mm.')            

    
    funNum = {
        "API 1: Predict next 5 days Weather": api1,
        "API 2: Meteorological data": api2,
        "API 3: Past data search": api3
    }

    selectFun = st.sidebar.selectbox("choose function", funNum.keys())
    funNum[selectFun]()
else:
    st.markdown('# Please login first')