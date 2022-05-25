Processen består av två delar:

1. Export-skript (bash) som exporterar poster från LibrisXL
2. Import-skript i python som importerar till FOLIO


Körs som cron-jobb på folioscript: (flock hindrar flera samtidiga instanser)
(  EDITOR=nano crontab -e )

*/2 * * * * flock -n /usr/local/bin/python_scripts/libris.lock -c /usr/local/bin/python_scripts/libris.sh > /dev/null 2>&1
