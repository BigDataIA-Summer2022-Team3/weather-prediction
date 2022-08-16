import pymysql
from datetime import datetime as dt
# from dbconfig import funct
from functions.dbconfig import funct

def save_params_into_db(id, tdatetime, precipitation, temp_max, temp_min, wind, real_weather):
    # 上传数据到本地库
    Host, User, Password = funct()
    con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
    c = con.cursor()
    id = id + "-a"
    
    precipitation = float(precipitation)
    temp_max = float(temp_max)
    temp_min = float(temp_min)
    wind = float(wind)

    sql = "insert into seattle_weather \
                values('%s','%s','%f','%f','%f','%f','%s')" % \
                (id, tdatetime, precipitation, temp_max, temp_min, wind, real_weather)
    try: 
        print("Prepare to do...")
        c.execute(sql)
        # print(c.fetchall())
        print("till now")
        con.commit() # 若操作为增删改则需要提交数据
        
    except:
        print("Something went wrong")
    finally:
        c.close()
        con.close()

# utctimenow = dt.datetime.utcnow()
# save_params_into_db('test01', utctimenow, 0.3, 27, 16, 10, 'clean')