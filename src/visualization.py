import sqlite3
import matplotlib.pyplot as plt


def generate_chart(user_id):

    conn = sqlite3.connect(
        "database/travel.db"
    )

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
    """,
    (user_id,))

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:

        return None

    places = []
    visits = []

    for place, count in rows:

        places.append(
            place.split(",")[0]
        )

        visits.append(
            count
        )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        places,
        visits
    )

    ax.set_title(
        "Visited Places"
    )

    ax.set_xlabel(
        "Places"
    )

    ax.set_ylabel(
        "Visits"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    return fig