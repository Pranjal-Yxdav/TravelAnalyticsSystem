import sqlite3
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from time import sleep


def import_csv(csv_file, user_id):

    conn = sqlite3.connect("database/travel.db")
    cursor = conn.cursor()

    df = pd.read_csv(csv_file)

    required_columns = [
        "latitude",
        "longitude",
        "timestamp"
    ]

    for column in required_columns:

        if column not in df.columns:

            conn.close()

            raise Exception(
                f"Missing column: {column}"
            )

    imported_count = 0

    for _, row in df.iterrows():

        latitude = float(
            row["latitude"]
        )

        longitude = float(
            row["longitude"]
        )

        timestamp = str(
            row["timestamp"]
        )

        cursor.execute("""
        SELECT COUNT(*)
        FROM locations
        WHERE user_id = ?
        AND latitude = ?
        AND longitude = ?
        AND timestamp = ?
        """,
        (
            user_id,
            latitude,
            longitude,
            timestamp
        ))

        exists = cursor.fetchone()[0]

        if exists == 0:

            cursor.execute("""
            INSERT INTO locations
            (
                user_id,
                latitude,
                longitude,
                timestamp
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                user_id,
                latitude,
                longitude,
                timestamp
            ))

            imported_count += 1

    conn.commit()

    conn.close()

    return imported_count


def generate_places(user_id):

    conn = sqlite3.connect("database/travel.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT
        latitude,
        longitude
    FROM locations
    WHERE user_id = ?
    """,
    (user_id,))

    rows = cursor.fetchall()

    geolocator = Nominatim(
        user_agent="travel_analytics"
    )

    for lat, lon in rows:

        cursor.execute("""
        SELECT COUNT(*)
        FROM place_names
        WHERE latitude = ?
        AND longitude = ?
        """,
        (
            lat,
            lon
        ))

        exists = cursor.fetchone()[0]

        if exists == 0:

            try:

                location = geolocator.reverse(
                    f"{lat},{lon}"
                )

                if location:

                    cursor.execute("""
                    INSERT INTO place_names
                    (
                        latitude,
                        longitude,
                        place_name
                    )
                    VALUES
                    (
                        ?, ?, ?
                    )
                    """,
                    (
                        lat,
                        lon,
                        location.address
                    ))

                    conn.commit()

                sleep(1)

            except:

                pass

    conn.close()


def calculate_distance(user_id):

    conn = sqlite3.connect("database/travel.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        latitude,
        longitude
    FROM locations
    WHERE user_id = ?
    ORDER BY timestamp
    """,
    (user_id,))

    rows = cursor.fetchall()

    distance = 0

    for i in range(1, len(rows)):

        distance += geodesic(
            rows[i - 1],
            rows[i]
        ).km

    conn.close()

    return round(distance, 2)


def most_visited(user_id):

    conn = sqlite3.connect("database/travel.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        p.place_name,
        COUNT(*) AS visits
    FROM locations l
    JOIN place_names p
    ON l.latitude = p.latitude
    AND l.longitude = p.longitude
    WHERE l.user_id = ?
    GROUP BY p.place_name
    ORDER BY visits DESC
    LIMIT 1
    """,
    (user_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def total_records(user_id):

    conn = sqlite3.connect("database/travel.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM locations
    WHERE user_id = ?
    """,
    (user_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


def unique_places(user_id):

    conn = sqlite3.connect("database/travel.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(
        DISTINCT latitude || longitude
    )
    FROM locations
    WHERE user_id = ?
    """,
    (user_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


def user_history(user_id):

    conn = sqlite3.connect(
        "database/travel.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        timestamp,
        latitude,
        longitude
    FROM locations
    WHERE user_id = ?
    ORDER BY timestamp
    """,
    (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def dashboard_data(user_id):

    place = most_visited(
        user_id
    )

    return {
        "records": total_records(
            user_id
        ),
        "places": unique_places(
            user_id
        ),
        "distance": calculate_distance(
            user_id
        ),
        "most_visited": place[0] if place else "N/A",
        "visits": place[1] if place else 0
    }

