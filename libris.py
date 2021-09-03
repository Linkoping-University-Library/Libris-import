import requests
import json
import os
import logging

from FolioCommunication import FolioCommunication


def is_empty_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) == 0


if __name__ == "__main__":
#    logging.basicConfig(filename='./log/folio_import.log',
#                        format='%(levelname)s: %(message)s', level=logging.INFO)
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    folio = FolioCommunication()
    libris_dir = './libris_files/'
    jobprofile = '"jobProfileInfo": {"id": "aa8ff044-2490-4611-ac74-3054aa21e8eb", "name": "Create MARC Bibs", "dataType": "MARC"}'

    for filename in os.listdir(libris_dir):
        if filename.endswith('.mrc'):
            # fil som inte är tom?
            if not is_empty_file(libris_dir + filename):
                logging.info('Processing file: %s', filename)

                # steg 1
                stage1_json = folio.uploadDefinitions(filename)
                uploadDefinitionId = stage1_json['id']
                fileDefinitionId = stage1_json['fileDefinitions'][0]['id']

                # Steg 2 - skicka in filen
                with open(libris_dir + filename, 'rb') as f:
                    data = f.read()

                stage2_json = folio.uploadFile(uploadDefinitionId, fileDefinitionId, data)

                # Steg 3
                stage2_string = json.dumps(stage2_json)
                stage2_string = stage2_string.replace("'", '"')

                data = '{"uploadDefinition":' + stage2_string + ', ' + jobprofile + '}'
                data_json = json.loads(data)

                stage3Response = folio.processFile(uploadDefinitionId, data_json)

                logging.info('Response from /data-import/uploadDefinitions/{uploadDefinitionId}/processFiles: %s', str(stage3Response.status_code))
                logging.info('Raw response from /data-import/uploadDefinitions/{uploadDefinitionId}/processFiles: %s', str(stage3Response.raw))

            # Radera filen (både om den är tom eller om vi bearbetat den)
            # os.remove(libris_dir + filename)

