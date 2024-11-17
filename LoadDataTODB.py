import sqlite3
import pandas as pd

# File paths
csv_file = 'AirData.csv'  # Replace with the path to your CSV file
sqlite_db = 'AirData.db'  # SQLite database name

# Table name
table_name = 'PollutantHistory'

# Step 1: Load the CSV into a Pandas DataFrame
try:
    df = pd.read_csv(csv_file)
    print("CSV loaded successfully!")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()

# Step 2: Connect to SQLite database (it will create the file if it doesn't exist)
try:
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    print(f"Connected to SQLite database at {sqlite_db}")
except Exception as e:
    print(f"Error connecting to SQLite database: {e}")
    exit()

# Step 3: Define the table schema with explicit column names and types
table_schema = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    latitude REAL,
    longitude REAL,
    city TEXT,
    pollutants TEXT,
    aqi REAL,
    date_local TEXT,
    state TEXT,
    county TEXT,
    arithmetic_mean REAL,
    observation_count INTEGER
);
"""

# Create the table
try:
    cursor.execute(table_schema)
    print(f"Table '{table_name}' created successfully!")
except Exception as e:
    print(f"Error creating table: {e}")
    exit()

# Step 4: Insert data into the table
try:
    # Insert the data using pandas to_sql
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Data successfully loaded into table '{table_name}'.")
except Exception as e:
    print(f"Error loading data into table: {e}")
finally:
    # Close the connection
    conn.close()
    print("Database connection closed.")
