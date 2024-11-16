Requirements:
- MySQL 8.0
- Python 3.11.5

Run steps:
1. Environment variables
- Create .env file
- Create the following variables:
  + DB_USER=...
  + DB_PASSWORD=...
  + OPENAI_ORGANIZATION_ID=...
  + OPENAI_PROJECT_ID=...
  + OPENAI_KEY=...

2. Database
- Create table named "ai_drawing_contest" in MySQL
- Run ALL commands in DDL.sql file

3. Virtual Environment, dependencies (terminal at clone directory)
- python -m venv .venv
- .venv/Scripts/activate
   + If unauthorized, run the following command: Set-ExecutionPolicy Unrestricted -Scope Process
- pip install -r requirements.txt

4. Run backend app (from activated virtual environment)
flask --app app run
