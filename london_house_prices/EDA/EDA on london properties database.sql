-- Handling 0 values in tube distance and crime 
update tubes
set distance = 2
where distance = 0

-- Average price per person in each postcode
select p.postcode, 
round(avg(p.price / p.bedrooms)) as price_per_person, 
avg(c.crime_count) as avg_crime,
round(avg(t.distance), 2) as avg_tube_distance
from properties p 
join crime c on p.property_id = c.property_id
join tubes t on p.property_id = t.property_id
group by postcode
order by price_per_person asc

-- Testing if living close to a tube station is more exspensive 
WITH CrimeCategories AS (
    SELECT c.crime_count,
           NTILE(3) OVER (ORDER BY c.crime_count) AS crime_third,
           CASE
               WHEN NTILE(3) OVER (ORDER BY c.crime_count) = 1 THEN 'Low'
               WHEN NTILE(3) OVER (ORDER BY c.crime_count) = 2 THEN 'Middle'
               WHEN NTILE(3) OVER (ORDER BY c.crime_count) = 3 THEN 'Upper'
           END AS crime_category,
           c.property_id
    FROM crime c
)
SELECT cc.crime_category,
       AVG(p.price) AS avg_price
FROM CrimeCategories cc
JOIN properties p ON cc.property_id = p.property_id
GROUP BY cc.crime_category
ORDER BY avg_price DESC;


-- Creating a scoring system to rank the best places to live
WITH normalized_data AS (
    SELECT 
        p.property_id, 
        p.price, 
        p.bedrooms, 
        p.address,
        ROUND(p.price / p.bedrooms , 2) AS price_per_person,
        t.distance as tube_distance,
        c.crime_count AS crime_count,

        -- Min-Max Normalization for price
        (p.price - (SELECT MIN(price) FROM properties)) / 
        (SELECT MAX(price) - MIN(price) FROM properties) AS price_score,

        -- Min-Max Normalization for tube distance
        (t.distance - (SELECT MIN(distance) FROM tubes)) / 
        (SELECT MAX(distance) - MIN(distance) FROM tubes) AS tube_score,

        -- Min-Max Normalization for crime rate
        (c.crime_count - (SELECT MIN(crime_count) FROM crime)) / 
        (SELECT MAX(crime_count) - MIN(crime_count) FROM crime) AS crime_score
    FROM properties p
    JOIN tubes t ON p.property_id = t.property_id
    JOIN crime c ON p.property_id = c.property_id
)
SELECT 
    property_id, 
    address,
    bedrooms,
    price_per_person,
    tube_distance,
    crime_count,
    
    -- Compute weighted score (lower is better for all factors)
    ROUND(
        (1 - price_score) * 0.4 + 
        (1 - tube_score) * 0.3 + 
        (1 - crime_score) * 0.3, 
        3
    ) AS final_score
FROM normalized_data
ORDER BY final_score DESC;






