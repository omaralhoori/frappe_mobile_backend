from __future__ import unicode_literals
import frappe
import requests


URL = 'http://194.165.141.2:8888/reports/rwservlet?report=DGR02STDPE_RET&userid=MOBUSR/RET_2015ACD@INFRA&DESFORMAT=PDF&DESTYPE=Cache&PERCENFLG=1&STDTRNFLG=1&CONCATMATFLG=2&CONCATMATFLG_DTL=0&SUMPERDIPFLG=2&STDFLG=2'

@frappe.whitelist(allow_guest=True)
def get_report():
    #settings = frappe.get_single("School Settings")

    #report = frappe.form_dict.report
    
    year = frappe.form_dict.year
    all_periods = frappe.form_dict.all_periods
    class_no = frappe.form_dict.class_no
    division_no =  frappe.form_dict.division_no
    branch_no = frappe.form_dict.branch_no
    period = frappe.form_dict.period
    semester= frappe.form_dict.semester
    contract_no = frappe.form_dict.contract_no
    student_no = frappe.form_dict.student_no
    report = "DGR02STDA_MN2" if int(semester) == 9 else "DGR02STD_MN2"
    # print(all_periods, period, semester, report)
    #url = f"{settings.data_url}/reports/rwservlet?report={report}&userid={settings.user_id}&PERCENFLG=1&STDTRNFLG=1&CONCATMATFLG=2&CONCATMATFLG_DTL=0&SUMPERDIPFLG=2&STDFLG=2&PYEAR={year}&PALLPER={all_periods}&PCLASS={class_no}&PDIV={division_no}&PBRN={branch_no}&PPER={period}&PSEM={semester}&STDBRN={branch_no}&STDCON={contract_no}&STDNO={student_no}"
    options = frappe.db.sql(f"""
        SELECT hide_percentage, merge_subjects, merge_subjects_with_details, hide_total FROM `tabSchool Class`
        WHERE name='{class_no}'
    """, as_dict=True)
    hide_percentage, merge_subjects, merge_subjects_with_details, hide_total= 1, 2, 0, 2
    if len(options) > 0:
        hide_percentage = get_results_options('hide_percentage', options[0]['hide_percentage'])
        merge_subjects = get_results_options('merge_subjects', options[0]['merge_subjects'])
        merge_subjects_with_details = get_results_options('merge_subjects_with_details', options[0]['merge_subjects_with_details'])
        hide_total = get_results_options('hide_total', options[0]['hide_total'])

    url = f"http://46.185.139.178:7778/reports/rwservlet?report={report}&userid=MOBUSR/M0B_2O20_Y5N@manar&DESFORMAT=PDF&DESTYPE=Cache&PERCENFLG={hide_percentage}&STDTRNFLG=1&CONCATMATFLG={merge_subjects}&CONCATMATFLG_DTL={merge_subjects_with_details}&SUMPERDIPFLG={hide_total}&STDFLG=2&PYEAR={year}&PALLPER={all_periods}&PCLASS={class_no}&PDIV={division_no}&PBRN={branch_no}&PPER={period}&PSEM={semester}&STDBRN={branch_no}&STDCON={contract_no}&STDNO={student_no}"
    # print(url)
    res = requests.get(url)
    frappe.local.response.filename = "Degree Report"
    frappe.local.response.filecontent = res.content #get_pdf(html)
    frappe.local.response.type = "pdf"

def get_results_options(option_name, option):
    if option_name == 'merge_subjects_with_details':
        return 1 if option else 0
    else:
        return 1 if option else 2