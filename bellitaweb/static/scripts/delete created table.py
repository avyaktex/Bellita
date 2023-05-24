import sqlite3

# Connect to the database
conn = sqlite3.connect('BellitaSalon.db')
cursor = conn.cursor()

# Define the table name you want to delete
table_name = 'bellitaweb_service_list'

# Execute the DROP TABLE statement
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Commit the changes
conn.commit()

# Close the connection
conn.close()