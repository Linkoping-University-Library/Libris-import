import json
import os
import sys
import logging
import pymarc

logging.basicConfig(filename='/usr/local/bin/python_scripts/logs/libris_import.log', filemode = 'a', level=logging.ERROR)


sys.path.append('../foliocommunication')
from FolioCommunication import FolioCommunication

folio = FolioCommunication()


# Kollar om en fil är tom
def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


chunkSize = 200

filesFolder = "./libris_files/"
chunksFolder = "./libris_files/chunks/"

for filename in os.listdir(filesFolder):
    if filename.endswith(".mrc"):
        # fil som inte är tom?
        if is_non_zero_file(filesFolder + filename):
            
            with open(filesFolder + filename, 'rb') as data:
                reader = pymarc.MARCReader(data)

                chunkNumber = 0
                recordCounter = 1
                outfile = open(chunksFolder + filename.replace(".mrc", "_" + str(chunkNumber) + ".mrc"), "wb")

                for record in reader:
                    outfile.write(record.as_marc())
                    recordCounter += 1

                    if recordCounter > chunkSize:
                        outfile.flush()
                        outfile.close
                        chunkNumber +=1
                        outfile = open(chunksFolder + filename.replace(".mrc", "_" + str(chunkNumber) + ".mrc"), "wb")
                        recordCounter = 1

                outfile.flush()
                outfile.close
            
            os.remove(filesFolder + filename)

        else:
            os.remove(filesFolder + filename)




for filename in os.listdir(chunksFolder):

            response = folio.uploadDefinitions(filename)
            stage1_json = response


            uploadDefinitionId = stage1_json['id']
            fileDefinitionId = stage1_json['fileDefinitions'][0]['id']



            # Steg 2 - skicka in filen
            with open(chunksFolder + filename, 'rb') as f:
                data = f.read()

            sendResponse = folio.uploadFile(uploadDefinitionId, fileDefinitionId, data)
            stage2_json = sendResponse



            # Steg 3
            stage2_string = json.dumps(stage2_json)
            stage2_string = stage2_string.replace("'",'"')

            data = '{"uploadDefinition":' + stage2_string + ', "jobProfileInfo": {"id": "aa8ff044-2490-4611-ac74-3054aa21e8eb", "name": "Libris", "dataType": "MARC"}}'
            data_json = json.loads(data)


            steg3Response = folio.processFile(uploadDefinitionId, data_json)
            logging.info(steg3Response)
           

            # Radera filen om allt gick bra
            os.remove(chunksFolder + filename)
            

        
