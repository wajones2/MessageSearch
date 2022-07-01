import sqlite3

location = "data"
sms_database = "contacts.db"
con = sqlite3.connect(f"{location}/{sms_database}")
cursor = con.cursor()

cursor.execute("""create table if not exists contact (ROWID integer primary key autoincrement, full_name text, phone_number text)""")
cursor.execute("""create table if not exists id_join (contact_id integer primary key autoincrement, handle_id integer)""")


