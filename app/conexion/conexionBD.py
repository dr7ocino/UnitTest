import mysql.connector

def connectDB():
    try:
        connection = mysql.connector.connect(
            host="192.168.31.155",
            user="carlos",
            passwd="7603e5efLp@",
            database="test_RFID",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
