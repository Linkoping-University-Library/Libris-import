#!/bin/bash


# exit shell om nåt går fel:
set -e

# Se till att vi inte kör flera instanser av skriptet samtidigt
# Vi kör flock direkt i crontabellen för att förhindra flera instanser, se crontab -e /Anders Fåk

# Om vi kör för första gången, sätt 'nu' till start-tid
LASTRUNTIMEPATH="lastRun.timestamp"
if [ ! -e $LASTRUNTIMEPATH ]
then
    date -u +%Y-%m-%dT%H:%M:%SZ > $LASTRUNTIMEPATH
fi

# Avgör vilket tidsintervall vi ska hämta
STARTTIME=`cat $LASTRUNTIMEPATH`
STOPTIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
filename="./libris_files/export_"$current_time".mrc"

# Hämta data
curl --fail -XPOST "https://libris.kb.se/api/marc_export/?from=$STARTTIME&until=$STOPTIME&deleted=ignore&virtualDelete=false" --data-binary @./settings/export.properties > $filename

# Om allt gick bra, uppdatera tidsstämpeln
echo $STOPTIME > $LASTRUNTIMEPATH

# Importera till FOLIO
python libris.py
