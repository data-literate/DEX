import os
from collections.abc import Iterator
from contextlib import contextmanager

import pyodbc
from dotenv import load_dotenv

load_dotenv()


def get_connection_string() -> str:
    driver = os.getenv("DB_DRIVER")
    server_name = os.getenv("DB_SERVER")
    database_name = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    return (
        f"DRIVER={driver};"
        f"SERVER={server_name};"
        f"DATABASE={database_name};"
        f"UID={username};"
        f"PWD={password}"
    )


@contextmanager
def db_connection() -> Iterator[pyodbc.Connection]:
    conn_str = get_connection_string()
    conn = pyodbc.connect(conn_str)
    try:
        yield conn
    finally:
        conn.close()


if __name__ == "__main__":

    with db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        print("Database connection test result:", row)
