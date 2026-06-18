import sqlite3
import pandas as pd
import os


def export_results(
    user_id,
    user_name
):

    conn = sqlite3.connect(
        "database/travel.db"
    )

    query = """
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
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(user_id,)
    )

    conn.close()

    user_folder = os.path.join(
        "reports",
        user_name
    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    output_file = os.path.join(
        user_folder,
        "analytics_export.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    return output_file

