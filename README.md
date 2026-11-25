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

Das Protokoll zeigt die öffentliche IPv4, die Entscheidung anhand des Caches,
den Anmeldeversuch sowie HTTP-Status und Bestätigung für beide DNS-Updates.
Zugangsdaten, Sitzungs-Cookies und Antwortinhalte werden nicht protokolliert.

`currentIP.txt` wird erst aktualisiert, wenn der Anbieter beide DNS-Änderungen
bestätigt hat. Fehlgeschlagene Läufe enden mit einem Fehlercode, sodass der
nächste Lauf die DNS-Änderungen erneut versucht.

Wenn der Anbieter nach der Anmeldung erneut das Login-Formular anzeigt,
prüfe die Zugangsdaten in `.env` im Kundenbereich. Meldet eine DNS-Anfrage,
dass eine Anmeldung erforderlich ist, hat der Anbieter die Sitzung für diese
Anfrage nicht akzeptiert.

Für beide DNS-Updates sendet der Client den `Origin`-Header des Kundenbereichs,
den der Anbieter bei diesen POST-Anfragen prüft.
