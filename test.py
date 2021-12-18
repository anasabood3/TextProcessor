import mysql.connector

mydb = mysql.connector.connect(host="localhost",user='root',passwd='MH{2t$Jw+%XpK5v}',database='test_db')


mycursor = mydb.cursor()
mycursor.execute('drop database world;')
for i in mycursor:
    print(i)
