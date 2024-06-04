import mysql.connector
from mysql.connector import errorcode

try:
    # Connect to the MySQL server
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="kitech"
    )
    
    # Create a cursor object
    my_cursor = mydb.cursor()

    # Execute the command to create the database
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS door_Shop")

    # Execute the command to show all databases
    my_cursor.execute("SHOW DATABASES")
    
    # Fetch and print the list of databases
    for db in my_cursor:
        print(db)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
