import sqlite3
import matplotlib.pyplot as plt

from database import get_connection


def get_place_data(user_id):

    conn = get_connection()

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

    return rows


def generate_chart(user_id):

    rows = get_place_data(user_id)

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
        figsize=(12, 6)
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


def generate_pie_chart(user_id):

    rows = get_place_data(user_id)

    if len(rows) == 0:

        return None

    labels = []
    sizes = []

    for place, count in rows:

        labels.append(
            place.split(",")[0]
        )

        sizes.append(
            count
        )

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%"
    )

    ax.set_title(
        "Travel Distribution"
    )

    return fig


def generate_line_chart(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        timestamp
    FROM locations
    WHERE user_id = ?
    ORDER BY timestamp
    """,
    (user_id,))

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:

        return None

    x = list(
        range(
            1,
            len(rows) + 1
        )
    )

    y = x

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.plot(
        x,
        y,
        marker="o"
    )

    ax.set_title(
        "Travel Activity Timeline"
    )

    ax.set_xlabel(
        "Travel Records"
    )

    ax.set_ylabel(
        "Activity"
    )

    plt.tight_layout()

    return fig


def generate_horizontal_chart(user_id):

    rows = get_place_data(user_id)

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
        figsize=(10, 6)
    )

    ax.barh(
        places,
        visits
    )

    ax.set_title(
        "Most Visited Places"
    )

    ax.set_xlabel(
        "Visits"
    )

    plt.tight_layout()

    return fig

