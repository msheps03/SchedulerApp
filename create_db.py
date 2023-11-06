import mysql.connector

mydb =mysql.connector.connect(host='localhost', user="Shep", passwd = "1max2well3")

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE conflicts")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)

