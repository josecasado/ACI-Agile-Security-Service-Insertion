# imports

import os
import requests
import json
import sys
import openpyxl
from sparkjc import writeMessage

# vars
base_url = "http://10.50.0.138/api/"
global device
device = {}
apic_password = "password"

# function to read the excel with the tenant parametes


def excel():
    wb = openpyxl.load_workbook('app/shared/tenant-parametros.xlsx')
    sheet = wb.get_sheet_by_name('Sheet1')
    global t_name
    t_name = sheet['A2']
    vrf_name = sheet['B2']
    anp_name = sheet['C2']
    epg_web_name = sheet['D2']
    epg_app_name = sheet['E2']
    contract_web_name = sheet['F2']
    subject_web_name = sheet['G2']
    contract_bd_name = sheet['H2']
    subject_bd_name = sheet['I2']
    l3out_name = sheet['J2']
    l3out_epg_name = sheet['K2']
    # print l3out_name.value
    # print l3out_epg_name.value
    device["tn-t_name"] = "tn-" + t_name.value
    device["vrf_name"] = vrf_name.value
    device["anp_name"] = anp_name.value
    device["epg_web_name"] = epg_web_name.value
    device["epg_app_name"] = epg_app_name.value
    device["contract_web_name"] = contract_web_name.value
    device["subject_web_name"] = subject_web_name.value
    device["contract_bd_name"] = contract_bd_name.value
    device["subject_bd_name"] = subject_bd_name.value
    device["l3out_name"] = l3out_name.value
    device["l3out_epg_name"] = l3out_epg_name.value

# create credentials structure and login into apic

def login():
        name_pwd = {'aaaUser': {'attributes': {'name': 'security', 'pwd': apic_password}}}
        json_credentials = json.dumps(name_pwd)
        global my_session
        my_session = requests.session()
        login_url = base_url + 'aaaLogin.json'
        login_response = my_session.post(login_url, data=json_credentials)

# function to replace the json.config with the tenant parameters


def replace_words(base_text, device_values):
    for key, val in device_values.items():
        base_text = base_text.replace(key, val)
    return base_text

# function to create the output file with all the tenant parameters to send to apic

def create_output(file):
    t = open(file, 'r')
    tempstr = t.read()
    t.close()
    global output
    output = replace_words(tempstr, device)
    fout = open('output', 'w')
    fout.write(output)
    fout.close()

# function to load the json file


def json_load(json_file):
    file = open(json_file)
    texto = file.read()
    config = json.loads(texto)
    file.close()
    return config

# function to post the json config file


def post_the_json(data_text, data_url):
    json_datos = json.dumps(data_text)
    r = my_session.post(data_url, data=json_datos)
    json_response = json.loads(r.text)
    if json_response["totalCount"] == "0":
        return True


