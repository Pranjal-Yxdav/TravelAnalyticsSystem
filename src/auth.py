import os

from database import get_connection


def register_user(
    name,
    email,
    password
):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users
        (
            name,
            email,
            password
        )
        VALUES
        (
            ?, ?, ?
        )
        """,
        (
            name,
            email,
            password
        ))

        conn.commit()

        conn.close()

        os.makedirs(
            os.path.join(
                "reports",
                name
            ),
            exist_ok=True
        )

        return True

    except Exception:

        return False


def login_user(
    email,
    password
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email = ?
    AND password = ?
    """,
    (
        email,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user

