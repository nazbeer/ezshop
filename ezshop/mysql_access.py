import mysql.connector

# Database configuration
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'ezshopdb',
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print('Connected to MySQL database')

        # Create a cursor object to execute queries
        cursor = connection.cursor()

        # Get all table names in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Iterate over tables
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")

            # Fetch all rows from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Print fetched rows
            for row in rows:
                print(row)

        # Close cursor and connection
        cursor.close()
        connection.close()
        print('MySQL connection closed')

except mysql.connector.Error as e:
    print(f'Error connecting to MySQL: {e}')
