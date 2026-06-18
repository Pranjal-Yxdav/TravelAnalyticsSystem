from analytics import (
    import_csv,
    generate_places
)

from reports import generate_report


def import_user_data(
    user_id,
    user_name,
    csv_path
):

    import_csv(
        csv_path,
        user_id
    )

    generate_places(
        user_id
    )

    generate_report(
        user_id,
        user_name
    )

    return True

