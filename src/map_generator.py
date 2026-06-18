import folium

from database import get_connection


def generate_map(user_id):

    conn = get_connection()

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

    print("USER ID =", user_id)
    print("ROWS =", rows)

    conn.close()

    if len(rows) == 0:

        return None

    travel_map = folium.Map(
        location=[
            rows[0][0],
            rows[0][1]
        ],
        zoom_start=10
    )

    folium.PolyLine(
        rows,
        weight=5,
        color="blue"
    ).add_to(travel_map)

    for lat, lon in rows:

        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.9,
            tooltip=f"{lat}, {lon}"
        ).add_to(travel_map)

    return travel_map

