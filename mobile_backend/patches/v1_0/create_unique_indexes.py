import frappe

def execute():
    view_key = frappe.db.sql('''SHOW INDEX FROM `tabMobile View` WHERE Key_name='View_Index';''')
    if not view_key or len(view_key) == 0:
        #frappe.db.sql('''ALTER TABLE `tabMobile View` DROP INDEX View_Index;''')
        frappe.db.sql('''
            CREATE UNIQUE INDEX View_Index
                ON `tabMobile View`(parenttype,parent,user)
        ''')
    like_key = frappe.db.sql('''SHOW INDEX FROM `tabMobile Like` WHERE Key_name='Like_Index';''')
    if not like_key or len(like_key) == 0:
        frappe.db.sql('''
            CREATE UNIQUE INDEX Like_Index
                ON `tabMobile Like`(parenttype,parent,user)
        ''')