def asavg():
    excel()
    login()
    print "\n Insertando FW clase ORO (ASAv) external en tenant: " + t_name.value + "\n"

    # Inserta BD-bd_asapbr_ext

    create_output('BD-bd_asapbr_ext.json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # if response:
        # print "\n" + "***************** Insertado BD_asapbr_ext"

    # Inserta Policy Based Redirect svcRedirectPol-ASAv-PBR-EXT

    create_output("svcRedirectPol-ASAv-PBR-EXT.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        pass
        # print "\n" + "***************** Insertado pbr_ext" + "\n"
        # raw_input("Press Enter to insert ASAv_device and service graph...")

    # Inserta Asav external lDevVip-ASAv-Security-1

    create_output("lDevVip-ASAv-Security-1.json")
    json_file = "output"
    config = json_load(json_file)
    post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado ASAv_device con EXITO" + "\n"

    # Inserta Asav external service graph AbsGraph-ASAv-pbr-ext

    create_output("AbsGraph-ASAv-pbr-ext.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado ASAv_service_graph con EXITO" "\n"
        return True
        # raw_input("Press Enter to apply service graph in contract web...")

def asavi():
    # Apply Asav external service graph asav1pbrextapplyservicegraph


    create_output("asav1pbrextapplyservicegraph.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # print response
    if response:
        print "\n" + "***************** Insertado ASAv_service_graph con EXITO"
        writeMessage("\n" + "Inserted FW class GOLD (ASAv) in tenant  ->>" + t_name.value + " -- Your Tenant is secured with CISCO SECURITY" + "\n")
        return True
def asaphyg():
    excel()
    login()
    print "\n Inserted FW class PLATINUM (ASA_PHY) in tenant: " + t_name.value + "\n"

    # Inserta BD-bd_asapbr_ext

    create_output('BD-bd_asapbr_phy_ext.json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # if response:
        # print "\n" + "***************** Insertado BD_asapbr_ext"

    # Inserta Policy Based Redirect svcRedirectPol-ASAv-PBR-EXT

    create_output("svcRedirectPol-ASAv-PBR-PHY-EXT.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        pass
        # print "\n" + "***************** Insertado pbr_ext" + "\n"

    # Inserta Asav external lDevVip-ASAv-Security-1

    create_output("lDevVip-ASA5515.json")
    json_file = "output"
    config = json_load(json_file)
    post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado ASA_PHY_device con EXITO" + "\n"

    # Inserta Asav external service graph AbsGraph-ASAv-pbr-ext

    create_output("AbsGraph-ASA5515-PHY.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado ASA-PHY_ext_service_graph con EXITO" "\n"
        return True

def asaphyi():
    create_output("insertagraph5515.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # print response
    if response:
        print "\n" + "***************** Insertado ASA-PHY_service_graph con EXITO"
        writeMessage("\n" + "Inserted FW class PLATINUM (ASA_PHY) in tenant  ->>" + t_name.value + " -- You tenant is secured with CISCO SECURITY" + "\n")
        return True

def ftdv3g():
    excel()
    login()
    print "\n Insertando FTD internal no gestionado en tenant: " + t_name.value + "\n"

    # Inserta BD-bd_ftdv3_int

    create_output('BD-bd_ftdv3_int.json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # print response
    # if response:
        # print "\n" + "***************** Insertado BD_FTD_int"

    # Inserta Policy Based Redirect ssvcRedirectPol-FTD-PBR-INT.json

    create_output("svcRedirectPol-FTD-PBR-INT.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        # print "\n" + "***************** Insertado pbr_ext" + "\n"
        pass

    # Inserta FTD internal lDevVip-ASAv-Security-1

    create_output("deviceftdv3.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado FTD Unmanaged con EXITO" + "\n"

    # Inserta FTD internal service graph graphftdv3

    create_output("graphftdv3.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado FTD_service_graph Unmanaged con EXITO" "\n"
        return True

def ftdv3i():
    create_output("applyftdgraph.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Insertado FTD_service_graph Unmanaged con EXITO"
        writeMessage("\n" + "Inserted FTD in tenant  ->>" + t_name.value + " -- Your tenant is secured with CISCO SECURITY" + "\n")
        return True

def ftdv4g():
    excel()
    login()
    print "\n Insertando FTD gestionado por APIC internal en tenant: " + t_name.value + "\n"

    # Inserta BD-bd_ftdv3_int

    create_output('BD-bd_ftdv3_int.json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # print response
    # if response:
        # print "\n" + "***************** Insertado BD_FTD_int"

    # Inserta Policy Based Redirect FTD-PBR-INT-ftdv4

    create_output("FTD-PBR-INT-ftdv4.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        # print "\n" + "***************** Insertado pbr_ext" + "\n"
        pass

    # Inserta Device Manager FTF device package

    create_output('devMgr-FMC.json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")

    # Inserta FTD internal lDevVip-FTDv4

    create_output("lDevVip-FTDv4.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado FTD Managed con EXITO" + "\n"

    # Inserta Function profile group1

    create_output('absFuncProfGrp-Group1 (3).json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # print response

    # Inserta Function profile one-armed

    create_output('absFuncProf-one-armed.json')
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    # print response

    # Crea FTD internal service graph graphftdv4

    create_output("AbsGraph-FTDv4-SG.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
    if response:
        print "\n" + "***************** Preparado FTD_service_graph Managed con EXITO" "\n"
        return True


def ftdv4i():
    create_output("applySGFTDv4.json")
    json_file = "output"
    config = json_load(json_file)
    response = post_the_json(config, "http://10.50.0.138/api/node/mo/uni/%s.json" % (device["tn-t_name"]))
    os.remove("output")
      # print response
    if response:
        print "\n" + "***************** Aplicado FTD_service_graph Managed con EXITO"
        writeMessage("\n" + "Inserted Managed FTD  in tenant  ->>" + t_name.value + " -- Your tenant is secured with CISCO SECURITY" + "\n")
        return True
