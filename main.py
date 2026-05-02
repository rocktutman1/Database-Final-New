import mysql.connector
from datetime import datetime
import database

def I_NEED_HELP(): #Gets ID's
    print("Welcome to I need help!! This is a tool to help you find ID's")
    print("1. Get athlete ID by name \n2. Get race ID by name \n3. Get event ID by race name \n4. Get result ID by athlete name and event id \n5. Get record ID by athlete name \n6. Back")
    help_target = input ("What would you like to do? ")
    if help_target.startswith("1"):
        athlete_name = input("What athlete would you like to find the ID for? ")
        database.get_athlete_id(connection, athlete_name)
    if help_target.startswith("2"):
        race_name = input("What race would you like to find the ID for? ")
        database.get_race_id(connection, race_name)
    if help_target.startswith("3"):
        race_name = input("What race would you like to find the event ID for? ")
        database.get_event_id(connection, race_name)
    if help_target.startswith("4"):
        athlete_name = input("What athlete would you like to find the result ID for? ")
        event_id = input("What event id would you like to see results for? (H for help) ")
        if event_id.startswith("H"):
            I_NEED_HELP()
        else:
            database.get_result_id(connection, athlete_name, event_id)
    if help_target.startswith("5"):
        athlete_name = input("What athlete would you like to find the record ID for? ")
        database.get_record_id(connection, athlete_name)
    if help_target.startswith("6"):
        return
    
def Good_Time_Machine(): #Verifies time
    while True:
        time = input("What is the athlete's time? (HH:MM:SS.sss) ")
        try:
            datetime.strptime(time, "%H:%M:%S.%f")
            break
        except ValueError:
            print("Invalid format. Use HH:MM:SS.sss")
        continue
    return time


connection = database.create_connection()

print("Welcome too the running database manager!!!")
print("View the README for helpfull instruction")

