REST API für das managen von Todo-Listen

Author: Benjamin Bat
Email: b-bat@gmx.de
Telefon: 05491/994167

Libraries:
uuid
flask

Funktionalitäten:
Holen, senden, ändern und löschen (CRUD) der Listen und Listeneinträge
uuid für einzigartige, sichere IDs

Diese Funktionalitäten werden über folgende Endpunkte erreicht:

/todo-list
Hinzufügen einer neuen Liste, POST

/todo-list/{list_id}
Aufrufen oder Löschen einer spezifischen Liste, je nachdem ob GET oder DELETE

/todo-lists
Abfragen aller Listen über GET

/todo-list/{list_id}/entry
Anlegen eines neuen Eintrags für die Liste über POST

/todo-list/{list_id}/entries
abfragen aller Einträge einer Liste über GET

/todo-list/{list_id}/
entry/{entry_id}
Updaten oder Löschen eines bestimmten Eintrags einer Liste über PUT oder DELETE

Setup:
Klone das Git-Repository
git clone https://github.com/BatBenjamin/big-api-task.git

Platziere in ihren Projektpfad
cd <Pfad>\big-api-task

Installiere Flask
pip install Flask

Führe die Python-Datei aus
python index.py

Der Server startet standardmäßig auf 127.0.01:5000

Das Projekt läuft unter der MIT-Lizenz, welche in der LICENSE-Datei nachfolzogen werden kann.

