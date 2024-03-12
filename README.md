# dsbDynDns
ist ein DynDns Client für den Webanbieter domainssaubillig.de

## Installation
1. .env Datei Erstellen ([Beispiel](beispiel.env))
2. [updateDns.py](updateDns.py) als cronjob regelmäßig ausführen
Hierzu bietet sich Crontab an:\
[Anleitung Crontab Job erstellen](https://askubuntu.com/questions/2368/how-do-i-set-up-a-cron-job)\
Bsp: `*/5 * * * * python3 /root/dsbDyndns/updateDns.py >> /root/dsbDyndns/log.txt`
