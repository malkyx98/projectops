from database import get_connection


def get_requirements(project_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM requirements
        WHERE project_id = ?
        ORDER BY id DESC
        """,
        (project_id,)
    ).fetchall()

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

    connection.execute(
        """
        INSERT INTO requirements
        (
            project_id,
            requirement,
            module,
            priority,
            status
        )
        VALUES (?, ?, ?, ?, ?)
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
    connection.close()


def update_requirement_status(
    requirement_id,
    status
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE requirements
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            requirement_id
        )
    )

    connection.commit()
    connection.close()
