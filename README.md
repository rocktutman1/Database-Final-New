
# Guide to downloading and running Database-Final-New

## Description

If you want to **larp** as a race official then you can use this to do so. \
Also if you want to store race times, you can also do that

## Requirements

- **Python 3** or higher
- **Docker** (maybe I'm not sure) and MYSQL
- Datetime and mysql.connector modules

## Installation

Clone the git repository

>git clone https://github.com/rocktutman1/Database-Final-New \
>cd Database-Final-New

## Localisation

If text is rendering stragely run these commands to fix it

>export LANG=en_US.UTF-8 \
>export LC_ALL=en_US.UTF-8

## Running

**Step 1: Set up MySQL in Docker**

```bash
docker run --name final-project-db \
  -e MYSQL_ROOT_PASSWORD=password \
  -p 3306:3306 \
  -d mysql:latest
```

**Step 2: Create your database and tables**

```bash
docker exec -i final-project-db mysql -uroot -ppassword < schema.sql
docker exec -i final-project-db mysql -uroot -ppassword < data.sql
```

**Step 2.5: Create and source a VENV**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Python dependencies**

```bash
pip install mysql-connector-python
```

**Step 4: Run your app**

```bash
python main.py
```

## Table Descriptions

![ERD](https://github.com/rocktutman1/Database-Final-New/blob/main/ERD.png)

### Athletes
Stores country and name of athletes, and acts as a foreign key to records, event_entries, race_entries, and results.

### Races
Stores names and dates of races, and acts as a foreign key to events and race_entries

### Events
Stores individual events ran and identifies them even_type and heat, acts as a foreign key to event_entires

### Results
Stores finish times from events based, identified a composite foreign key of event and athlete ids, acts as a foreign key to splits

### Splits
Stores split distances and times from races 800m >= by deafult, identifiable by result_id

### Records
Stores personal record times of athletes per event, identified by athlete_id

### Race_Entries
Acts as a joining table between the M:M relationship Races and Athletes

### Event_Entries
Acts as a joining table between the M:M relationship Events and Athletes

## Features

Using the application main.py you can delete and insert to all 6 tables, update in pre-determined ways, and read data using pre-made queres (see bellow), read entire tables, and easily find race times and records by event, race, and athlete.

## Using the application

### Premade Queries

The following are the premade commands that can be found by entering  *2* -> *2*\
-- 0. Reads all data from every table -- \
-- 1. Gets every split along with the athelete that ran it and the event and their final time -- \
-- 2. Gets the fastest result for every event and who ran it -- \
-- 3. Gets the number of Atheletes from each country -- \
-- 4. Gets the number of athelets in each heat in each race -- \
-- 5. Gets the average time for each event type -- \
-- 6. Gets the number of events each athlete has entered -- \
-- 7. Selects all results where an athlete ran their personal record -- \
-- 8. Gets the average time for each country in each event type -- 

### Using event_type

Since event type does not use a fk it can be easily descronized, stick to only using the following values for it, or at least attempting to follow their naming conventions

* 100m
* 200m
* 300m
* 400m
* 800m
* 1500m
* 3000m
* 5000m
* 10000m
* 100m Hurdles
* 110m Hurdles
* 300m Hurdles
* 400m Hurdles
* 300m Steeplechase
* Half Marathon
* Marathon

### Finding IDs

Many update and read tools will ask you for a id to target. If you are unsure of the id you wish to target enter h and you will be taken to a id lookup to help you locate them based off name, or other ids

### Finding names

If you do not know the name of which to find an ID with you can find entries for the entire tables by entering *2* -> *3* from the main menu


## Known Limitations

The ways you can manipulate the database are extremely limited in contrast too what you can actually do with MYsql, so for writing complex, or even simple updates and selects you might want to consider logging in. Since the options given to you are by no means all encompasing.

## Reflection

I think I learened a lot from this project overall. I didnt have much expierence with the sql.connector before so I definitely got more hands on time with that. But I also was able to learn that I'm bit more compotent with SQL than I though since I had a lot less trouble writing insert statements and the like while actually working on a project rather than just learning a new thing. I also faced a couple big challenges, the 2 most notables ones being trying to figure out how to deal with the insane ammoutn of data that I decided to use (eventually I settled on having a python script take a input that I could very easily write and transform it into insert statements) and also trying to fight localisation features to get special characters like accented letters to display properly. Both of these defininetly took a lot of perseverance.

I think this was a decent culmination of everything we've learned so far in the semester, but a lot of stuff was deff missing like there was no reason to interact with rollbacks and the like in a database like this, except for the once or twice that I would actually have to add multiple things in one function, a lot of other stuff like users wasnt even present here at all. I think looking at how I approached the project it wasnt to bad eithier. I think I defininetly chose a good idea since people have already set up databases on this type of stuff so figuring out how data should fit together wasnt too hard. While there was a lot less I could've done like not gone super omega overkill with my data there was also a lot more I could've done, like tracked field events which I completely neglected, properly track DNS/DNF/DQ isntead of relying on the layers event_entries system, and finally maybe even track meet records for things like annual events. Overall i do think this project did succeed in showing me how much more there is to databases than the 10 minute labs we've done in class.

## Configuration

No configuration is currently avaiable
