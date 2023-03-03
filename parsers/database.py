import psycopg2

connection = psycopg2.connect(
    database="kufar_parser",
    user="dedrobin",
    password="dedrobin",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()
try:
    cursor.execute(
        """
        CREATE TABLE users (
        id       INTEGER PRIMARY KEY,
        username VARCHAR
    );
        """
    )
except:
    print("Table exists")

connection.commit()
