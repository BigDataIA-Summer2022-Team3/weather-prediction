import pymysql
from functions.dbconfig import funct
# from dbconfig import funct

def load_history_weather(input_year:int):
    if(input_year > 2022):
        return "Input year should be a history year"
    
    Host, User, Password = funct()
    con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
    c = con.cursor()
    
    sql = "select DATE_FORMAT(date,'%%Y-%%m-%%d') dates, DATE_FORMAT(date,'%%m') months,precipitation,temp_max,temp_min,wind \
    from seattle_weather where year(date) = '%d'" % (input_year)

    try: 
        c.execute(sql)
        history_year_data = c.fetchall()
        print(f"Loaded history weather of {input_year}!")

    except:
        print("Something went wrong")
    finally:
        c.close()
        con.close()
        
    return history_year_data

# print(load_history_weather(2023))