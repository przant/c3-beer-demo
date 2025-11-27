-- Create beers table
CREATE TABLE IF NOT EXISTS beers (
    id SERIAL PRIMARY KEY,
    beer_name VARCHAR(255) NOT NULL,
    beer_style VARCHAR(100) NOT NULL,
    abv DECIMAL(4,2) NOT NULL,
    ibu INTEGER NOT NULL,
    brewery_name VARCHAR(255) NOT NULL,
    brewery_location VARCHAR(255) NOT NULL
);

-- Load data from CSV (PostgreSQL will look for this file in the mounted volume)
-- The COPY command expects the file to be accessible to the PostgreSQL server
COPY beers(beer_name, beer_style, abv, ibu, brewery_name, brewery_location)
FROM '/docker-entrypoint-initdb.d/beers.csv'
DELIMITER ','
CSV HEADER;

-- Create indexes for common query patterns
CREATE INDEX idx_beer_style ON beers(beer_style);
CREATE INDEX idx_brewery_name ON beers(brewery_name);

-- Verify data loaded
SELECT COUNT(*) as total_beers FROM beers;
SELECT DISTINCT beer_style FROM beers ORDER BY beer_style;
