import json
import sqlite3
from django.conf import settings
settings.configure()

def convert_json_to_database(json_file_path, db_file_path, table_name):
    with open(json_file_path) as file:
        json_data = json.load(file)
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    for item in json_data:
        cursor.execute(f"INSERT INTO {table_name} (name, price, service_time, gender, category) VALUES (?, ?, ?, ?, ?)",
                       (item['Name'], item['Price'], item['Service time'], item['Gender'], item['Category']))
    conn.commit()
    conn.close()

db_file_path = "D:\\Avyakt\\Bellita\\db.sqlite3"
json_file_path = "D:\\Avyakt\\Bellita\\bellitaweb\\static\\json\\services_by_category.json"
table_name = 'bellitaweb_services_by_cat'
convert_json_to_database(json_file_path,db_file_path,table_name)