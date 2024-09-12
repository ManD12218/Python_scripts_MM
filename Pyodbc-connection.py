import pyodbc

# Database connection details
server = 'medminellc.database.windows.net'  # Replace with your server name
database = 'MedMine'  # Replace with your database name
username = 'Mandeep'  # Replace with your username
password = '0J2x8VVv4b'  # Replace with your password
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure the correct driver is installed

# Establishing connection
conn = pyodbc.connect(
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
cursor = conn.cursor()

# Fetching table names from ra.tickers
fetch_tables_query = "SELECT ticker FROM ra.tickers"
cursor.execute(fetch_tables_query)
tables = cursor.fetchall()

# Loop over each table and update the NULL values
for table in tables:
    table_name = table[0]  # Assuming the table_name is the first column in ra.tickers

    update_query = f"""
        UPDATE ra.map_{table_name}
        SET [Group] = REPLACE([Group], 'OtherOther', 'Other'),
            Business = REPLACE(Business, 'OtherOther', 'Other'),
            Division = REPLACE(Division, 'OtherOther', 'Other'),
            Therapy = REPLACE(Therapy, 'OtherOther', 'Other'),
            Specialty = REPLACE(Specialty, 'OtherOther', 'Other'),
            Anatomy = REPLACE(Anatomy, 'OtherOther', 'Other'),
            Subanatomy = REPLACE(Subanatomy, 'OtherOther', 'Other')
        WHERE [Group] LIKE '%OtherOther%'
        OR Business LIKE '%OtherOther%'
        OR Division LIKE '%OtherOther%'
        OR Therapy LIKE '%OtherOther%'
        OR Specialty LIKE '%OtherOther%'
        OR Anatomy LIKE '%OtherOther%'
        OR Subanatomy LIKE '%OtherOther%';
        """

    try:
        # Executing the update query for each table
        cursor.execute(update_query)
        conn.commit()  # Commit after each table update
        print(f"Update completed for table: {table_name}")
    except Exception as e:
        print(f"An error occurred while updating table {table_name}: {e}")

# Closing the connection
cursor.close()
conn.close()

print("All updates are completed.")
