from datetime import datetime

from database import get_connection


def get_tasks(project_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE project_id = %s
        ORDER BY id DESC
        """,
        (project_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
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
    cursor = connection.cursor()

    completed_at = None

    if status == "Done":
        completed_at = datetime.now().isoformat(
            timespec="seconds"
        )

    cursor.execute(
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
        VALUES (%s, %s, %s, %s, %s, %s)
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
    cursor.close()
    connection.close()


def update_task_status(
    task_id,
    status
):
    connection = get_connection()
    cursor = connection.cursor()

    completed_at = None

    if status == "Done":
        completed_at = datetime.now().isoformat(
            timespec="seconds"
        )

    cursor.execute(
        """
        UPDATE tasks
        SET status = %s,
            completed_at = %s
        WHERE id = %s
        """,
        (
            status,
            completed_at,
            task_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
