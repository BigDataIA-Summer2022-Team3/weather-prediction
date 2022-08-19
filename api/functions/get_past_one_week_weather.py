import pymysql

from functions.dbconfig import funct
# from dbconfig import funct

'''
'''
def get_past_one_week_weather():
    Host, User, Password = funct()
    con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
    c = con.cursor()
    
    sql = "select date, precipitation, temp_max, temp_min, wind, real_weather \
        from seattle_weather \
        where date_sub(curdate(), interval 7 day) <= date(date)"

    try: 
        c.execute(sql)
        last_week_weather = c.fetchall()
        print("Loaded 7 days weather!")

    except:
        print("Something went wrong")
    finally:
        c.close()
        con.close()
        
        return last_week_weather

# print(get_past_one_week_weather())