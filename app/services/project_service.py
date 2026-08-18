from database import get_connection


def get_projects():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return rows


def add_project(name, description):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO projects (name, description)
        VALUES (?, ?)
        """,
        (name, description)
    )

    connection.commit()
    connection.close()
