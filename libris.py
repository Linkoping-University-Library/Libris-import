import requests
import json
import os

# Läs in FOLIO-settings:
with open('./settings/folio.ini', 'r') as ini_f:
    # släng första radens kommentar
    slask = ini_f.readline()
    folio_endpoint = ini_f.readline().strip()
    username = ini_f.readline().strip()
    password = ini_f.readline().strip()
    okapi_tenant = ini_f.readline().strip()
    log_results = ini_f.readline().strip()


# Kollar om en fil är tom
def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

# Logga in och returnera okapiToken
def getToken(folio_endpoint, username, password, okapi_tenant):
    login = '/authn/login'
    url = folio_endpoint + login
    payload = {"username":username,"password":password}
    header = {'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-okapi-tenant': okapi_tenant}

    response= requests.post(url,data=json.dumps(payload), headers=header)
    okapiToken = response.headers['x-okapi-token']
    return okapiToken


########################################################
okapiToken = getToken(folio_endpoint, username, password, okapi_tenant)

if log_results == "true":
    log_f = open('./log/folio_import.log', 'a+')

for filename in os.listdir("./libris_files/"):
    if filename.endswith(".mrc"):
        # fil som inte är tom?
        if is_non_zero_file("./libris_files/" + filename):
            if log_results == "true":
                log_f.write(filename + "\n")



        # steg 1
        url = folio_endpoint + "/data-import/uploadDefinitions"

        header = {'Content-Type': 'application/json',
                 'x-okapi-tenant': okapi_tenant,
                 'X-Okapi-Token': okapiToken}

        payload = {"fileDefinitions":[{"name": filename}]}
        response= requests.post(url,data=json.dumps(payload), headers=header)

        stage1_json = response.json()

        uploadDefinitionId = stage1_json['id']
        fileDefinitionId = stage1_json['fileDefinitions'][0]['id']


        # Steg 2 - skicka in filen
        url = folio_endpoint + "/data-import/uploadDefinitions/" + uploadDefinitionId + "/files/" + fileDefinitionId

        header = {'Content-Type': 'application/octet-stream',
                'x-okapi-tenant': okapi_tenant,
                'X-Okapi-Token': okapiToken}

        with open("./libris_files/" + filename, 'rb') as f:
            data = f.read()

        sendResponse = requests.post(url,
                            data=data,
                            headers=header)

        stage2_json = sendResponse.json()

        # Steg 3

        url = folio_endpoint + "/data-import/uploadDefinitions/" + uploadDefinitionId + "/processFiles?defaultMapping=true"
        header = {'Content-Type': 'application/json',
                'x-okapi-tenant': okapi_tenant,
                'X-Okapi-Token': okapiToken}


        stage2_string = json.dumps(stage2_json)
        stage2_string = stage2_string.replace("'",'"')

        data = '{"uploadDefinition":' + stage2_string + ', "jobProfileInfo": {"id": "22fafcc3-f582-493d-88b0-3c538480cd83", "name": "Create MARC Bibs", "dataType": "MARC"}}'
        data_json = json.loads(data)



        steg3Response = requests.post(url,data=json.dumps(data_json), headers=header)

        if log_results == "true":
            log_f.write(str(steg3Response.status_code) + "\n")
            log_f.write(str(steg3Response.raw) + "\n")



        # Radera filen om allt gick bra
        os.remove("./libris_files/" + filename)

    else:
        # radera den tomma filen
        os.remove("./libris_files/" + filename)

if log_results == "true":
    log_f.close()

