from database import get_connection


def get_requirements(project_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM requirements
        WHERE project_id = %s
        ORDER BY id DESC
        """,
        (project_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def add_requirement(
    project_id,
    requirement,
    module,
    priority,
    status
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO requirements
        (
            project_id,
            requirement,
            module,
            priority,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            project_id,
            requirement,
            module,
            priority,
            status
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def update_requirement_status(
    requirement_id,
    status
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE requirements
        SET status = %s
        WHERE id = %s
        """,
        (
            status,
            requirement_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()
