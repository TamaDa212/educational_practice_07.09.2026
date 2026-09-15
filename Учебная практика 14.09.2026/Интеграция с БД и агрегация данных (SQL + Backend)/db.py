import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "partners.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
SEED_PATH = Path(__file__).resolve().parent / "seed.sql"


def get_connection(database_path=None):
    if database_path is None:
        database_path = DB_PATH
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(connection):
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    seed_sql = SEED_PATH.read_text(encoding="utf-8")
    connection.executescript(schema_sql)
    connection.executescript(seed_sql)
    connection.commit()
