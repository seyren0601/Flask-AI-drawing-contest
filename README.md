Requirements:
- MySQL 8.0
- Python 3.11.5

Dependencies:
* Environment files
- Create .env file
- Create the following variables:
  + DB_USER=...
  + DB_PASSWORD=...

* Database
- Create table named "ai_drawing_contest"
- Run ALL commands in DDL.sql file

* Terminal
- python -m venv .env/
- .env/Scripts/activate

* Virtual Environment
- pip install -m "requirements.txt"

Run backend app (from activated virtual environment):
flask --app app run
