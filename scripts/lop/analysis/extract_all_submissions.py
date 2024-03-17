from api.sql_api import query, connect_to_server
from dotenv import load_dotenv

import pandas as pd, os

load_dotenv()

SQL_ADDRESS = os.environ.get("SQL_ADDRESS")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")
SQL_DATABASE = os.environ.get("SQL_DATABASE")

CSV_EXPORT_PATH = os.environ.get("CSV_EXPORT_PATH")

sql = connect_to_server(SQL_ADDRESS, SQL_USER, SQL_PASSWORD, SQL_DATABASE)

vals = []

resultados = query(sql, 'SELECT * FROM `submission` LIMIT 1000')

for resultados in resultados:
    
    vals.append(resultados)

"""
As colunas reais utilizadas estão no df gerado a partir do pandas, mas para o csv exportado, apenas as colunas que estão no df.to_csv() são utilizadas.

Por questões de performance e evitar travamentos, o limite de resultados por submissões é de 1000, como estamos em um ambiente de desenvolvimento, para uma melhor
visualização dos dados, recomenda-se utilizar um limite baixo!

Neste caso, se atentar as colunas utilizadas e extraídas serem as mesmas da consulta.
"""

columns = ["id", "ip", "type", "environment", "hitPercentage", "language", "answer", "char_change_number", "timeConsuming", "createdAt", "user_id", "question_id", "listQuestions_id", "test_id", "class_id", "lesson_id"]

df = pd.DataFrame(vals, columns=columns)

print(df.to_json())

df[['id', 'ip', 'type', 'environment', 'language', 'hitPercentage', 'user_id', 'question_id', 'timeConsuming', 'listQuestions_id', 'class_id', 'lesson_id']].to_csv(CSV_EXPORT_PATH)