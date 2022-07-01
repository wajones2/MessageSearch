import sqlite3
from datetime import datetime
import os

class xMessages:
    def __init__(self):
        
        os.popen('./update_sms')    # Updates Messages database

        # 'contacts.db'
        self.database_c = "data/contacts.db"
        self.con = sqlite3.connect(f"{self.database_c}")
        self.cursor = self.con.cursor()

        # 'chat.db'
        self.database_sms = "data/db/chat.db"
        self.chat_con = sqlite3.connect(f"{self.database_sms}")
        self.chat_cursor = self.chat_con.cursor()


        self.contact_dict = {} 
        self.id_join_dict = {}
        self.data_dict = {}

        self.search_contact = ''
        self.query_list = ''

        self.convert_timestamp = lambda timestamp: datetime.fromtimestamp(timestamp/1000000000 + 978307200)
        self.format_time = lambda converted_timestamp: datetime.strftime(converted_timestamp, '%a, %b %d, %Y, %-I:%-M %p')
        self.formtime = lambda timestamp: self.format_time(self.convert_timestamp(timestamp))

    def get_contacts_temporary(self):
        self.cursor.execute(f"""
            SELECT * FROM contact
        """)
        self.contact_list = self.cursor.fetchall()

        for contact in self.contact_list:
            self.contact_dict[contact[0]] = [contact[1], contact[2]]

        self.cursor.execute(f"""
            SELECT * FROM id_join
        """)
        self.id_join_list = self.cursor.fetchall()

        for idx in self.id_join_list:
            self.id_join_dict[idx[0]] = idx[1]

        for contact in self.contact_dict:
            contact_id = contact
            handle_id = self.id_join_dict[contact]
            name = self.contact_dict[contact][0]
            number = self.contact_dict[contact][1]

            self.data_dict[name] = {}
            self.data_dict[name]['number'] = number
            self.data_dict[name]['handle_id'] = handle_id
            self.data_dict[name]['contact_id'] = contact_id

        self.names_list = [name for name in self.data_dict.keys()]

    def message_search(self, contact, keywords):
        print('\x1b[3J\x1b[H\x1b[2J')
        self.keywords = keywords
        self.not_exact_contact = self.not_exact(contact)

        if contact == self.search_contact or self.not_exact_contact == self.search_contact:
            for text in self.query_list:
                if text[0] == None:
                    pass
                elif keywords.lower() in text[0].lower():
                    if text[2] == 0:
                        print('\033[1;31;1m• \033[1;31;0m' + self.formtime(text[1]) + '\n', text[0] + '\n')
                    elif text[2] == 1:
                        print('\033[1;32;1m• \033[1;32;0m' + self.formtime(text[1]) + '\n', text[0] + '\n')


        else:
            self.message_query(contact)


    def not_exact(self, check_contact):

        names = []
        name_count = 0
        for name in self.names_list:
            if check_contact.lower() in name.lower() and len(check_contact.lower().split()[0])/len(name.lower().split()[0]) >= 0.5:
                names.append(name)
                name_count += 1
        if name_count > 1:
            print("Enter contact #:\n")
            for idx in range(len(names)):
                print([idx+1], names[idx])
            self.duplicate_selected = int(input('\n')) - 1
            self.not_exact_contact = names[self.duplicate_selected]
            return self.not_exact_contact
        elif name_count == 1:
            self.not_exact_contact = names[0]
            return self.not_exact_contact
        else:
            self.not_exact_contact = ''
            return self.not_exact_contact


    def message_query(self, contact):

        if self.not_exact != '':
            self.search_contact = self.not_exact_contact
        

            self.chat_cursor.execute(f"""
                SELECT text,date,is_from_me FROM message
                WHERE handle_id = {self.data_dict[self.search_contact]['handle_id']}
            """)
            self.query_list = self.chat_cursor.fetchall()

            for text in self.query_list:
                if text[0] == None:
                    pass
                elif self.keywords.lower() in text[0].lower():
                    if text[2] == 0:
                        print('\033[1;31;1m• \033[1;31;0m' + self.formtime(text[1]) + '\n', text[0] + '\n')
                    elif text[2] == 1:
                        print('\033[1;32;1m• \033[1;32;0m' + self.formtime(text[1]) + '\n', text[0] + '\n')

        else:
            print("Contact doesn't exist!\n")


xm = xMessages()
xm.get_contacts_temporary()
