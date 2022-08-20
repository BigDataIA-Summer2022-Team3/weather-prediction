import pymysql
from datetime import datetime as dt
# from dbconfig import funct
from functions.dbconfig import funct
import time

def save_log_into_db(logs):
    # 上传数据到本地库
    Host, User, Password = funct()
    con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
    c = con.cursor()

    logID = str(time.time())
    userID = 0
    logInfo = ''

    try: 
        print("Prepare to insert...")
        print(type(logs))
        name = logs.split('; ')[0]
        print(name)
        if 'zhijie' in name:
            userID = 1
        elif 'yijun' in name:
            userID = 2
        elif 'team4' in name:
            userID = 3
        elif 'parth' in name:
            userID = 4
        elif 'srikanth' in name:
            userID = 5
        else:
            userID = 6
        
        print(logs)
        logInfo = logs.split('; ')[1]
        print('#########################################00')
        print(logID)
        print(userID)
        print(logInfo)

        sql = "insert into log_table (logID, userID, logInfo)\
                values('%s', '%d','%s')" % \
                (logID, userID, logInfo)

        c.execute(sql)
        print('#########################################01')
        # testreturn = c.lastrowid
        con.commit() # 若操作为增删改则需要提交数据
        print('#########################################02')
        print("Inserted!")

    except Exception as e:
        print(e)
        print("Something went wrong")
    finally:
        c.close()
        con.close()
