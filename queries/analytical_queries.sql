
-- Query 1: Top 10 highest-revenue movies
SELECT title, year, revenue
FROM movie_full_view
WHERE revenue IS NOT NULL
ORDER BY revenue DESC
LIMIT 10;

-- Query 2: Top 10 highest-rated movies
SELECT title, year, vote_average
FROM movie_full_view
WHERE vote_average IS NOT NULL
ORDER BY vote_average DESC
LIMIT 10;

-- Query 3: Average rating by year 
SELECT year, ROUND(AVG(vote_average)::numeric, 2) AS avg_rating
FROM movie_full_view
WHERE vote_average IS NOT NULL
GROUP BY year
ORDER BY year;

-- Query 4: Number of movies by year
SELECT year, COUNT(*) AS movie_count
FROM movie_full_view
GROUP BY year
ORDER BY year;

-- Query 5: Most popular movies
SELECT title, year, popularity
FROM movie_full_view
WHERE popularity IS NOT NULL
ORDER BY popularity DESC
LIMIT 10;

-- Query 6: Top distributors by number of movies
SELECT distributor, COUNT(*) AS movie_count
FROM movie_full_view
WHERE distributor IS NOT NULL
GROUP BY distributor
ORDER BY movie_count DESC, distributor;

-- Query 7: Average revenue by year
SELECT year, ROUND(AVG(revenue)::numeric, 2) AS avg_revenue
FROM movie_full_view
WHERE revenue IS NOT NULL
GROUP BY year
ORDER BY year;

-- Check data quality
SELECT
    COUNT(*) AS total_movies,
    COUNT(*) FILTER (WHERE revenue IS NULL) AS missing_revenue,
    COUNT(*) FILTER (WHERE vote_average IS NULL) AS missing_vote_average,
    COUNT(*) FILTER (WHERE popularity IS NULL) AS missing_popularity,
    COUNT(*) FILTER (WHERE distributor IS NULL) AS missing_distributor
FROM movie_full_view;




