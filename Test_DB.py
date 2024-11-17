import sqlite3

# Database file
sqlite_db = 'AirData.db'
table_name = 'PollutantHistory'

# Query to fetch the 'arithmetic_mean' column
query = f"SELECT distinct pollutants FROM {table_name} "

# Connect to the database
try:
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Display the fetched data
    print(f"Arithmetic Mean values from table '{table_name}':")
    for row in rows:
        print(row[0])  # row[0] because we are selecting a single column
except Exception as e:
    print(f"Error querying the database: {e}")
finally:
    conn.close()
    print("Database connection closed.")
