-- ============================================================
-- Global Seismic Trends: Data-Driven Earthquake Insights
-- SQL Analysis Queries
-- Database: earthquake_db
-- Table: earthquakes
--
-- Note:
-- Tasks that require casualties, economic loss, or alert-level
-- fields cannot be calculated from the current USGS table because
-- those fields are not present in the project dataset.
-- ============================================================

USE earthquake_db;

-- ============================================================
-- TASK 1: Top 10 strongest earthquakes
-- ============================================================
SELECT
    id, time, place, mag, depth_km
FROM earthquakes
WHERE mag IS NOT NULL
ORDER BY mag DESC
LIMIT 10;


-- ============================================================
-- TASK 2: Top 10 deepest earthquakes
-- ============================================================
SELECT
    id, time, place, mag, depth_km
FROM earthquakes
WHERE depth_km IS NOT NULL
ORDER BY depth_km DESC
LIMIT 10;


-- ============================================================
-- TASK 3: Shallow earthquakes (<50 km) with magnitude > 7.5
-- ============================================================
SELECT
    id, time, place, mag, depth_km
FROM earthquakes
WHERE depth_km < 50
  AND mag > 7.5
ORDER BY mag DESC;


-- ============================================================
-- TASK 4: Average depth per continent
-- NOTE: The current table does not contain a continent column.
-- ============================================================
-- Requires a continent mapping derived from country/coordinates.


-- ============================================================
-- TASK 5: Average magnitude per magnitude type
-- ============================================================
SELECT
    magType,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE magType IS NOT NULL
  AND mag IS NOT NULL
GROUP BY magType
ORDER BY average_magnitude DESC;


-- ============================================================
-- TASK 6: Year with the most earthquakes
-- ============================================================
SELECT
    year,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY year
ORDER BY earthquake_count DESC
LIMIT 1;


-- Full yearly count
SELECT
    year,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY year
ORDER BY year;


-- ============================================================
-- TASK 7: Month with the highest earthquake count
-- ============================================================
SELECT
    month,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY month
ORDER BY earthquake_count DESC
LIMIT 1;


-- Monthly names and counts
SELECT
    MONTHNAME(STR_TO_DATE(month, '%m')) AS month_name,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY month
ORDER BY earthquake_count DESC;


-- ============================================================
-- TASK 8: Weekday with the most earthquakes
-- ============================================================
SELECT
    day_of_week,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE day_of_week IS NOT NULL
GROUP BY day_of_week
ORDER BY earthquake_count DESC
LIMIT 1;


-- ============================================================
-- TASK 9: Earthquake count by hour
-- ============================================================
SELECT
    HOUR(time) AS hour_of_day,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE time IS NOT NULL
GROUP BY HOUR(time)
ORDER BY hour_of_day;


-- ============================================================
-- TASK 10: Most active seismic network
-- ============================================================
SELECT
    net,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE net IS NOT NULL
  AND net <> ''
GROUP BY net
ORDER BY earthquake_count DESC
LIMIT 1;


-- Full network ranking
SELECT
    net,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE net IS NOT NULL
  AND net <> ''
GROUP BY net
ORDER BY earthquake_count DESC;


-- ============================================================
-- TASK 11: Top 5 places with highest casualties
-- NOTE: No casualties/fatalities column exists in the current table.
-- ============================================================


-- ============================================================
-- TASK 12: Total estimated economic loss per continent
-- NOTE: No economic-loss column exists in the current table.
-- ============================================================


-- ============================================================
-- TASK 13: Average economic loss by alert level
-- NOTE: No economic-loss or alert-level column exists in the table.
-- ============================================================


-- ============================================================
-- TASK 14: Reviewed vs automatic events
-- ============================================================
SELECT
    status,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE status IS NOT NULL
GROUP BY status
ORDER BY earthquake_count DESC;


-- ============================================================
-- TASK 15: Earthquake count by event type
-- ============================================================
SELECT
    type,
    COUNT(*) AS event_count
FROM earthquakes
WHERE type IS NOT NULL
GROUP BY type
ORDER BY event_count DESC;


-- ============================================================
-- TASK 16: Number of earthquakes by data type
-- `types` contains a comma-separated list of USGS products.
-- ============================================================
SELECT
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(types, ',', numbers.n), ',', -1)) AS data_type,
    COUNT(*) AS earthquake_count
