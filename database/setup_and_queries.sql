
CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    rating DECIMAL(3,2) CHECK (rating >= 0 AND rating <= 5),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO restaurants (name, address, phone_number, rating, is_active) VALUES
('Sushi Sensation', '321 Elm St, Downtown', '+1-555-0104', 4.9, true),
('The Golden Spoon', '123 Main St, Uptown', '+1-555-0101', 4.8, true),
('Pasta Paradise', '456 Oak Ave, Midtown', '+1-555-0102', 4.7, true),
('Burger Barn', '789 Pine St, Westside', '+1-555-0103', 4.6, true),
('Pizza Palace', '654 Maple Ave, Eastside', '+1-555-0105', 4.5, true),
('Taco Town', '987 Cedar St, Southside', '+1-555-0106', 4.4, true),
('Curry Corner', '147 Birch St, Northside', '+1-555-0107', 4.3, true),
('Steakhouse Supreme', '258 Walnut St, Central', '+1-555-0108', 4.2, true),
('Seafood Shack', '369 Cherry St, Harbor', '+1-555-0109', 4.1, true),
('Deli Delights', '741 Spruce St, Market', '+1-555-0110', 4.0, true),
('Cafe Cozy', '852 Poplar St, Arts District', '+1-555-0111', 3.9, true),
('Bistro Blue', '963 Willow St, Financial', '+1-555-0112', 3.8, false),
('Grill & Chill', '159 Ash St, University', '+1-555-0113', NULL, true);


CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants(rating DESC);


CREATE INDEX IF NOT EXISTS idx_restaurants_rating_name ON restaurants(rating DESC, name ASC);


CREATE INDEX IF NOT EXISTS idx_restaurants_rating_active ON restaurants(rating DESC, name ASC) 
WHERE is_active = true AND rating IS NOT NULL;


CREATE INDEX IF NOT EXISTS idx_restaurants_name ON restaurants(name);


SELECT 
    id,
    name,
    address,
    phone_number,
    rating
FROM restaurants
WHERE rating IS NOT NULL
ORDER BY rating DESC, name ASC
LIMIT 5;


SELECT 
    id,
    name,
    address,
    phone_number,
    rating
FROM restaurants
WHERE rating IS NOT NULL 
    AND is_active = true
ORDER BY rating DESC, name ASC
LIMIT 5;

SELECT 
    id,
    name,
    address,
    phone_number,
    rating,
    ROUND(rating, 2) as formatted_rating,
    RANK() OVER (ORDER BY rating DESC) as rank,
    CASE 
        WHEN rating >= 4.5 THEN 'Excellent'
        WHEN rating >= 4.0 THEN 'Very Good'
        WHEN rating >= 3.5 THEN 'Good'
        WHEN rating >= 3.0 THEN 'Average'
        ELSE 'Below Average'
    END as rating_category
FROM restaurants
WHERE rating IS NOT NULL
ORDER BY rating DESC, name ASC
LIMIT 5;


SELECT 
    id,
    name,
    address,
    phone_number,
    rating,
    rating - (SELECT AVG(rating) FROM restaurants WHERE rating IS NOT NULL) as above_average,
    PERCENT_RANK() OVER (ORDER BY rating) as percentile_rank
FROM restaurants
WHERE rating IS NOT NULL
ORDER BY rating DESC, name ASC
LIMIT 5;


EXPLAIN ANALYZE 
SELECT id, name, address, phone_number, rating
FROM restaurants
WHERE rating IS NOT NULL
ORDER BY rating DESC, name ASC
LIMIT 5;


SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE tablename = 'restaurants';


SELECT 
    COUNT(*) as total_restaurants,
    COUNT(rating) as restaurants_with_ratings,
    ROUND(AVG(rating), 2) as average_rating,
    MIN(rating) as min_rating,
    MAX(rating) as max_rating,
    COUNT(*) FILTER (WHERE is_active = true) as active_restaurants
FROM restaurants;


ANALYZE restaurants;

VACUUM ANALYZE restaurants;

SELECT 
    pg_size_pretty(pg_total_relation_size('restaurants')) as total_size,
    pg_size_pretty(pg_relation_size('restaurants')) as table_size,
    pg_size_pretty(pg_total_relation_size('restaurants') - pg_relation_size('restaurants')) as indexes_size;


DO $$
DECLARE
    result_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO result_count
    FROM (
        SELECT id
        FROM restaurants
        WHERE rating IS NOT NULL
        ORDER BY rating DESC, name ASC
        LIMIT 5
    ) subquery;
    
    IF result_count = 5 THEN
        RAISE NOTICE 'SUCCESS: Query returns exactly 5 restaurants';
    ELSE
        RAISE NOTICE 'WARNING: Query returns % restaurants instead of 5', result_count;
    END IF;
END $$;

WITH top_restaurants AS (
    SELECT rating, name,
           LAG(rating) OVER (ORDER BY rating DESC, name ASC) as prev_rating
    FROM restaurants
    WHERE rating IS NOT NULL
    ORDER BY rating DESC, name ASC
    LIMIT 5
)
SELECT 
    CASE 
        WHEN COUNT(*) FILTER (WHERE rating > prev_rating) = 0 
        THEN 'SUCCESS: Results are properly ordered'
        ELSE 'ERROR: Results are not properly ordered'
    END as order_check
FROM top_restaurants;
