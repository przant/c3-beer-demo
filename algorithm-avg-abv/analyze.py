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

def analyze_avg_abv():
    """Calculate average ABV (alcohol by volume) by beer style"""
    
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
    
    # Query to calculate average ABV by style
    query = """
        SELECT 
            beer_style,
            ROUND(AVG(abv), 2) as avg_abv,
            COUNT(*) as beer_count
        FROM beers
        GROUP BY beer_style
        ORDER BY avg_abv DESC;
    """
    
    # Use pandas to make results pretty
    df = pd.read_sql_query(query, conn)
    
    print("\n" + "="*60)
    print("AVERAGE ABV BY BEER STYLE")
    print("="*60)
    print(df.to_string(index=False))
    print("="*60)
    
    # Find the strongest style
    strongest = df.iloc[0]
    print(f"\n🍺 Strongest style: {strongest['beer_style']} at {strongest['avg_abv']}% ABV")
    print(f"   (based on {int(strongest['beer_count'])} beers)")
    
    conn.close()
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    analyze_avg_abv()
