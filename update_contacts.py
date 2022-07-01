import sqlite3
from datetime import datetime
import os


class UpdateContactsDB:
    def __init__(self):

        # get_database
        self.numbers_dict = {}
        self.new_contact_dict = {}
        self.name_dict = {}
        self.number_list = []

        # update_database
        self.contact_dict = {}
        self.get_contact = lambda number: os.popen(f'./get_contact {number}').read()


    def get_chat_database(self):
        location = "data/db"
        sms_database = "chat.db"
        con = sqlite3.connect(f"{location}/{sms_database}")
        cursor = con.cursor()

        cursor.execute("""
            SELECT ROWID,id FROM handle
        """)
        self.phone_numbers = cursor.fetchall()
        self.phone_numbers.sort()

        counter = 0
        for pn in self.phone_numbers:
            self.new_contact_dict[pn[0]] = {}
            self.new_contact_dict[pn[0]]["phone"] = pn[1]   # number
            self.new_contact_dict[pn[0]]["first"] = self.get_contact(pn[1]).strip() # name
            print(f"{counter}/{len(self.phone_numbers)}")
            counter += 1


        for rowid in self.new_contact_dict:
            if '+1' not in self.new_contact_dict[rowid]["first"]:
                self.name_dict[self.new_contact_dict[rowid]["first"]] = self.new_contact_dict[rowid]["phone"]
                print(self.new_contact_dict[rowid]["first"])

        for num in self.name_dict:
            self.number_list.append(self.name_dict[num][2:])

        for num in self.new_contact_dict:
            if self.new_contact_dict[num]['phone'][2:] in self.number_list:
                ncd = self.new_contact_dict[num]
                sms_id = num
                first = ncd['first']
                phone = ncd['phone'][2:]
                self.contact_dict[first] = [phone, sms_id]
                # self.contact_dict[first] = phone
        
        con.close()



    def update_sms_database(self):

        self.location = "data"
        self.sms_database = "contacts.db"
        self.con = sqlite3.connect(f"{self.location}/{self.sms_database}")
        self.cursor = self.con.cursor()


        for idx in self.contact_dict:
            self.cursor.execute(f"""INSERT INTO contact ('full_name', 'phone_number')
            VALUES ("{idx}", "{self.contact_dict[idx][0]}")""")

            self.cursor.execute(f"""INSERT INTO id_join ('handle_id')
            VALUES ({self.contact_dict[idx][1]})""")

        self.con.commit()


sl = UpdateContactsDB()
sl.get_chat_database()
sl.update_sms_database()