FROM earthquakes
JOIN (
    SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL
    SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL
    SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL
    SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL
    SELECT 19 UNION ALL SELECT 20
) numbers
ON numbers.n <= 1 + LENGTH(types) - LENGTH(REPLACE(types, ',', ''))
WHERE types IS NOT NULL
  AND types <> ''
GROUP BY data_type
ORDER BY earthquake_count DESC;


-- ============================================================
-- TASK 17: Average RMS and GAP per continent
-- NOTE: No continent column exists in the current table.
-- ============================================================


-- ============================================================
-- TASK 18: High station coverage (nst > 100)
-- ============================================================
SELECT
    COUNT(*) AS high_station_coverage_events,
    ROUND(AVG(nst), 2) AS average_station_count,
    MAX(nst) AS maximum_station_count
FROM earthquakes
WHERE nst > 100;


-- Detailed high-coverage events
SELECT
    id, time, place, mag, nst
FROM earthquakes
WHERE nst > 100
ORDER BY nst DESC;


-- ============================================================
-- TASK 19: Tsunami events per year
-- ============================================================
SELECT
    year,
    COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year
ORDER BY year;


-- ============================================================
-- TASK 20: Count by alert level
-- NOTE: No alert-level column exists in the current table.
-- ============================================================


-- ============================================================
-- TASK 21: Top 5 countries by average magnitude
-- ============================================================
SELECT
    country,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE country IS NOT NULL
  AND country <> ''
  AND mag IS NOT NULL
GROUP BY country
ORDER BY average_magnitude DESC
LIMIT 5;

-- IMPORTANT:
-- Country/region values were derived from the USGS `place` field,
-- so small-sample and imperfect-extraction cases should be treated
-- cautiously.


-- ============================================================
-- TASK 22: Countries having both shallow and deep earthquakes
-- in the same year/month
-- ============================================================
SELECT
    country,
    year,
    month,
    SUM(depth_category = 'Shallow') AS shallow_count,
    SUM(depth_category = 'Deep') AS deep_count
FROM earthquakes
WHERE country IS NOT NULL
  AND country <> ''
GROUP BY country, year, month
HAVING shallow_count > 0
   AND deep_count > 0
ORDER BY year, month, country;


-- ============================================================
-- TASK 23: Year-over-year earthquake growth
-- ============================================================
WITH yearly_counts AS (
    SELECT
        year,
        COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY year
)
SELECT
    year,
    earthquake_count,
    LAG(earthquake_count) OVER (ORDER BY year) AS previous_year_count,
    ROUND(
        (
            earthquake_count -
            LAG(earthquake_count) OVER (ORDER BY year)
        ) * 100.0 /
        NULLIF(LAG(earthquake_count) OVER (ORDER BY year), 0),
        2
    ) AS yoy_growth_percent
FROM yearly_counts
ORDER BY year;


-- ============================================================
-- TASK 24: Top 3 regions combining frequency and average magnitude
-- Activity score = earthquake_count * average_magnitude
-- ============================================================
SELECT
    region,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude,
    ROUND(COUNT(*) * AVG(mag), 2) AS activity_score
FROM earthquakes
WHERE region IS NOT NULL
  AND region <> ''
  AND mag IS NOT NULL
GROUP BY region
ORDER BY activity_score DESC
LIMIT 3;


-- ============================================================
-- TASK 25: Average depth for each country within ±5° latitude
-- of the equator
-- ============================================================
SELECT
    country,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(depth_km), 2) AS average_depth_km
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
  AND country IS NOT NULL
  AND country <> ''
GROUP BY country
ORDER BY average_depth_km DESC;


-- ============================================================
-- TASK 26: Country with the highest shallow/deep ratio
-- ============================================================
SELECT
    country,
    SUM(depth_category = 'Shallow') AS shallow_count,
    SUM(depth_category = 'Deep') AS deep_count,
    ROUND(
        SUM(depth_category = 'Shallow') /
        NULLIF(SUM(depth_category = 'Deep'), 0),
        2
    ) AS shallow_deep_ratio
FROM earthquakes
WHERE country IS NOT NULL
  AND country <> ''
GROUP BY country
HAVING deep_count > 0
ORDER BY shallow_deep_ratio DESC
LIMIT 1;


