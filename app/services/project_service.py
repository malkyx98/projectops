from database import get_connection


def get_projects():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def add_project(name, description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO projects (name, description)
        VALUES (%s, %s)
        """,
        (name, description)
    )

    connection.commit()
    cursor.close()
    connection.close()
