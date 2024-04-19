from dotenv import load_dotenv
import os
import mysql.connector
load_dotenv()
def connectDB():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            passwd=os.getenv("MYSQL_PASSWORD"),
            database="test_RFID",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")




            
# host=os.getenv("MYSQL_HOST"),
# user=os.getenv("MYSQL_USER"),
# passwd=os.getenv("MYSQL_PASSWORD"),
# database=os.getenv("MYSQL_DATABASE"),
# charset='utf8mb4',
# collation='utf8mb4_unicode_ci',
# raise_on_warnings=True
        