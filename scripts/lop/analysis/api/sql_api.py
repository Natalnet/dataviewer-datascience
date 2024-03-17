import mysql.connector

from mysql.connector import Error

def connect_to_server(hostname, username, password, db):

    connection = None

    try:

        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            passwd=password,
            database=db
        )

        print('Conectado ao MySQL com sucesso')
    
    except Error as e:
        print(e)

    return connection

def create_database(connection, query):
    cursor = connection.cursor()

    try:

        cursor.execute(query)
    
    except Error as e:
        print(e)

def query(connection, query):
    cursor = connection.cursor()

    rs = None

    try:

        cursor.execute(query)

        rs = cursor.fetchall()

        return rs
    
    except Error as e:
        print(e)