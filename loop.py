

# imports
from acitoolkit.acitoolkit import *
import requests
import json
import sys
import openpyxl
import os
from sparkjc import writeMessage

# variable
base_url = 'http://10.50.0.138/api/'


""" This section is related to clean the tenant, login APIC, etc """

# First create an instance of the Credentials class
description = "acitoolkit tenant_creation"
creds = Credentials('apic_Madlab', description)

# Retrieve the credentials from the file
apic_credentials = creds.get()

# Login to APIC
session = Session("http://10.50.0.138", apic_credentials.login, apic_credentials.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

""" This section is related to get names from the excell """

wb = openpyxl.load_workbook('app/shared/tenant-parametros.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')
t_name = sheet['A2']
anp_name = sheet['C2']
epg_web_name = sheet['D2']
contract_web_name = sheet['F2']
data_url = "http://10.50.0.138/api/node/mo/uni/%s.json" % ("tn-" + t_name.value)
print ("Suscripcion-->" + " tenant:" + t_name.value + ",   anp:" + anp_name.value + "   ,epg:" + epg_web_name.value)


""" This section is related to subscribe if a microEPG is created """


my_tenant = Tenant(t_name.value)
my_app = AppProfile(anp_name.value, my_tenant)
my_epg = EPG(epg_web_name.value, my_app)
my_tenant.subscribe(session, only_new=True)
my_app.subscribe(session, only_new=True)
my_epg.subscribe(session, only_new=True)

""" This section is related to the contracts for remediation """


def consume_contract():
    name_pwd = {'aaaUser': {'attributes': {'name': 'security', 'pwd': 'Security123'}}}
    json_credentials = json.dumps(name_pwd)
    # log in to API
    my_session = requests.session()
    login_url = base_url + 'aaaLogin.json'
    login_response = my_session.post(login_url, data=json_credentials)
    # print login_response
    # Post to provide the apic with json
    datos = {"fvRsProv":{"attributes":{"dn":"uni/%s/%s/epg-remediacion/rsprov-remediacion" % ("tn-" + t_name.value, "ap-" + anp_name.value),"matchT":"AtleastOne","prio":"unspecified","tnVzBrCPName":"remediacion"}}}
    json_datos = json.dumps(datos)
    # print datos
    r = my_session.post(data_url, data=json_datos)

    datos = {"fvRsProv":{"attributes":{"dn":"uni/%s/%s/%s/%s" % ("tn-" + t_name.value, "ap-" + anp_name.value, "epg-quarantine-" + epg_web_name.value, "rsprov-" + contract_web_name.value),"matchT":"AtleastOne","prio":"unspecified","tnVzBrCPName":contract_web_name.value}}}
    json_datos = json.dumps(datos)
    # print datos
    r = my_session.post(data_url, data=json_datos)



    # Post to consume the apic with json
    datos = {"fvRsCons":{"attributes":{"dn":"uni/%s/%s/%s/rscons-remediacion" % ("tn-" + t_name.value, "ap-" + anp_name.value, "epg-quarantine-" + epg_web_name.value),"prio":"unspecified","tnVzBrCPName":"remediacion"}}}
    json_datos = json.dumps(datos)
    r = my_session.post(data_url, data=json_datos)
    print "\n" + "ALARMA se ha puesto en Cuarentena el servidor Web" + "\n"
    writeMessage("\n" + "ALARMA se ha puesto en Cuarentena el servidor Web" + "\n")
    # print r.text


""" This section is related to subscribe if a microEPG is created """

def main():
  quarantine = False
  while quarantine == False:
    if my_epg.has_events(session):
      epg = my_epg.get_event(session)
      if epg.name == "quarantine-" + epg_web_name.value:
        quarantine = True
        if epg.is_deleted():
            # print "\n"
            # print('EPG', epg.name, 'has been deleted.')
            a = 1
        else:
            print "\n"
            print('EPG', epg.name, 'has been created or modified.')
            consume_contract()

while True:
  main()
