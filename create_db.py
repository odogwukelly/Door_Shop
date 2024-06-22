import mysql.connector
from mysql.connector import errorcode

try:
    # Connect to the MySQL server
    mydb = mysql.connector.connect(
        host= "localhost",
        user="root",
        passwd="kitech",
        auth_plugin='sha256_password'
    )
    
    # Create a cursor object
    my_cursor = mydb.cursor()

    # Execute the command to create the database
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS door_Shop")
    
    # my_cursor.execute("DROP DATABASE door_shop")

    # Execute the command to show all databases
    my_cursor.execute("SHOW DATABASES")

    print("Database Created Successfully......")
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    # Close the cursor and connection
    if 'my_cursor' in locals() and my_cursor is not None:
        my_cursor.close()
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()