
-- Verifying the restored file
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT COUNT(*) AS movies_count FROM movies;
SELECT COUNT(*) AS ratings_count FROM ratings;
SELECT COUNT(*) AS revenue_count FROM revenue;
SELECT COUNT(*) AS reference_info_count FROM reference_info;
SELECT COUNT(*) AS final_stage_count FROM final_dataset_stage;

SELECT * FROM movies LIMIT 5;
SELECT * FROM ratings LIMIT 5;
SELECT * FROM revenue LIMIT 5;
SELECT * FROM reference_info LIMIT 5;

-- Add the missing indexes
CREATE INDEX IF NOT EXISTS idx_movies_title_clean
ON movies(title_clean);

CREATE INDEX IF NOT EXISTS idx_movies_year
ON movies(year);

CREATE INDEX IF NOT EXISTS idx_ratings_movie_id
ON ratings(movie_id);

CREATE INDEX IF NOT EXISTS idx_ratings_vote_average
ON ratings(vote_average);

CREATE INDEX IF NOT EXISTS idx_ratings_popularity
ON ratings(popularity);

CREATE INDEX IF NOT EXISTS idx_revenue_movie_id
ON revenue(movie_id);

CREATE INDEX IF NOT EXISTS idx_revenue_revenue
ON revenue(revenue);

CREATE INDEX IF NOT EXISTS idx_reference_info_movie_id
ON reference_info(movie_id);

CREATE INDEX IF NOT EXISTS idx_reference_info_rank_ref
ON reference_info(rank_ref);

-- Check indexes
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Create one clean query-ready view
CREATE OR REPLACE VIEW movie_full_view AS
SELECT
    m.id,
    m.title,
    m.title_clean,
    m.year,
    r.revenue,
    rt.vote_average,
    rt.popularity,
    ri.rank_ref,
    ri.distributor,
    ri.total_gross_ref,
    ri.theaters_ref,
    ri.release_date_ref
FROM movies m
LEFT JOIN ratings rt
    ON m.id = rt.movie_id
LEFT JOIN revenue r
    ON m.id = r.movie_id
LEFT JOIN reference_info ri
    ON m.id = ri.movie_id;

-- Test the view
SELECT * FROM movie_full_view LIMIT 10;

-- Got duplicates in the test view
-- Fix the issue
-- Find which tables have duplicates
SELECT movie_id, COUNT(*)
FROM ratings
GROUP BY movie_id
HAVING COUNT(*) > 1
ORDER BY COUNT (*) DESC
LIMIT 20;

SELECT movie_id, COUNT(*)
FROM revenue
GROUP BY movie_id
HAVING COUNT(*) > 1
ORDER BY COUNT (*) DESC
LIMIT 20;

SELECT movie_id, COUNT(*)
FROM reference_info
GROUP BY movie_id
HAVING COUNT(*) > 1
ORDER BY COUNT (*) DESC
LIMIT 20;

-- Test again
SELECT * FROM movie_full_view LIMIT 10;

-- Confirm row counts
SELECT COUNT(*) AS movies_rows FROM movies;
SELECT COUNT(*) AS view_rows FROM movie_full_view;

-- Check indexes 
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
