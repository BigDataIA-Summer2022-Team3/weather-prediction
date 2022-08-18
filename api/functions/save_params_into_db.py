import pymysql
from datetime import datetime as dt
from functions.dbconfig import funct
# from dbconfig import funct

def save_params_into_db(key_id, tdatetime, precipitation, temp_max, temp_min, wind, real_weather):
    # 上传数据到本地库
    Host, User, Password = funct()
    con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
    c = con.cursor()
    key_id = key_id + "-a"
    
    precipitation = float(precipitation)
    temp_max = float(temp_max)
    temp_min = float(temp_min)
    wind = float(wind)

    testreturn = -1

    sql = "insert into seattle_weather (id, date, precipitation, temp_max, temp_min, wind, real_weather)\
                values('%s','%s','%f','%f','%f','%f','%s')" % \
                (key_id, tdatetime, precipitation, temp_max, temp_min, wind, real_weather)

    try: 
        print("Prepare to insert...")
        c.execute(sql)
        testreturn = c.lastrowid
        con.commit() # 若操作为增删改则需要提交数据
        print("Inserted!")

    except:
        print("Something went wrong")
    finally:
        c.close()
        con.close()
        print(testreturn)
        return testreturn

utctimenow = dt.utcnow()
save_params_into_db('test02', utctimenow, 0.3, 27, 16, 10, 'clean')

