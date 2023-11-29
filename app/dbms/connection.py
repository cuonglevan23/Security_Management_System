import mysql.connector

def Connect():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='Security_Management_System'
        )
    except mysql.connector.Error as e:
        print("MySQL Connection Error:", str(e))

    finally:
     return conn


