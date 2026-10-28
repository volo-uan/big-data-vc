\timing on

-- The computation that killed pandas on CSV.
SELECT avg(trip_distance) FROM trips;

-- The computation that pandas fits into the limit only barely.
SELECT pu_location_id, do_location_id, count(*) AS n, avg(trip_distance) AS d
FROM trips
GROUP BY 1, 2
ORDER BY n DESC
LIMIT 5;

-- What the engine is allowed to hold at once.
SHOW shared_buffers;
SHOW work_mem;
