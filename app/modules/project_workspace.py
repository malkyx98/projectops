import streamlit as st

from database import get_connection


def _next_id(cursor, table):
    cursor.execute(
        f"SELECT COALESCE(MAX(id), 0) + 1 FROM {table}"
    )
    return cursor.fetchone()["count"]


def show(project):

    project_id = project["id"]
    project_name = project["name"]

    if st.button("Back to Projects", key="back_to_projects"):
        st.session_state["selected_project_id"] = None
        st.rerun()

    st.title(project_name)

    if project["description"]:
        st.caption(project["description"])

    st.divider()

    section = st.radio(
        "Project Workspace",
        [
            "Dashboard",
            "Requirements",
            "Features",
            "Tasks",
            "Change Requests",
            "Issues",
            "Notes"
        ],
        horizontal=True
    )

    st.divider()

    connection = get_connection()
    cursor = connection.cursor()

    if section == "Dashboard":

        st.subheader("Project Dashboard")

        cursor.execute(
            "SELECT COUNT(*) FROM requirements WHERE project_id = %s",
            (project_id,)
        )
        requirements_count = cursor.fetchone()["count"]

        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE project_id = %s",
            (project_id,)
        )
        tasks_count = cursor.fetchone()["count"]

        cursor.execute(
            "SELECT COUNT(*) FROM issues WHERE project_id = %s",
            (project_id,)
        )
        issues_count = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE project_id = %s
            AND status = 'Done'
            """,
            (project_id,)
        )
        completed_tasks = cursor.fetchone()["count"]

        progress = (
            int((completed_tasks / tasks_count) * 100)
            if tasks_count
            else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Requirements", requirements_count)

        with col2:
            st.metric("Tasks", tasks_count)

        with col3:
            st.metric("Issues", issues_count)

        with col4:
            st.metric("Progress", f"{progress}%")

        st.subheader("Project Information")

        st.write(f"**Project ID:** PRJ-{project_id:03d}")
        st.write(f"**Status:** {project['status']}")

        if project["description"]:
            st.write(f"**Description:** {project['description']}")

    elif section == "Requirements":

        st.subheader("Requirements")

        with st.form("add_requirement_form"):

            requirement = st.text_input("Requirement")
            module = st.text_input("Module")

            priority = st.selectbox(
                "Priority",
                ["Critical", "High", "Medium", "Low"]
            )

            status = st.selectbox(
                "Status",
                ["Planned", "In Progress", "Completed"]
            )

            if st.form_submit_button(
                "Add Requirement",
                type="primary"
            ):

                if not requirement.strip():
                    st.error("Requirement cannot be empty.")
                else:
                    new_id = _next_id(cursor, "requirements")

                    cursor.execute(
                        """
                        INSERT INTO requirements
                        (
                            id,
                            project_id,
                            requirement,
                            module,
                            priority,
                            status
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            new_id,
                            project_id,
                            requirement.strip(),
                            module.strip(),
                            priority,
                            status
                        )
                    )

                    connection.commit()
                    st.success("Requirement added.")
                    st.rerun()

        st.divider()

        cursor.execute(
            """
            SELECT *
            FROM requirements
            WHERE project_id = %s
            ORDER BY id DESC
            """,
            (project_id,)
        )

        requirements = cursor.fetchall()

        if not requirements:
            st.info("No requirements added yet.")

        for item in requirements:

            with st.container(border=True):

                col1, col2, col3 = st.columns([5, 2, 1])

                with col1:
                    st.write(
                        f"REQ-{item['id']:03d}"
                    )
                    st.write(item["requirement"])
                    if item["module"]:
                        st.caption(
                            f"Module: {item['module']} | "
                            f"Priority: {item['priority']}"
                        )

                with col2:

                    statuses = [
                        "Planned",
                        "In Progress",
                        "Completed"
                    ]

                    current = item["status"]

                    new_status = st.selectbox(
                        "Status",
                        statuses,
                        index=(
                            statuses.index(current)
                            if current in statuses
                            else 0
                        ),
                        key=f"req_status_{item['id']}"
                    )

                    if new_status != current:

                        cursor.execute(
                            """
                            UPDATE requirements
                            SET status = %s
                            WHERE id = %s
                            """,
                            (
                                new_status,
                                item["id"]
                            )
                        )

                        connection.commit()
                        st.rerun()

                with col3:

                    if st.button(
                        "Delete",
                        key=f"delete_req_{item['id']}"
                    ):

                        cursor.execute(
                            "DELETE FROM requirements WHERE id = %s",
                            (item["id"],)
                        )

                        connection.commit()
                        st.rerun()

    elif section == "Features":

        st.subheader("Features")

        st.info(
            "Features are not stored in the current database schema yet."
        )

    elif section == "Tasks":

        st.subheader("Tasks")

        with st.form("add_task_form"):

            title = st.text_input("Task")

            module = st.selectbox(
                "Module",
                [
                    "Service Desk",
                    "Call Center",
                    "ANA",
                    "Alerts & Notifications",
                    "Reports",
                    "System Monitoring",
                    "Infrastructure",
                    "Platform"
                ]
            )

            priority = st.selectbox(
                "Priority",
                ["Critical", "High", "Medium", "Low"]
            )

            status = st.selectbox(
                "Status",
                ["To Do", "In Progress", "Testing", "Blocked", "Done"]
            )

            if st.form_submit_button(
                "Add Task",
                type="primary"
            ):

                if not title.strip():
                    st.error("Task cannot be empty.")
                else:

                    new_id = _next_id(cursor, "tasks")

                    completed_at = None

                    if status == "Done":
                        from datetime import datetime
                        completed_at = datetime.now().isoformat(
                            timespec="seconds"
                        )

                    cursor.execute(
                        """
                        INSERT INTO tasks
                        (
                            id,
                            project_id,
                            title,
                            module,
                            priority,
                            status,
                            completed_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            new_id,
                            project_id,
                            title.strip(),
                            module,
                            priority,
                            status,
                            completed_at
                        )
                    )

                    connection.commit()
                    st.success("Task added.")
                    st.rerun()

        st.divider()

        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE project_id = %s
            ORDER BY id DESC
            """,
            (project_id,)
        )

        tasks = cursor.fetchall()

        if not tasks:
            st.info("No tasks added yet.")

        for task in tasks:

            with st.container(border=True):

                col1, col2, col3 = st.columns([5, 2, 1])

                with col1:
                    st.write(
                        f"TASK-{task['id']:03d}"
                    )
                    st.write(task["title"])
                    st.caption(
                        f"Module: {task['module']} | "
                        f"Priority: {task['priority']}"
                    )

                with col2:

                    statuses = [
                        "To Do",
                        "In Progress",
                        "Testing",
                        "Blocked",
                        "Done"
                    ]

                    current = task["status"]

                    new_status = st.selectbox(
                        "Status",
                        statuses,
                        index=(
                            statuses.index(current)
                            if current in statuses
                            else 0
                        ),
                        key=f"task_status_{task['id']}"
                    )

                    if new_status != current:

                        from datetime import datetime

                        completed_at = None

                        if new_status == "Done":
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
                                new_status,
                                completed_at,
                                task["id"]
                            )
                        )

                        connection.commit()
                        st.rerun()

                with col3:

                    if st.button(
                        "Delete",
                        key=f"delete_task_{task['id']}"
                    ):

                        cursor.execute(
                            "DELETE FROM tasks WHERE id = %s",
                            (task["id"],)
                        )

                        connection.commit()
                        st.rerun()

    elif section == "Change Requests":

        st.subheader("Change Requests")

        with st.form("add_change_form"):

            requirement = st.text_input(
                "Requirement / Change"
            )

            reason = st.text_area("Reason")
            impact = st.text_area("Impact")

            if st.form_submit_button(
                "Add Change Request",
                type="primary"
            ):

                if not requirement.strip():
                    st.error("Change request cannot be empty.")
                else:

                    new_id = _next_id(
                        cursor,
                        "change_requests"
                    )

                    cursor.execute(
                        """
                        INSERT INTO change_requests
                        (
                            id,
                            project_id,
                            requirement,
                            reason,
                            impact
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            new_id,
                            project_id,
                            requirement.strip(),
                            reason.strip(),
                            impact.strip()
                        )
                    )

                    connection.commit()
                    st.success("Change request added.")
                    st.rerun()

        st.divider()

        cursor.execute(
            """
            SELECT *
            FROM change_requests
            WHERE project_id = %s
            ORDER BY id DESC
            """,
            (project_id,)
        )

        changes = cursor.fetchall()

        if not changes:
            st.info("No change requests yet.")

        for item in changes:

            with st.container(border=True):

                st.write(
                    f"CR-{item['id']:03d} — "
                    f"{item['requirement']}"
                )

                if item["reason"]:
                    st.caption(
                        f"Reason: {item['reason']}"
                    )

                if item["impact"]:
                    st.caption(
                        f"Impact: {item['impact']}"
                    )

                if st.button(
                    "Delete",
                    key=f"delete_change_{item['id']}"
                ):

                    cursor.execute(
                        """
                        DELETE FROM change_requests
                        WHERE id = %s
                        """,
                        (item["id"],)
                    )

                    connection.commit()
                    st.rerun()

    elif section == "Issues":

        st.subheader("Issues")

        with st.form("add_issue_form"):

            title = st.text_input("Issue")
            description = st.text_area("Description")

            priority = st.selectbox(
                "Priority",
                ["Critical", "High", "Medium", "Low"]
            )

            status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Resolved"]
            )

            if st.form_submit_button(
                "Add Issue",
                type="primary"
            ):

                if not title.strip():
                    st.error("Issue title cannot be empty.")
                else:

                    new_id = _next_id(cursor, "issues")

                    cursor.execute(
                        """
                        INSERT INTO issues
                        (
                            id,
                            project_id,
                            title,
                            description,
                            priority,
                            status
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            new_id,
                            project_id,
                            title.strip(),
                            description.strip(),
                            priority,
                            status
                        )
                    )

                    connection.commit()
                    st.success("Issue added.")
                    st.rerun()

        st.divider()

        cursor.execute(
            """
            SELECT *
            FROM issues
            WHERE project_id = %s
            ORDER BY id DESC
            """,
            (project_id,)
        )

        issues = cursor.fetchall()

        if not issues:
            st.info("No issues yet.")

        for issue in issues:

            with st.container(border=True):

                col1, col2 = st.columns([6, 1])

                with col1:

                    st.write(
                        f"ISSUE-{issue['id']:03d} — "
                        f"{issue['title']}"
                    )

                    st.caption(
                        f"Priority: {issue['priority']} | "
                        f"Status: {issue['status']}"
                    )

                    if issue["description"]:
                        st.write(issue["description"])

                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_issue_{issue['id']}"
                    ):

                        cursor.execute(
                            "DELETE FROM issues WHERE id = %s",
                            (issue["id"],)
                        )

                        connection.commit()
                        st.rerun()

    elif section == "Notes":

        st.subheader("Notes")

        with st.form("add_note_form"):

            note = st.text_area("Note")

            if st.form_submit_button(
                "Add Note",
                type="primary"
            ):

                if not note.strip():
                    st.error("Note cannot be empty.")
                else:

                    new_id = _next_id(cursor, "notes")

                    cursor.execute(
                        """
                        INSERT INTO notes
                        (
                            id,
                            project_id,
                            note
                        )
                        VALUES (%s, %s, %s)
                        """,
                        (
                            new_id,
                            project_id,
                            note.strip()
                        )
                    )

                    connection.commit()
                    st.success("Note added.")
                    st.rerun()

        st.divider()

        cursor.execute(
            """
            SELECT *
            FROM notes
            WHERE project_id = %s
            ORDER BY id DESC
            """,
            (project_id,)
        )

        notes = cursor.fetchall()

        if not notes:
            st.info("No notes yet.")

        for note in notes:

            with st.container(border=True):

                col1, col2 = st.columns([6, 1])

                with col1:
                    st.write(
                        f"NOTE-{note['id']:03d}"
                    )
                    st.write(note["note"])

                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_note_{note['id']}"
                    ):

                        cursor.execute(
                            "DELETE FROM notes WHERE id = %s",
                            (note["id"],)
                        )

                        connection.commit()
                        st.rerun()

    cursor.close()
    connection.close()





