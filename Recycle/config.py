import os
import pymysql
import pymysql.cursors

db_user = 'root'
db_password = '123456'
db_name = "point_system_2"
db_connection_name = 'rewardmeasure:us-central1:measureward2'


host = '127.0.0.1'
con = pymysql.connect(user=db_user,port=5432, password=db_password,host = host, db=db_name)
with con:
    cur =con.cursor()
    cur.execute("select * from user;")
    output = cur.fetchall()
    if not output:
        print("empty")
    else:

        print(output)
    print("test done!")

con.close()