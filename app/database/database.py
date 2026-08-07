import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.utils.config import settings


class DatabaseManager:
    def __init__(self):
        self.database_path = settings.DATABASE_PATH

        # Ensure the data folder exists
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            yield connection
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def create_tables(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expiry_date TEXT,
                    status TEXT NOT NULL DEFAULT 'Active'
                )
                """
            )


database = DatabaseManager()