# list_tables.py

# Import Django settings and setup
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ezshop.settings")
django.setup()

# Import Django models
from django.db import connection
from django.apps import apps

# Function to list all tables in the database
def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return [table[0] for table in tables]

# Function to clear all data in each table
def clear_data():
    for model in apps.get_models():
        table_name = model._meta.db_table
        try:
            model.objects.all().delete()
            print(f"All data cleared from table: {table_name}")
        except Exception as e:
            print(f"Failed to clear data from table: {table_name}. Error: {e}")

# Main function to execute the script
if __name__ == "__main__":
    tables = list_tables()
    print("Tables in the database:")
    for table in tables:
        print(table)

    # Ask for confirmation before clearing data
    confirm = input("Do you want to clear all data in these tables? (yes/no): ")
    if confirm.lower() == "yes":
        clear_data()
        print("All data cleared successfully.")
    else:
        print("No data cleared.")
