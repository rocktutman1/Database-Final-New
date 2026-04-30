import mysql.connector
def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='running-database',
            user='root',
            password='password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error {e}")
        return None

def add_athlete(connection, name, country):
    """Add a new Athlete to the database"""
    try: 
        cursor = connection.cursor()
        query = "INSERT INTO Athletes (name, country) VALUES (%s, %s)"
        cursor.execute(query, (name, country))
        connection.commit()
        print(f"Added Athlete: {name}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def add_race(connection, title, date):
    """Add a race to the database"""
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Races (name, date) VALUES (%s, %s)"
        cursor.execute(query, (title, date))
        connection.commit()
        print(f"Added race: {title}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def add_event(connection, race_id, event_type, heat):
    """Add an event to the database"""
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Events (race_id, event_type, heat) VALUES (%s, %s, %s)"
        cursor.execute(query, (race_id, event_type, heat))
        query = "SELECT name FROM Races WHERE id = %s"
        cursor.execute(query, (race_id,))
        race_name = cursor.fetchone()
        connection.commit()
        if race_name:
            print(f"Added event {heat} at {race_name[0]}")
        else:
            print(f"Added event {heat} (race not found)")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
