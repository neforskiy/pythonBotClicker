from getpass import getpass
from mysql.connector import connect, Error

def db_connect(Query):
    try:
        with connect(
            host="localhost",
            user="root",
            password="",
            database="clicks",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(Query)
                result = cursor.fetchall()
                connection.commit()
                for item in result:
                    resultat = item
                    print(resultat)
                    return resultat
        print(f"""
    Соединение установлено:
    хост: {connection.server_host}
    порт: {connection.server_port}
    пользователь: {connection.user}
    база данных: {connection.database}""")
    except Error as e:
        print(f"Ошибка подключения к серверу:\n{e}")
