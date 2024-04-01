import os
import django
import mysql.connector
from django.core.management import call_command
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ezshop.settings')
django.setup()

# Database configuration
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': '3307',
    'database': 'ezshopdb',
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print('Connected to MySQL database')

        # Call Django's management command to create tables
        call_command('migrate')

        print('Migration successful')

        # Close connection
        connection.close()
        print('MySQL connection closed')

except mysql.connector.Error as e:
    print(f'Error connecting to MySQL: {e}')
