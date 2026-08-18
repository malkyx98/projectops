from datetime import datetime

from database import get_connection


def get_tasks(project_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE project_id = ?
        ORDER BY id DESC
        """,
        (project_id,)
    ).fetchall()

    connection.close()

    return rows


def add_task(
    project_id,
    title,
    module,
    priority,
    status
):
    connection = get_connection()

    completed_at = None

    if status == "Done":
        completed_at = datetime.now().isoformat(
            timespec="seconds"
        )

    connection.execute(
        """
        INSERT INTO tasks
        (
            project_id,
            title,
            module,
            priority,
            status,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            project_id,
            title,
            module,
            priority,
            status,
            completed_at
        )
    )

    connection.commit()
    connection.close()


def update_task_status(
    task_id,
    status
):
    connection = get_connection()

    completed_at = None

    if status == "Done":
        completed_at = datetime.now().isoformat(
            timespec="seconds"
        )

    connection.execute(
        """
        UPDATE tasks
        SET status = ?,
            completed_at = ?
        WHERE id = ?
        """,
        (
            status,
            completed_at,
            task_id
        )
    )

    connection.commit()
    connection.close()
