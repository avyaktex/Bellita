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
        cursor.execute(f"INSERT INTO {table_name} (ser_id, ser_name, ser_duration, ser_price) VALUES (?, ?, ?, ?)",
                       (item['serId'], item['serName'], item['serDuration'], item['serPrice']))
    conn.commit()
    conn.close()

db_file_path = "D:\\Bellita\\Bellitathesalon\\BellitaSalon\\db.sqlite3"
json_file_path = "D:\\Bellita\\Bellitathesalon\\BellitaSalon\\bellitaweb\\static\\json\\services.json"
table_name = 'bellitaweb_service'
convert_json_to_database(json_file_path,db_file_path,table_name)