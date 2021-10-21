import frappe

def execute():
    try:
        frappe.db.sql('''
        ALTER TABLE `tabUser` ADD COLUMN device_token VARCHAR(140);
        ''')
    except:
        pass