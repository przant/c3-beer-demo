import psycopg2
import pandas as pd
import os
import time

def wait_for_db(host, max_retries=30):
    """Wait for database to be ready"""
    print(f"Waiting for database at {host}...")
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=host,
                database=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD']
            )
            conn.close()
            print("Database is ready!")
            return True
        except psycopg2.OperationalError:
            print(f"Attempt {i+1}/{max_retries}: Database not ready yet...")
            time.sleep(2)
    return False

def analyze_top_breweries():
    """Find top breweries by number of beers produced"""
    
    # Database connection parameters from environment variables
    db_host = os.environ.get('DB_HOST', 'database')
    
    # Wait for database to be ready
    if not wait_for_db(db_host):
        print("ERROR: Database never became ready!")
        return
    
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )
    
    # Query to find most productive breweries
    query = """
        SELECT 
            brewery_name,
            brewery_location,
            COUNT(*) as beer_count,
            ROUND(AVG(abv), 2) as avg_abv,
            ROUND(AVG(ibu), 1) as avg_ibu
        FROM beers
        GROUP BY brewery_name, brewery_location
        ORDER BY beer_count DESC
        LIMIT 10;
    """
    
    # Use pandas to make results pretty
    df = pd.read_sql_query(query, conn)
    
    print("\n" + "="*80)
    print("TOP 10 BREWERIES BY NUMBER OF BEERS")
    print("="*80)
    print(df.to_string(index=False))
    print("="*80)
    
    # Highlight the winner
    top_brewery = df.iloc[0]
    print(f"\n🏆 Most productive brewery: {top_brewery['brewery_name']}")
    print(f"   Location: {top_brewery['brewery_location']}")
    print(f"   Total beers: {int(top_brewery['beer_count'])}")
    print(f"   Average ABV: {top_brewery['avg_abv']}%")
    print(f"   Average IBU: {top_brewery['avg_ibu']}")
    
    conn.close()
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    analyze_top_breweries()
