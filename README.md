Processen består av två delar:

1. Export-skript (bash) som exporterar poster från LibrisXL
2. Import-skript i python som importerar till FOLIO

Export-skriptet är taget rakt av från KBs exempel: https://github.com/libris/librisxl/blob/master/marc_export/examplescripts/export_nix.sh

Import-skriptet är en python-översättning av exempel-skriptet här: https://github.com/folio-org/mod-data-import/blob/master/scripts/load-marc-data-into-folio.sh

Klona först och skapa sedan en python virtual environment med:

cd libris-import

python3 -m venv venv

Installera "requests" med:
pip install requests

I mappen "settings" finns url och inloggning till FOLIO och "export.properties" för Libris.

Ge exekveringsrättigheter till bash-skriptet med:
sudo chmod +X libris_exp.sh


Bash-skriptet "libris_exp.sh" hämtar data från LibrisXL och sparar i mappen "libris-files".

Python-skriptet läser filerna och importerar till FOLIO:
python libris.py 

I en senare driftmiljö bör båda skripten köras minutvis med en halv minuts förskjutning.