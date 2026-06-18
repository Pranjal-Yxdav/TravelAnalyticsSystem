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

    conn.close()

    if len(rows) == 0:

        return None

    travel_map = folium.Map(
        location=[
            rows[0][0],
            rows[0][1]
        ],
        zoom_start=10,
        tiles="CartoDB Positron"
    )

    folium.PolyLine(
        rows,
        weight=4,
        color="blue"
    ).add_to(travel_map)

    folium.Marker(
        rows[0],
        popup="🚀 Start",
        icon=folium.Icon(color="green")
    ).add_to(travel_map)

    folium.Marker(
        rows[-1],
        popup="🏁 End",
        icon=folium.Icon(color="red")
    ).add_to(travel_map)

    for lat, lon in rows[1:-1]:

        folium.Marker(
            [lat, lon],
            popup=f"{lat}, {lon}"
        ).add_to(travel_map)

    return travel_map

