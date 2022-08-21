# Command Collection

## Virtuelle Umgebung Python
Befehl | Beschreibung
----|----
python -m venv NAME	            |   Erstellen einer vrituellen Umgebung mit dem Namen "NAME"
venv\Scripts\activate.bat	    |   Startet virtuelle Umgebung mit dem Namen "venv" in Windows (falls erfolgreich ->"(venv)" vor dem Pfad)
deactivate					    |	Beendet die virtuelle Umgebung
pip list					    |	Listet alle installierten Bibliotheken der Umgebung
pip freeze > requirements.txt	|	Erstellt requirements.txt File
pip install -r requirements.txt	|	Installiert alle Requirements

## Backend Installs (newest Versions)
pip install fastapi\
pip install "uvicorn[standard]"\
pip install pytest\
pip install request\
pip install pytest-cov\
pip install python-multipart\
pip install jinja2\
pip install SQLAlchemy\
pip install Pillow\
pip install tensorflow\
pip install opencv-python\
pip install Shapely\
pip install scikit-learn\
pip install pandas\
pip install plotly\

## Tests
Befehl | Beschreibung
----|----
pytest								                        |   Startet Tests
pytest -v							                        |   Detailiertere Ausgabe der Tests (noch detailierter mit -vv)
pytest --cov > coverage.txt; Remove-Item -Path .coverage	|   (Powershell) Bewertet die Test Coverage und speichert Ergebnis in coverage.txt und löschen der Meta-Daten

## Run Backend
Befehl | Beschreibung
----|----
startServer.bat                                 |   Startet den Server mit der derzeitigen Konfiguration
uvicorn main:app --reload					    |   (Ausführung im REST_Server Directory) Startet den Server der Änderungen akktualisiert (Ctrl.+C -> Beenden)
uvicorn main:app --host 0.0.0.0 --port 8000		|	(Ausführung im REST_Server Directory) Startet Server der im Netzwerk erreichbar ist, unter der IP-Adresse mit dem Port 8000