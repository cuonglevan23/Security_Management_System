from app.dbms.connection import Connect
import mysql.connector
import sys


def adminLogin(adminInfo):

    sql="""SELECT * FROM admin WHERE username=%s and password=%s"""
    values=(adminInfo.getUserName(), adminInfo.getPassword())
    adminresult=None

    try:
        conn=Connect()
        cursor=conn.cursor()
        cursor.execute(sql, values)
        adminresult=cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print("Error", sys.exc_info())

    finally:
        del values, sql
        return adminresult
# Assume AdminInfo class has been defined with methods getUserName() and getPassword()

class AdminInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUserName(self):
        return self.username

    def getPassword(self):
        return self.password

# Test the adminLogin function

def createAdmin(username, password):
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Check if the admin already exists
        check_sql = "SELECT * FROM admin WHERE username = %s"
        check_values = (username,)
        cursor.execute(check_sql, check_values)
        existing_admin = cursor.fetchone()

        if existing_admin:
            print("Admin with username '{}' already exists.".format(id))
            return None

        # If admin doesn't exist, create a new admin
        create_sql = """
            INSERT INTO admin (username,password)
            VALUES (%s, %s)
        """
        create_values = ( username,password)
        cursor.execute(create_sql, create_values)
        conn.commit()

        print("Admin '{}' created successfully.".format(username))

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))
    finally:
        if conn:
            conn.close()

