from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.pdf import get_pdf
import requests
from xml.etree import ElementTree
import pdfkit

def get_or_create_user(user):
    if frappe.session.user == 'Guest' and user:
        res = frappe.db.get_value("Mobile Guest", user, ["name","is_active"])
        if res:
            name, is_active = res
            if is_active == 1:
                return name
            else: return frappe.throw("You are not allowed to use the system.")
        else:
            user_doc = frappe.get_doc({
                "doctype": "Mobile Guest",
                "device_id": user
            })
            user_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return user_doc.name
    else:
        return frappe.session.user


@frappe.whitelist()
def get_transactions_pdf():
    if frappe.session.user == "Guest":
        frappe.throw(_("You are not permitted to access this page."), frappe.PermissionError)
    branch=frappe.local.form_dict.PBRN
    year=frappe.local.form_dict.PYEAR
    contract=frappe.local.form_dict.PCONNO
    student=frappe.local.form_dict.PSTD
    parent = frappe.db.get_value("School Parent", {"branch":branch, "year": year, "contract_no": contract}, ["name"])
    if not parent:#not(branch and year and contract):
        frappe.throw(_("Not found."), frappe.DoesNotExistError)
    if (parent != frappe.session.user and
        frappe.db.get_value("User", frappe.session.user, "user_type")=="Website User"):
        frappe.throw(_("You are not permitted to access this page."), frappe.PermissionError)
    if student:
        url = 'http://202.147.198.58:8888/reports/rwservlet?report=STRMOBBAL&userid=MOBUSR/F1T_2O21_Y5N@SCHOOLDB&PBRN={}&PYEAR={}&PCONNO={}&PSTD={}'.format(branch, year, contract, student)
    else:
        url = 'http://202.147.198.58:8888/reports/rwservlet?report=STRMOBBAL&userid=MOBUSR/F1T_2O21_Y5N@SCHOOLDB&PBRN={}&PYEAR={}&PCONNO={}'.format(branch, year, contract)
    res = requests.get(url.format(branch, year, contract))
    tree = ElementTree.fromstring(res.content)
    parent = tree.find("Parent")
    students = parent.findall("Student")
    student_list = []
    for student in students:
        transactions = get_transactions(student.find('StudentTransaction'))
        extra_amount = get_extra_amounts(student.find('StudentExtraAmount'))
        installments = get_installments(student.find('StudentInstallment'))
        fees = get_fees(student.find('StudentFees'))
        student_list.append({
            "STDNO": student.find("STDNO").text,
            "STDNAME": student.find("STDNAME").text,
            "STDGENDER": student.find("STDGENDER").text,
            "CLSCODE": student.find("CLSCODE").text,
            "CLSNAME": student.find("CLSNAME").text,
            "SECCODE": student.find("SECCODE").text,
            "SECNAME": student.find("SECNAME").text,
            "StudentTransaction": transactions,
            "StudentExtraAmount": extra_amount,
            "StudentInstallment": installments,
            "StudentFees": fees,
        })
    YEARNAME = parent.find('YEARNAME').text
    BRNNAME = frappe.db.get_value("School Branch", parent.find('BRNCODE').text, ["branch_name"])
    BRNCODE = parent.find('BRNCODE').text
    CONNO = parent.find('CONNO').text
    CONNAME = parent.find('CONNAME').text
    #hosturl = frappe.utils.()
    html = frappe.render_template('templates/transaction_report.html', {
        "student_list": student_list,
        "YEARNAME": YEARNAME,
        "BRNNAME": BRNNAME,
        "BRNCODE": BRNCODE,
        "CONNO": CONNO,
        "CONNAME": CONNAME,
        "hosturl": "http://{}:8000".format(frappe.local.site),
    }) #response.content
    name = branch+"-"+ year + "-" + contract + ".html"
    # with open( name.replace("/", "-"), "w+") as f:
    #     f.write(html)
    frappe.local.response.filename = name
    frappe.local.response.filecontent = pdfkit.from_string(html, False) #get_pdf(html)
    frappe.local.response.type = "pdf"



def get_transactions(student_transaction):
    transactions = []
    for transaction in student_transaction.findall('Transaction'):
        transactions.append({
            'TRXCODE': transaction.find('TRXCODE').text,
            'TRXNAME': transaction.find('TRXNAME').text,
            'TRXVOUCHER': transaction.find('TRXVOUCHER').text,
            'TRXDATE': transaction.find('TRXDATE').text,
            'TRXNOTE': transaction.find('TRXNOTE').text,
            'TRXAMT': transaction.find('TRXAMT').text,
        })
    return transactions

def get_extra_amounts(student_extra_amount):
    extra_amounts = []
    for amount in student_extra_amount.findall('ExtraAmount'):
        extra_amounts.append({
            'TRXEXCODE': amount.find('TRXEXCODE').text,
            'TRXEXNAME': amount.find('TRXEXNAME').text,
            'TRXEXVOUCHER': amount.find('TRXEXVOUCHER').text,
            'TRXEXDATE': amount.find('TRXEXDATE').text,
            'TRXEXNOTE': amount.find('TRXEXNOTE').text,
            'TRXEXAMT': amount.find('TRXEXAMT').text,
        })
    return extra_amounts

def get_installments(stdent_installments):
    installments = []
    for amount in stdent_installments.findall('InstallmentAmount'):
        installments.append({
            'PAYNO': amount.find('PAYNO').text,
            'PAYDATE': amount.find('PAYDATE').text,
            'PAYAMT': amount.find('PAYAMT').text,
            'PAYPAID': amount.find('PAYPAID').text,
            'PAYBAL': amount.find('PAYBAL').text,
        })
    return installments

def get_fees(student_fees):
    fees = []
    for fee in student_fees.findall('FeesAmount'):
        fees.append({
            'FEECODE': fee.find('FEECODE').text,
            'FEENAME': fee.find('FEENAME').text,
            'AMTFEE': fee.find('AMTFEE').text,
            'AMFDSC': fee.find('AMFDSC').text,
            'AMTTOT': fee.find('AMTTOT').text,
            'AMTPAID': fee.find('AMTPAID').text,
            'AMTBAL': fee.find('AMTBAL').text,
        })
    return fees