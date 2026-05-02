import mysql.connector

## Stuff ig

def fix_encoding(message):
    """some bs was happening where it was turning all the accents into nonsence and I googled it apparently 
    this is the fix """
    return message.encode("latin-1").decode("utf-8")

def epstein_reader(cursor):
    """lil printy function to print stuff"""
    headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    for h in headers:
        print(h, end="      ")
    print()
    print("=" * 100)
    for row in rows:
        for i in range(len(row)):
            dude = fix_encoding(str(row[i]))
            ## Grows and shrinks the spacing 
            if headers[i] == "race":
                print(dude.ljust(40), end="")
            elif headers[i] == "country":
                print(dude.ljust(7), end="")
            elif headers[i] in ("time", "date"):
                print(dude[0:11].ljust(20), end="")
            else:
                print(dude.ljust(25), end="")
        print()

def create_connection():
    """ Create connection """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="Running",
        )
        ## Tried to do localisation stuff here for a while before I found out I needed to encode it
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

## Stuff to give data for other queries

def get_record_id(connection, name):
    try:
        cursor=connection.cursor()
        cursor.execute("Select * from Records WHERE athlete_id = (SELECT id FROM Athletes WHERE name = %s)", (name,))
        print(f"\nRecords for {name}")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_athlete_id(connection, name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Athletes WHERE name = %s", (name,))
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_race_id(connection, name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Races WHERE name = %s", (name,))
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_event_id(connection, race_name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Events WHERE race_id = (SELECT id FROM Races WHERE name = %s)", (race_name,)) ## Somestimes I feel nice and dont make them go into HELP_ME while already in HELP_ME
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_result_id(connection, athlete_name, event_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Results.id, Athletes.name, time FROM Results JOIN Athletes ON Results.athlete_id = Athletes.id WHERE Athletes.name = %s AND event_id = %s", (athlete_name, event_id))
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

## (C)RUD

def add_record(connection, athlete_id, time, event_type):
    """Add a new record if there is no exsisting record and they dont have a recorded faster time"""
    try:
        cursor = connection.cursor()
        fastest_time_q = "SELECT CAST(MIN(time) AS CHAR) FROM Results JOIN Events ON Results.event_id = Events.id WHERE athlete_id = %s AND event_type = %s"
        cursor.execute(fastest_time_q, (athlete_id, event_type)) #Cast as char because I give it input as a string and I cant compare a deltatime object to a string
        fastest_result = cursor.fetchone()[0] 
        if fastest_result is not None and time >= fastest_result:
            print(f"Error: Time {time} is not faster than best result {fastest_result}")
            return
        existing_record_q = "SELECT time FROM Records WHERE athlete_id = %s AND event_type = %s"
        cursor.execute(existing_record_q, (athlete_id, event_type))
        existing_record = cursor.fetchone()
        if existing_record:
            print(f"Error: Record already exists for athlete {athlete_id} in {event_type}, use update instead")
            return
        insert_record_q = "INSERT INTO Records (athlete_id, event_type, time) VALUES (%s, %s, %s)"
        cursor.execute(insert_record_q, (athlete_id, event_type, time))
        connection.commit()
        print(f"Record added for {athlete_id} in {event_type}: {time}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

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

def add_event(connection, race_name, event_type, heat):
    """Add an event to the database"""
    try:
        cursor = connection.cursor()
        if race_name == "NULL".upper(): ## I figure it kinda makes sence to be able to have events that arent part of a meet, and I think sql doesnt enforce unique on nulls
            query = "INSERT INTO Events (event_type, heat) VALUES (%s, %s)"
            cursor.execute(query, (event_type, heat))
        else:
            query = "INSERT INTO Events (race_id, event_type, heat) VALUES ((SELECT id FROM Races WHERE name = %s), %s, %s)"
            cursor.execute(query, (race_name, event_type, heat))
        connection.commit()
        print(f"Added event: {event_type} heat {heat}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def add_result(connection, athlete_id, event_id, time):
    """Add a result and also put the athlete into the event and race if they arent already.
    If the result is a PB it will update the records table."""
    try:
        cursor = connection.cursor()
        cursor.execute("START TRANSACTION") ## DEI transaction because the rubric asked for one
        cursor.execute("SELECT race_id, event_type FROM Events WHERE id = %s", (event_id,)) ## get stuff to check for pbs and also register athletes for races
        row = cursor.fetchone()
        if not row:
            cursor.execute("ROLLBACK")
            print(f"Error: Event {event_id} not found")
            return
        race_id, event_type = row
        cursor.execute("INSERT IGNORE INTO Race_Entries (athlete_id, race_id) VALUES (%s, %s)",(athlete_id, race_id)) #I decided to have it do this to avoid orphaned entries
        cursor.execute("INSERT IGNORE INTO Event_Entries (athlete_id, event_id) VALUES (%s, %s)",(athlete_id, event_id)) #Ignore so no error :)
        cursor.execute("INSERT INTO Results (athlete_id, event_id, time) VALUES (%s, %s, %s)",(athlete_id, event_id, time))
        # check if this is a pb (peanut butter)
        cursor.execute("SELECT CAST(time as CHAR) FROM Records WHERE athlete_id = %s AND event_type = %s",(athlete_id, event_type))
        existing_record = cursor.fetchone()
        if not existing_record: ##Insert the new peanut butter
            cursor.execute("INSERT INTO Records (athlete_id, event_type, time) VALUES (%s, %s, %s)",(athlete_id, event_type, time))
            is_pb = True
        elif time < existing_record[0]: ##Updates the peantut butter to peanut jam
            cursor.execute("UPDATE Records SET time = %s WHERE athlete_id = %s AND event_type = %s",(time, athlete_id, event_type))
            is_pb = True
        else:
            is_pb = False
        cursor.execute("COMMIT")
        cursor.execute("SELECT name FROM Athletes WHERE id = %s", (athlete_id,))
        athlete_name = cursor.fetchone()[0]
        cursor.execute("SELECT heat FROM Events WHERE id = %s", (event_id,))
        heat = cursor.fetchone()[0]
        print(f"Added result for {athlete_name} in {heat}: {time}")
        if is_pb:
            print("  New Peronal best registed")
    except mysql.connector.Error as e:
        cursor.execute("ROLLBACK")
        print(f"Error: {e}")

def add_split(connection, result_id, split_distance, split_time):
    try:
        cursor = connection.cursor()
        insert_split_q = "INSERT INTO Splits (result_id, split_distance, split_time) VALUES (%s, %s, %s)"
        cursor.execute(insert_split_q, (result_id, split_distance, split_time))
        connection.commit()
        print(f"Split added for result #{result_id}: {split_distance} in {split_time}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def register_race(connection, athlete_id, race_id):
    """Register a athelete for a race"""
    try: 
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Race_Entries (athlete_id, race_id) VALUES (%s, %s)",(athlete_id, race_id))
        connection.commit()
        print(f"Registered athlete #{athlete_id} for race #{race_id}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def register_event(connection, athlete_id, event_id):
    """Register a athelete for a event"""
    try: 
        cursor=connection.cursor()
        cursor.execute("INSERT INTO Event_Entries (athlete_id, event_id) VALUES (%s, %s)",(athlete_id,event_id))
        cursor.execute("INSERT IGNORE INTO Race_Entries (athlete_id, race_id) VALUES (%s, (SELECT race_id FROM Events WHERE id = %s))", (athlete_id, event_id))\
        ## Did this while writing comments and realized I avoided orphaned entries earlier but not here ^
        connection.commit()
        print(f"Registered athlete #{athlete_id} for event #{event_id}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

## C(R)UD

def get_race_results(connection, race_name):
    """Get all results for a race"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT heat, Athletes.name, country, time FROM Results JOIN Athletes  ON Results.athlete_id = Athletes.id JOIN Events ON Results.event_id = Events.id JOIN Races ON Events.race_id = Races.id WHERE Races.name = %s ORDER BY heat, time", (race_name,))
        print(f"\nAll {race_name} results")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_athlete_results(connection, athlete_name):
    """Get all results for a athlete"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, event_type, heat, time FROM Results JOIN Events ON Results.event_id = Events.id JOIN Races ON Events.race_id = Races.id WHERE athlete_id = (SELECT id FROM Athletes WHERE name = %s) ORDER BY time, event_type", (athlete_name,))
        print(f"\n{athlete_name}")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_event_type_results(connection, event_type):
    """Get all results for a type of event"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Athletes.name, country, Races.name as race, date, time FROM Results JOIN Athletes ON Results.athlete_id = Athletes.id JOIN Events ON Results.event_id = Events.id JOIN Races ON Events.race_id = Races.id WHERE event_type = %s ORDER BY time ", (event_type,))
        print(f"\nAll {event_type} results")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_athlete_records(connection, athlete_name):
    """Get all records for a athlete"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, event_type, time from Athletes JOIN Records ON Records.athlete_id = Athletes.id WHERE name = (%s)", (athlete_name,))
        print(f"\n{athlete_name}")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_event_results(connection, event_id):
    """Get results for a specific event"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, time FROM Events JOIN Results on Events.id = Results.event_id JOIN Athletes on Results.athlete_id = Athletes.id WHERE Events.id = %s", (event_id,))
        print(f"\nResults for event #{event_id}")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_splits(connection, result_id):
    """Get splits for a specific result"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT split_distance, split_time FROM Splits WHERE result_id = %s", (result_id,))
        print(f"\nSplits for result #{result_id}")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")
## premade queries cus why not

def premade(connection, query): ## Figured it would be a waste of time to have written them for queries.sql and not put them in here
    try:
        big_scary_query_list = ['SELECT * FROM Races', 
            '''SELECT split_distance, split_time, event_type, time, name FROM Splits JOIN Results on Results.id = Splits.result_id JOIN Events on Events.id = Results.event_id JOIN Athletes on Results.athlete_id = Athletes.id ORDER BY split_time ASC''',
            '''SELECT time, name, event_type FROM Results JOIN Athletes ON Results.athlete_id = Athletes.id JOIN Events ON Results.event_id = Events.id WHERE time IN ( SELECT MIN(Results.time) FROM Results JOIN Events ON Results.event_id = Events.id GROUP BY Events.event_type ) ORDER BY time ASC''',
            '''SELECT country, COUNT(*) AS num_athletes FROM Athletes GROUP BY country ORDER BY num_athletes DESC''',
            '''SELECT count(*) AS num_athletes, heat, name FROM Races JOIN Events ON Races.id = Events.race_id JOIN Results ON Events.id = Results.event_id GROUP BY heat, name ORDER BY num_athletes DESC''',
            '''SELECT SEC_TO_TIME(ROUND(AVG(TIME_TO_SEC(time)), 3)) AS avg_time, event_type FROM Events JOIN Results ON Results.event_id = Events.id WHERE results.time IS NOT NULL GROUP BY event_type ORDER BY avg_time DESC''',
            '''SELECT name, count(athlete_id) as num_events FROM Event_Entries RIGHT JOIN Athletes ON Athletes.id = Event_Entries.athlete_id GROUP BY name, athlete_id ORDER BY num_events DESC''',
            '''SELECT name, event_type, time as PR FROM Results JOIN Athletes ON Results.athlete_id = Athletes.id JOIN Events ON Results.event_id = Events.id WHERE (time, name, event_type) IN ( SELECT time, name, event_type FROM Records JOIN Athletes ON Records.athlete_id = Athletes.id )''',
            '''SELECT country, event_type, SEC_TO_TIME(ROUND(AVG(TIME_TO_SEC(time)), 3)) AS avg_time FROM Athletes JOIN Results ON Athletes.id = Results.athlete_id JOIN Events ON Results.event_id = Events.id WHERE time IS NOT NULL GROUP BY country, event_type ORDER BY avg_time DESC'''
            ]
        cursor=connection.cursor()
        cursor.execute(big_scary_query_list[query])
        print(f"Results for query #{query}")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

## also simple star selects cus I guess they would be a good idea
# I feel like ts is a waste of time because it would be so much faster to just write select stateaments in sql instead of making a frontend
# and its not even like I restriced privleges they could just enter * when deleting stuff and do the same damage
# Whats even the point of protecting against sql injection when they have all the privleges they could ever need besides like drop table and database
# Also the root password is litterally hardcoded so idk dawg
# Also they make the container 
def starathletes(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Athletes")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def starraces(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Races")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def starevents(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Events")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def starsplits(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Splits")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def starrecords(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Records")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def starresults(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Results")
        epstein_reader(cursor)
    except mysql.connector.Error as e:
        print(f"Error: {e}")

## CR(U)D

def update_record(connection, athlete_id, event_type, time): #This function reminds me of mijo :(
    """Update a record if the new time is faster"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT CAST(time as CHAR) as time FROM Records WHERE athlete_id = %s AND event_type = %s", (athlete_id, event_type))
        existing_record = cursor.fetchone()
        if not existing_record:
            print(f"Error: No record found for athlete {athlete_id} in {event_type}, use add instead")
            return
        if time >= existing_record[0]:
            print("Not a personal reccord ")
            return
        cursor.execute("UPDATE Records SET time = %s WHERE athlete_id = %s AND event_type = %s", (time, athlete_id, event_type))
        connection.commit()
        print(f"Record updated for athlete {athlete_id} in {event_type}: {time}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def update_athlete_name(connection, athlete_id, name):
    """Update the name of an athlete"""
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Athletes SET name = %s WHERE id = %s", (name, athlete_id))
        connection.commit()
        print(f"Athlete {athlete_id} name updated to {name}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def update_athlete_country(connection, athlete_id, country):
    """Update the country of an athlete"""
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Athletes SET country = %s WHERE id = %s", (country, athlete_id))
        connection.commit()
        print(f"Athlete {athlete_id} country updated to {country}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

## CRU(D)

def delete_athlete(connection, athlete_id):
    try: 
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Athletes WHERE id = %s", (athlete_id,))
        connection.commit()
        print(f"Athlete #{athlete_id} deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    
def delete_race(connection, race_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Races WHERE id = %s", (race_id,))
        connection.commit()
        print(f"Race #{race_id} deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def delete_event(connection, event_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Events WHERE id = %s", (event_id,))
        connection.commit()
        print(f"Event #{event_id} deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def delete_result(connection, result_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Results WHERE id = %s", (result_id,))
        connection.commit()
        print(f"Result #{result_id} deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def delete_record(connection, athlete_id, event_type):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Records WHERE athlete_id = %s AND event_type = %s", (athlete_id, event_type))
        connection.commit()
        print(f"Record for athlete #{athlete_id} in {event_type} deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

