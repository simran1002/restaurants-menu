# Database Management - PostgreSQL Query Solution

## Problem Statement
Given a PostgreSQL database with a restaurants table, write an SQL query to find the top 5 highest-rated restaurants.

## Solution

### Main Query
```sql
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
```

## Query Explanation

### 1. **SELECT Clause**
- Retrieves essential restaurant information including `id`, `name`, `address`, `phone_number`, and `rating`
- Uses specific column selection instead of `SELECT *` for better performance

### 2. **WHERE Clause**
- `rating IS NOT NULL` ensures we only consider restaurants that have been rated
- Prevents NULL values from affecting the results

### 3. **ORDER BY Clause**
- `rating DESC` sorts restaurants by rating in descending order (highest first)
- `name ASC` provides consistent tie-breaking when multiple restaurants have the same rating
- Ensures deterministic results across multiple query executions

### 4. **LIMIT Clause**
- Restricts results to exactly 5 restaurants
- PostgreSQL's LIMIT is efficient and stops processing once the required number of rows is found

## Performance Optimizations

### Recommended Indexes

#### 1. Single Column Index
```sql
CREATE INDEX idx_restaurants_rating ON restaurants(rating DESC);
```
- Optimizes the ORDER BY rating DESC operation
- Significantly improves query performance for large datasets

#### 2. Composite Index (Recommended)
```sql
CREATE INDEX idx_restaurants_rating_name ON restaurants(rating DESC, name ASC);
```
- Covers both sorting columns in the exact order used in the query
- Provides optimal performance for the complete ORDER BY clause
- Eliminates the need for additional sorting operations

#### 3. Partial Index (For Active Restaurants)
```sql
CREATE INDEX idx_restaurants_rating_active ON restaurants(rating DESC, name ASC) 
WHERE is_active = true;
```
- Use this if you have an `is_active` column and want to exclude inactive restaurants
- Smaller index size and better performance for filtered queries

### Query Performance Characteristics

1. **Time Complexity**: O(log n) with proper indexing
2. **Space Complexity**: O(1) - only returns 5 rows regardless of table size
3. **Index Usage**: Can use index-only scans with composite index
4. **Scalability**: Performance remains consistent even with millions of restaurants

## Alternative Queries

### Enhanced Query with Rating Categories
```sql
SELECT 
    r.id,
    r.name,
    r.address,
    r.phone_number,
    r.rating,
    ROUND(r.rating, 2) as formatted_rating,
    CASE 
        WHEN r.rating >= 4.5 THEN 'Excellent'
        WHEN r.rating >= 4.0 THEN 'Very Good'
        WHEN r.rating >= 3.5 THEN 'Good'
        WHEN r.rating >= 3.0 THEN 'Average'
        ELSE 'Below Average'
    END as rating_category
FROM restaurants r
WHERE r.rating IS NOT NULL
ORDER BY r.rating DESC, r.name ASC
LIMIT 5;
```

### Query with Ranking
```sql
SELECT 
    id,
    name,
    address,
    phone_number,
    rating,
    RANK() OVER (ORDER BY rating DESC) as rank
FROM restaurants
WHERE rating IS NOT NULL
ORDER BY rating DESC, name ASC
LIMIT 5;
```

## Database Schema Assumptions

Based on the Django model from the backend implementation, the `restaurants` table structure:

```sql
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    rating DECIMAL(3,2) CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing the Query

### Sample Data
```sql
INSERT INTO restaurants (name, address, phone_number, rating) VALUES
('The Golden Spoon', '123 Main St, City', '+1-555-0101', 4.8),
('Pasta Paradise', '456 Oak Ave, City', '+1-555-0102', 4.7),
('Burger Barn', '789 Pine St, City', '+1-555-0103', 4.6),
('Sushi Sensation', '321 Elm St, City', '+1-555-0104', 4.9),
('Pizza Palace', '654 Maple Ave, City', '+1-555-0105', 4.5),
('Taco Town', '987 Cedar St, City', '+1-555-0106', 4.4),
('Curry Corner', '147 Birch St, City', '+1-555-0107', 4.3);
```

### Expected Results
The query should return:
1. Sushi Sensation (4.9)
2. The Golden Spoon (4.8)
3. Pasta Paradise (4.7)
4. Burger Barn (4.6)
5. Pizza Palace (4.5)

## Production Considerations

1. **Monitoring**: Use `EXPLAIN ANALYZE` to monitor query performance
2. **Caching**: Consider caching results if this is a frequently accessed query
3. **Pagination**: For web applications, implement pagination for better UX
4. **Data Validation**: Ensure rating values are within expected range (0-5)
5. **Null Handling**: The query properly handles NULL ratings

## Conclusion

This solution provides an efficient, scalable SQL query that correctly identifies the top 5 highest-rated restaurants while maintaining optimal performance through proper indexing strategies. The query is production-ready and handles edge cases appropriately.
