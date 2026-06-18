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
    
    folium.CircleMarker(
        location=rows[0],
        radius=10,
        color="green",
        fill=True,
        fill_color="green",
        popup="🚀 Start"
    ).add_to(travel_map)
    
    folium.CircleMarker(
        location=rows[-1],
        radius=10,
        color="red",
        fill=True,
        fill_color="red",
        popup="🏁 End"
    ).add_to(travel_map)
    
    for lat, lon in rows[1:-1]:

        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.8,
            popup=f"{lat}, {lon}"
        ).add_to(travel_map)

    return travel_map

