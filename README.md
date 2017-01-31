#fantasyfootball-api-project

This project contains the source code for my first side project in python - to call the fantasy football nerd API.
http://www.fantasyfootballnerd.com/fantasy-football-api

Through the free level 1 access we can get data on NFL teams, Schedule, Players as well as weather forcasts. We recieve the response the response in JSON format, parse the information and store them in a SQLite database using Python DB-API for sqlite3 module.
The information retrieved once is stored in the Sqlite DB until the whole program is rerun to fetch any updates/new records.

To run this program on your computer you will need Python 3.x and sqlite3 or greater installed. 
