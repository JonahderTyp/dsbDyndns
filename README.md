# dsbDynDns
ist ein DynDns Client für den Webanbieter domainssaubillig.de

## Installation
1. `.env` im Repository anlegen ([Beispiel](beispiel.env)).
2. Abhängigkeiten installieren: `python3 -m pip install -r requirements.txt`.
3. Auf der VM mit `crontab -e` einen Eintrag für [updateDns.py](src/updateDns.py)
   anlegen. Den Beispielpfad durch den absoluten, für den Cron-Benutzer
   beschreibbaren Pfad zum Repository ersetzen:
   ```cron
   */5 * * * * cd /pfad/zu/dsbDyndns && python3 src/updateDns.py
   ```

## Protokolle und IP-Cache

Jeder Lauf protokolliert auf der Konsole und im Arbeitsverzeichnis unter
`logs/dyndns-JJJJ-MM-TT.log` (lokales Datum beim Start). Mehrere Läufe am
selben Tag ergänzen dieselbe Datei. Alte Logs werden nicht automatisch gelöscht.

`currentIP.txt` wird erst aktualisiert, wenn der Anbieter beide DNS-Änderungen
bestätigt hat. Fehlgeschlagene Läufe enden mit einem Fehlercode, sodass der
nächste Lauf die DNS-Änderungen erneut versucht.
