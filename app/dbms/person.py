from app.dbms.connection import Connect
import mysql.connector
from datetime import datetime
from datetime import timedelta

class PersonInfo:
    def __init__(self, id, username, age, phone, email, address):
        self.id = id
        self.username = username
        self.age = age
        self.phone = phone
        self.email = email
        self.address = address

    def getID(self):
        return self.id

    def getUserName(self):
        return self.username


class RecognizedPerson:
    def __init__(self, person_id, timestamp):
        self.person_id = person_id
        self.timestamp = timestamp

    def getPersonID(self):
        return self.person_id

    def getTimestamp(self):
        return self.timestamp


def person(personInfo):
    sql = "SELECT * FROM person WHERE id=%s"
    values = (personInfo.getID(),)
    person_result = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        person_result = cursor.fetchone()
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

    finally:
        del values, sql
        return person_result


def createPerson(person_info):
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        check_sql = "SELECT * FROM person WHERE id = %s"
        check_values = (person_info['id'],)
        cursor.execute(check_sql, check_values)
        existing_person = cursor.fetchone()

        if existing_person:
            print("Person with id '{}' already exists.".format(person_info['id']))
            return None

        create_sql = """
            INSERT INTO person (id, username, age, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        create_values = (
            person_info['id'],
            person_info['username'],
            person_info['age'],
            person_info['phone'],
            person_info['email'],
            person_info['address']
        )
        cursor.execute(create_sql, create_values)
        conn.commit()

        print("Person '{}' created successfully.".format(person_info['id']))

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))

    finally:
        if conn:
            conn.close()


def createRecognizedPerson(recognized_person):
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        create_sql = """
            INSERT INTO RecognizedPersons (person_id, timestamp)
            VALUES (%s, %s)
        """
        create_values = (
            recognized_person.getPersonID(),
            recognized_person.getTimestamp()
        )
        cursor.execute(create_sql, create_values)
        conn.commit()

        print("RecognizedPersons with person_id '{}' created successfully.".format(recognized_person.getPersonID()))

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))

    finally:
        if conn:
            conn.close()




def countRecognizedPersons(person_id, time_range):
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Calculate the start timestamp based on the time range
        if time_range == 'day':
            start_timestamp = current_timestamp - timedelta(days=1)
        elif time_range == 'month':
            start_timestamp = current_timestamp - timedelta(days=30)
        elif time_range == 'year':
            start_timestamp = current_timestamp - timedelta(days=365)
        else:
            print("Invalid time range")
            return None

        # Query to count RecognizedPersons within the specified time range
        count_sql = """
            SELECT COUNT(*) 
            FROM RecognizedPersons 
            WHERE person_id = %s 
                AND timestamp BETWEEN %s AND %s
        """
        count_values = (
            person_id,
            start_timestamp,
            current_timestamp
        )
        cursor.execute(count_sql, count_values)
        count_result = cursor.fetchone()[0]

        print("Number of RecognizedPersons for person_id '{}' in the last {} {}: {}".format(
            person_id, time_range, 'day' if time_range == 'day' else 'days',
            count_result
        ))

        return count_result

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))

    finally:
        if conn:
            conn.close()



def countRecognizedPersonsAll(time_range):
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Calculate the start timestamp based on the time range
        if time_range == 'day':
            start_timestamp = current_timestamp - timedelta(days=1)
        elif time_range == 'month':
            start_timestamp = current_timestamp - timedelta(days=30)
        elif time_range == 'year':
            start_timestamp = current_timestamp - timedelta(days=365)
        else:
            print("Invalid time range")
            return None

        # Query to count RecognizedPersons for all persons within the specified time range
        count_sql = """
            SELECT COUNT(*) 
            FROM RecognizedPersons 
            WHERE timestamp BETWEEN %s AND %s
        """
        count_values = (
            start_timestamp,
            current_timestamp
        )
        cursor.execute(count_sql, count_values)
        total_count = cursor.fetchone()[0]


        return total_count

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))

    finally:
        if conn:
            conn.close()


def joinPersonInfoAndRecognizedPerson():
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        join_sql = """
            SELECT pi.id, pi.username, pi.age, pi.phone, pi.address, pi.email, rp.timestamp
            FROM person pi
            JOIN RecognizedPersons rp ON pi.id = rp.person_id
        """

        cursor.execute(join_sql)
        join_results = cursor.fetchall()

        for result in join_results:
            person_id, username, age, phone, address, email, timestamp = result
            print("Person ID: {}, Username: {}, Age: {}, Phone: {}, Address: {}, Email: {}, Timestamp: {}".format(
                person_id, username, age, phone, address, email, timestamp
            ))

        return join_results

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))

    finally:
        if conn:
            conn.close()

def countTotalPersons():
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()

        count_sql = "SELECT COUNT(*) FROM person"
        cursor.execute(count_sql)
        total_persons = cursor.fetchone()[0]



        return total_persons

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))

    finally:
        if conn:
            conn.close()




# Example usage:
joinPersonInfoAndRecognizedPerson()