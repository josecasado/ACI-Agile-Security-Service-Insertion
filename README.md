Inserting automatically ASA and Firepower sensors in ACI 

This repo will include all the files needed for this use case demo. 

Python program has been used to make the API rest calls to APIC. A flask web server for presenting a portal to deploy the security services.

This setup requires:

    ACI Tenant with 2 tier (web+db) and a L3 out to get to the web server.
    FMC deployed and some FTD ready.
    Manual configuration of servige graph inserting ASA and FTD to save the json configuration file
    Xls file with the info containing the names of the tenant, EPG, contracts etc to be used.
    

The repo includes these relevant files:

    app.py - python flask file for the provisioning portal
    fw.py - python program reads the excel with the ACI Tenant info and make the rest API calls to APIC.
    sparkjc.py - python script to send messages to the webex team room
    app, static and templates directories - http and css for the web portal
    tenant-parametros - xls file for the tenant info
    

Application Workflow

    Web Portal allow to choose what device must be inserted, protecting the perimeter or the Data Base
    Example ASA:
    flask calls the fw.py program.The fw.py reads the tenant parameters excel and execute the functions for creating the Service graph and apply it to the contract.
    The json to configure the SG and apply it are already built from a manual config, the logic replace the tenant, epg names etc for the one used depending on the xls file.
    Finally a message is sent to the webex team.
