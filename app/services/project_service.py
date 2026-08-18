from database import get_connection


def get_projects():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def add_project(name, description):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT COALESCE(MAX(id), 0) + 1 FROM projects"
        )

        project_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO projects
            (
                id,
                name,
                description
            )
            VALUES (%s, %s, %s)
            """,
            (
                project_id,
                name,
                description
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete_project(project_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM requirements WHERE project_id = %s",
            (project_id,)
        )

        cursor.execute(
            "DELETE FROM tasks WHERE project_id = %s",
            (project_id,)
        )

        cursor.execute(
            "DELETE FROM change_requests WHERE project_id = %s",
            (project_id,)
        )

        cursor.execute(
            "DELETE FROM issues WHERE project_id = %s",
            (project_id,)
        )

        cursor.execute(
            "DELETE FROM notes WHERE project_id = %s",
            (project_id,)
        )

        cursor.execute(
            "DELETE FROM projects WHERE id = %s",
            (project_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
