from analytics import (
    calculate_distance,
    most_visited,
    total_records,
    unique_places
)

import os


def generate_report(
    user_id,
    user_name
):

    distance = calculate_distance(
        user_id
    )

    place = most_visited(
        user_id
    )

    records = total_records(
        user_id
    )

    places = unique_places(
        user_id
    )

    user_folder = os.path.join(
        "reports",
        user_name
    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    report_file = os.path.join(
        user_folder,
        "travel_report.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "TRAVEL ANALYTICS REPORT\n"
        )

        file.write(
            "=" * 40 + "\n\n"
        )

        file.write(
            f"User: {user_name}\n\n"
        )

        file.write(
            f"Total Records: {records}\n"
        )

        file.write(
            f"Unique Places: {places}\n"
        )

        file.write(
            f"Distance Covered: {distance} KM\n\n"
        )

        if place:

            file.write(
                "Most Visited Place:\n"
            )

            file.write(
                f"{place[0]}\n"
            )

            file.write(
                f"Visits: {place[1]}\n"
            )

        else:

            file.write(
                "Most Visited Place: Not Available\n"
            )

    return report_file