while True: #This is all pretty self explanitory its just nested if statements so I'm not gonna comment it
    print("1. Create \n2. Read \n 3. Update \n4. Delete \n5. Exit")
    choice = input("What would you like to do? ")
    if choice.startswith("1"):
        while True:
            print("1. Create athlete \n2. Create race \n3. Create event \n4. Create result \n5. Create split \n6. Create record \n7. Register athlete for race \n8. Register athlete for event \n9. Back")
            choice2 = input("What would you like to create? ")
            if choice2.startswith("1"):
                name = input("What is the athlete's name? ")
                country = input("What country is the athlete from? ")
                database.add_athlete(connection, name, country)
            if choice2.startswith("2"):
                name = input("What is the race's name? ")
                while True:
                    date = input("What is the race's date? (YYYY-MM-DD) ")
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date. Use YYYY-MM-DD.")
                        continue
                database.add_race(connection, name, date)
            if choice2.startswith("3"):
                race_name = input("What is the race called? (NULL for a unassociated event) ")
                event_type = input("What is the event type? ")
                heat = input("What heat is the event? ")
                database.add_event(connection, race_name, event_type, heat)
            if choice2.startswith("4"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                event_id = input("What is the event id? (H for help) ")
                if event_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                time = Good_Time_Machine()
                database.add_result(connection, athlete_id, event_id, time)
            if choice2.startswith("5"):
                result_id = input("What is the result id? (H for help) ")
                if result_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                split_distance = input("What is the split distance? (in meters) ")
                split_time = Good_Time_Machine()
                database.add_split(connection, result_id, split_distance, split_time)
            if choice2.startswith("6"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                event_type = input("What is the event type? ")
                record_time = Good_Time_Machine()
                database.add_record(connection, athlete_id, record_time, event_type)
            if choice2.startswith("7"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                race_id = input("What is the race id? (H for help) ")
                if race_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                database.register_race(connection, athlete_id, race_id)
            if choice2.startswith("8"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                event_id = input("What is the event id? (H for help) ")
                if event_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                database.register_event(connection, athlete_id, event_id)
            if choice2.startswith("9"):
                break
    if choice.startswith("2"):
        while True:
            print("1. Get results by parameter \n2. Use premade queries \n3. Read tables \n4. Back")
            choice2 = input("What would you like to do? ")
            if choice2.startswith("1"):
                print("1. Get results by race \n2. Get results by athlete \n3. Get results by event type \n4. Get records by athlete \n5. Get results by event \n6. Get splits by result \n7. Back")
                choice3 = input("What would you like to do? ")    
                if choice3.startswith("1"):
                    race_name = input("What race would you like to see results for? ")
                    database.get_race_results(connection, race_name)
                if choice3.startswith("2"):
                    athlete_name = input("What athlete would you like to see results for? ")
                    database.get_athlete_results(connection, athlete_name)
                if choice3.startswith("3"):
                    event_type = input("What event type would you like to see results for? ")
                    database.get_event_type_results(connection, event_type)
                if choice3.startswith("4"):
                    athlete_name = input("What athlete would you like to see records for? ")
                    database.get_athlete_records(connection, athlete_name)
                if choice3.startswith("5"):
                    while True:
                        event_id = input("What event id would you like to see results for? (h for help) ")
                        if event_id.startswith("h"):
                            I_NEED_HELP()
                        else:
                            database.get_event_results(connection, event_id)
                            break
                if choice3.startswith("6"):
                    while True:
                        result_id = input("What result id would you like to see splits for? (h for help) ")
                        if result_id.startswith("h"):
                            I_NEED_HELP()
                        else:
                            database.get_splits(connection, result_id)
                            break
                if choice3.startswith("7"):
                    break
            if choice2.startswith("2"):
                print("See all premade queries in Queries.sql")
                choice3 = input("What query would you like to run? (1-8) (9 for back) ")
                if choice3.startswith("9"):
                    break
                while True:
                    try:
                        database.premade(connection, int(choice3))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            if choice2.startswith("3"):
                print("1. Athletes \n2. Events \n3. Races \n4. Results \n5. Splits \n6. Records \n7. Back")
                choice3 = input("What table would you like to read? ")
                if choice3.startswith("1"):
                    database.starathletes(connection)
                if choice3.startswith("2"):
                    database.starevents(connection)
                if choice3.startswith("3"):
                    database.starraces(connection)
                if choice3.startswith("4"):
                    database.starresults(connection)
                if choice3.startswith("5"):
                    database.starsplits(connection)
                if choice3.startswith("6"):
                    database.starrecords(connection)
                if choice3.startswith("7"):
                    break
            if choice2.startswith("4"):
                break
    if choice.startswith("3"):
        while True:
            print("1. Update athlete country \n2. Update athlete name \n3. Update personal record \n4. Back")
            choice2 = input("What would you like to update? ")
            if choice2.startswith("1"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                new_country = input("What is the athlete's new country? ")
                database.update_athlete_country(connection, athlete_id, new_country)
            if choice2.startswith("2"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                new_name = input("What is the athlete's new name? ")
                database.update_athlete_name(connection, athlete_id, new_name)
            if choice2.startswith("3"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                event_type = input("What is the event type for the record? ")
                new_time = Good_Time_Machine()
                database.update_personal_record(connection, athlete_id, event_type, new_time)
            if choice2.startswith("4"):
                break
    if choice.startswith("4"):
        while True:
            print("1. Delete athlete \n2. Delete race \n3. Delete event \n4. Delete result\n5. Delete record \n6. Back")
            choice2 = input("What would you like to delete? ")
            if choice2.startswith("1"):
                athlete_id = input("What is the athlete's ID? (H for help) ")
                if athlete_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                if input(f"Are you sure you want to delete athlete #{athlete_id}? This cannot be undone. (Y/N) ").upper().startswith("Y"):
                    database.delete_athlete(connection, athlete_id)
                else:
                    print("Deletion cancelled.")
            if choice2.startswith("2"):
                race_id = input("What is the race's ID? (H for help) ")
                if race_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                if input(f"Are you sure you want to delete race #{race_id}? This cannot be undone. (Y/N) ").upper().startswith("Y"):
                    database.delete_race(connection, race_id)
                else:
                    print("Deletion cancelled.")
            if choice2.startswith("3"):
                event_id = input("What is the event's ID? (H for help) ")
                if event_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                if input(f"Are you sure you want to delete event #{event_id}? This cannot be undone. (Y/N) ").upper().startswith("Y"):
                    database.delete_event(connection, event_id)
                else:
                    print("Deletion cancelled.")
            if choice2.startswith("4"):
                result_id = input("What is the result's ID? (H for help) ")
                if result_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                if input(f"Are you sure you want to delete result #{result_id}? This cannot be undone. (Y/N) ").upper().startswith("Y"):
                    database.delete_result(connection, result_id)
                else:
                    print("Deletion cancelled.")
            if choice2.startswith("5"):
                record_id = input("What is the record's ID? (H for help) ")
                if record_id.startswith("H"):
                    I_NEED_HELP()
                    continue
                if input(f"Are you sure you want to delete record #{record_id}? This cannot be undone. (Y/N) ").upper().startswith("Y"):
                    database.delete_record(connection, record_id)
                else:
                    print("Deletion cancelled.")
            if choice2.startswith("6"):
                break
    if choice.startswith("5"):
        print("Goodbye!") 
        break #Man I've ts took me like 5 hours because I spent 3 trying to figure out how to run docker on my computer cus I need to make the demo video and its due tonight