import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "partners.db"
SCHEMA_PATH = HERE / "schema.sql"
SEED_PATH = HERE / "seed.sql"


def get_connection(database_path=None):
    if database_path is None:
        database_path = DB_PATH
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(connection):
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'partners'"
    ).fetchone()
    if row is not None:
        return
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    connection.executescript(SEED_PATH.read_text(encoding="utf-8"))
    connection.commit()


def open_db(database_path=None):
    connection = get_connection(database_path)
    initialize_database(connection)
    return connection
