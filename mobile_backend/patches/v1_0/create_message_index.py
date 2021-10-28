import frappe

def execute():
    index_key = frappe.db.sql('''SHOW INDEX FROM `tabSchool Parent Message` WHERE Key_name='Message_Index';''')
    if not index_key or len(index_key) == 0:
        #frappe.db.sql('''ALTER TABLE `tabSchool Parent Message` DROP INDEX Message_Index;''')
        frappe.db.sql('''
            CREATE UNIQUE INDEX Message_Index
                ON `tabSchool Parent Message`(message_type,parent,message_name,student)
        ''')