CREATE DATABASE IF NOT EXISTS Running;
USE Running;

-- Entity Tables --

-- I Guess if you had two guys from the same country with the name they would be the same guy aside from the pk
-- World athletics had birthdates but I was too lazy to include them :(, so idk
CREATE TABLE IF NOT EXISTS Athletes (
    id int PRIMARY KEY AUTO_INCREMENT,
    name varchar (100) NOT NULL,
    country varchar (3),    
    CHECK (LENGTH(country) = 3)
);
CREATE TABLE IF NOT EXISTS Records (
    id int PRIMARY KEY AUTO_INCREMENT,
    athlete_id INT NOT NULL,
    event_type varchar (100) NOT NULL,
    time TIME(3) NOT NULL,
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (athlete_id, event_type),
    CHECK (time > '00:00:00.000' AND time < '23:59:59.999')
);
CREATE TABLE IF NOT EXISTS Races (
    id int PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR (200) NOT NULL,
    date DATE DEFAULT CURRENT_DATE
); 
CREATE TABLE IF NOT EXISTS Events (
    id int PRIMARY KEY AUTO_INCREMENT,
    race_id int,
    event_type varchar (100) NOT NULL,
    heat varchar (100),
    FOREIGN KEY (race_id) REFERENCES Races(id) ON UPDATE CASCADE ON DELETE SET NULL,
    UNIQUE (race_id, event_type, heat)
);

-- Technically you could record DNF and DNS with null, there were a couple in the datasets but I changed my mind about this after
-- so theres no DNF/DNS/DQ or whatever else in the data but technically it can still work T-T
CREATE TABLE IF NOT EXISTS Results (
    id int PRIMARY KEY AUTO_INCREMENT,
    athlete_id INT,
    event_id INT NOT NULL,
    time TIME(3),
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (event_id) REFERENCES Events(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (time > '00:00:00.000' AND time < '23:59:59.999')
);
CREATE TABLE IF NOT EXISTS Splits (
    id INT PRIMARY KEY AUTO_INCREMENT,
    result_id INT NOT NULL,
    split_distance VARCHAR(100) NOT NULL,
    split_time TIME(3) NOT NULL,
    FOREIGN KEY (result_id) REFERENCES Results(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (split_time > '00:00:00.000' AND split_time < '23:59:59.999')
);
-- Relationship Tables -- 

CREATE TABLE IF NOT EXISTS Race_Entries (
    id int PRIMARY KEY AUTO_INCREMENT,
    athlete_id int,
    race_id int NOT NULL,
    UNIQUE (athlete_id, race_id),
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (race_id) REFERENCES Races(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Event_Entries(
    id int PRIMARY KEY AUTO_INCREMENT,
    athlete_id int,
    event_id int NOT NULL,
    UNIQUE (athlete_id, event_id),
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (event_id) REFERENCES Events(id) ON DELETE CASCADE ON UPDATE CASCADE
);
