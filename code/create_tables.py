import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name text, last_name text, username text email text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS users (meeting_id INTEGER PRIMARY KEY, created_on TIMESTAMP, start_time time, end_time time, subject text, created_by text)"
cursor.execute(create_table)

connection.commit()
connection.close()