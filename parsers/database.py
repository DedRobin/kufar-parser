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
        CREATE TABLE users
(
    id       INTEGER PRIMARY KEY,
    username VARCHAR
);
CREATE TABLE chat_ids
(
    id       INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    username_id INTEGER,
    CONSTRAINT username_id
        FOREIGN KEY (username_id)
            REFERENCES users(id)
);

        """
    )
    connection.commit()
except psycopg2.errors.DuplicateTable:
    print("The table is already exists")
