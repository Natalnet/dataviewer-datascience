from api.sql_api import query, connect_to_server
from dotenv import load_dotenv

import pandas as pd, os

SQL_ADDRESS = os.environ.get("SQL_ADDRESS")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")
SQL_DATABASE = os.environ.get("SQL_DATABASE")

CSV_EXPORT_PATH = os.environ.get("CSV_EXPORT_PATH")

sql = connect_to_server(SQL_ADDRESS, SQL_USER, SQL_PASSWORD, SQL_DATABASE)

vals = []

resultados = query(sql, "SELECT * FROM `submission` WHERE `user_id` = '8fc0c794-3bae-4c31-b5d9-d1a525f2046d'")

for resultados in resultados:
    
    vals.append(resultados)

columns = ["id", "ip", "type", "environment", "hitPercentage", "language", "answer", "char_change_number", "timeConsuming", "createdAt", "user_id", "question_id", "listQuestions_id", "test_id", "class_id", "lesson_id"]

df = pd.DataFrame(vals, columns=columns)

print(df.to_json())

df[['id', 'ip', 'type', 'environment', 'language', 'hitPercentage', 'user_id', 'question_id', 'timeConsuming', 'listQuestions_id', 'class_id', 'lesson_id']].to_csv(CSV_EXPORT_PATH)