-- ============================================================
-- TASK 27: Average magnitude for tsunami vs non-tsunami events
-- ============================================================
SELECT
    CASE
        WHEN tsunami = 1 THEN 'Tsunami'
        ELSE 'No Tsunami'
    END AS tsunami_status,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE mag IS NOT NULL
GROUP BY tsunami_status
ORDER BY average_magnitude DESC;


-- ============================================================
-- TASK 28: Lowest reliability using GAP/RMS indicator
-- Project-defined indicator:
-- reliability_indicator = (gap + rms) / 2
-- Lower values are considered better by this project metric.
--
-- NOTE: GAP and RMS have different units/scales, so this is only
-- a simple project-defined indicator, not an official USGS score.
-- ============================================================
SELECT
    id,
    time,
    place,
    mag,
    gap,
    rms,
    ROUND((gap + rms) / 2, 2) AS reliability_indicator
FROM earthquakes
WHERE gap IS NOT NULL
  AND rms IS NOT NULL
ORDER BY reliability_indicator DESC
LIMIT 10;


-- ============================================================
-- TASK 29: Consecutive earthquake pairs within 50 km and 1 hour
-- Uses the Haversine formula.
-- ============================================================
WITH ordered_events AS (
    SELECT
        id,
        time,
        latitude,
        longitude,
        mag,
        place,
        LAG(id) OVER (ORDER BY time) AS previous_id,
        LAG(time) OVER (ORDER BY time) AS previous_time,
        LAG(latitude) OVER (ORDER BY time) AS previous_latitude,
        LAG(longitude) OVER (ORDER BY time) AS previous_longitude
    FROM earthquakes
)
SELECT
    id AS event_id,
    previous_id,
    time AS event_time,
    previous_time,
    TIMESTAMPDIFF(SECOND, previous_time, time) / 3600.0
        AS time_difference_hours,
    ROUND(
        6371 * 2 * ASIN(
            SQRT(
                POWER(
                    SIN(
                        RADIANS(latitude - previous_latitude) / 2
                    ), 2
                ) +
                COS(RADIANS(previous_latitude)) *
                COS(RADIANS(latitude)) *
                POWER(
                    SIN(
                        RADIANS(longitude - previous_longitude) / 2
                    ), 2
                )
            )
        ),
        2
    ) AS distance_km,
    mag,
    place
FROM ordered_events
WHERE previous_id IS NOT NULL
  AND TIMESTAMPDIFF(SECOND, previous_time, time) BETWEEN 0 AND 3600
  AND latitude IS NOT NULL
  AND longitude IS NOT NULL
  AND previous_latitude IS NOT NULL
  AND previous_longitude IS NOT NULL
HAVING distance_km <= 50
ORDER BY event_time;


-- ============================================================
-- TASK 30: Regions with the highest frequency of deep-focus
-- earthquakes (>300 km)
-- ============================================================
SELECT
    region,
    COUNT(*) AS deep_focus_count
FROM earthquakes
WHERE depth_km > 300
  AND region IS NOT NULL
  AND region <> ''
GROUP BY region
ORDER BY deep_focus_count DESC
LIMIT 10;


-- ============================================================
-- ADDITIONAL USEFUL PROJECT QUERIES
-- ============================================================

-- Total records
SELECT COUNT(*) AS total_earthquakes
FROM earthquakes;


-- Date range
SELECT
    MIN(time) AS earliest_event,
    MAX(time) AS latest_event
FROM earthquakes;


-- Duplicate ID check
SELECT
    COUNT(*) - COUNT(DISTINCT id) AS duplicate_id_count
FROM earthquakes;


-- Depth category distribution
SELECT
    depth_category,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY depth_category
ORDER BY earthquake_count DESC;


-- Strong earthquake count
SELECT
    COUNT(*) AS strong_earthquake_count
FROM earthquakes
WHERE strong_earthquake = 1;


-- Top countries by earthquake frequency
SELECT
    country,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE country IS NOT NULL
  AND country <> ''
GROUP BY country
ORDER BY earthquake_count DESC
LIMIT 10;


-- Top regions by earthquake frequency
SELECT
    region,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE region IS NOT NULL
  AND region <> ''
GROUP BY region
ORDER BY earthquake_count DESC
LIMIT 10;
