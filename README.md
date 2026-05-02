
# Guide to downloading and running nerdle

## Description

If you want to **larp** as a race official then you can use this to do so


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


## Configuration

No configuration is currently avaiable
