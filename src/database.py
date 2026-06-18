import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DB_PATH = os.path.join(
    DATABASE_DIR,
    "travel.db"
)


def create_database():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        latitude REAL,
        longitude REAL,
        timestamp TEXT,
        UNIQUE(
            user_id,
            latitude,
            longitude,
            timestamp
        ),
        FOREIGN KEY(user_id)
        REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS place_names(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        place_name TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def get_connection():

    print("\nDATABASE PATH =", DB_PATH)

    return sqlite3.connect(
        DB_PATH
    )


if __name__ == "__main__":

    create_database()

    print("Database Created Successfully")

