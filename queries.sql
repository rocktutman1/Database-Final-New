-- 1. Gets every split along with the athelete that ran it and the event and their final time -- 
SELECT split_distance, split_time, event_type, time, name FROM Splits
JOIN Results on Results.id = Splits.result_id 
JOIN Events on Events.id = Results.event_id 
JOIN Athletes on Results.athlete_id = Athletes.id
ORDER BY split_time ASC;

-- 2. Gets the fastest result for every event and who ran it --
SELECT time, name, event_type
FROM Results
JOIN Athletes ON Results.athlete_id = Athletes.id
JOIN Events ON Results.event_id = Events.id
WHERE time IN (
    SELECT MIN(Results.time) FROM Results
    JOIN Events ON Results.event_id = Events.id
    GROUP BY Events.event_type
)
ORDER BY time ASC;

-- 3. Gets the number of Atheletes from each country --
SELECT country, COUNT(*) AS num_athletes
FROM Athletes
GROUP BY country
ORDER BY num_athletes DESC;

-- 4. Gets the number of athelets in each heat in each race --
SELECT count(*) AS num_athletes, heat, name FROM Races
JOIN Events ON Races.id = Events.race_id
JOIN Results ON Events.id = Results.event_id
GROUP BY heat, name
ORDER BY num_athletes DESC; 

-- 5. Gets the average time for each event type --
SELECT SEC_TO_TIME(ROUND(AVG(TIME_TO_SEC(time)), 3)) AS avg_time, event_type FROM Events
JOIN Results ON Results.event_id = Events.id
WHERE Results.time IS NOT NULL
GROUP BY event_type
ORDER BY avg_time DESC;

-- 6. Gets the number of events each athlete has entered --
SELECT name, count(athlete_id) as num_events FROM Event_Entries
RIGHT JOIN Athletes ON Athletes.id = Event_Entries.athlete_id
GROUP BY name, athlete_id
ORDER BY num_events DESC;

-- 7. Selects all results where an athlete ran their personal record --
SELECT name, event_type, time as PR FROM Results
JOIN Athletes ON Results.athlete_id = Athletes.id
JOIN Events ON Results.event_id = Events.id
WHERE (time, name, event_type) IN (
    SELECT time, name, event_type FROM Records
    JOIN Athletes ON Records.athlete_id = Athletes.id
);

-- 8. Gets the average time for each country in each event type --
SELECT country, event_type, SEC_TO_TIME(ROUND(AVG(TIME_TO_SEC(time)), 3)) AS avg_time FROM Athletes
JOIN Results ON Athletes.id = Results.athlete_id
JOIN Events ON Results.event_id = Events.id
WHERE time IS NOT NULL
GROUP BY country, event_type
ORDER BY avg_time DESC;