import sqlite3
import folium


def generate_map(
    user_id,
    user_name
):

    conn = sqlite3.connect("database/travel.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT latitude, longitude
    FROM locations
    WHERE user_id = ?
    ORDER BY timestamp
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return None

    travel_map = folium.Map(
        location=[rows[0][0], rows[0][1]],
        zoom_start=10
    )

    folium.PolyLine(
        rows,
        weight=4
    ).add_to(travel_map)

    for lat, lon in rows:

        folium.Marker(
            [lat, lon]
        ).add_to(travel_map)

    output_file = (
        f"reports/{user_name}/travel_map.html"
    )

    travel_map.save(output_file)

    return output_file