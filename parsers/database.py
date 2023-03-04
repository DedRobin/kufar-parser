import os
import psycopg2

connection = psycopg2.connect(
    database=os.environ.get("DATABASE_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
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
    connection.commit()
except:
    print("Table exists")


