Processen består av två delar:

1. Export-skript (bash) som exporterar poster från LibrisXL
2. Import-skript i python som importerar till FOLIO

Import-skriptet är helt baserat på exempel-skriptet här: https://github.com/folio-org/mod-data-import/blob/master/scripts/load-marc-data-into-folio.sh

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