import sqlite3


def create_database():

    conn = sqlite3.connect("database/travel.db")

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


if __name__ == "__main__":

    create_database()

    print("Database Created Successfully")