import streamlit as st

from services.project_service import get_projects
from services.task_service import (
    get_tasks,
    add_task,
    update_task_status
)


MODULES = [
    "Service Desk",
    "Call Center",
    "ANA",
    "Alerts & Notifications",
    "Reports",
    "System Monitoring",
    "Infrastructure",
    "Platform"
]

PRIORITIES = [
    "Critical",
    "High",
    "Medium",
    "Low"
]

STATUSES = [
    "To Do",
    "In Progress",
    "Testing",
    "Blocked",
    "Done"
]


def show():

    st.title("Tasks")

    projects = get_projects()

    if not projects:
        st.warning("Create a project first.")
        return

    project_names = {
        project["name"]: project["id"]
        for project in projects
    }

    selected_project = st.selectbox(
        "Project",
        list(project_names.keys())
    )

    project_id = project_names[selected_project]

    st.subheader("Add Task")

    with st.form("add_task"):

        title = st.text_input("Task")

        module = st.selectbox(
            "Module",
            MODULES
        )

        priority = st.selectbox(
            "Priority",
            PRIORITIES
        )

        status = st.selectbox(
            "Status",
            STATUSES
        )

        submitted = st.form_submit_button(
            "Add Task"
        )

        if submitted:

            if not title.strip():

                st.error(
                    "Task cannot be empty."
                )

            else:

                add_task(
                    project_id,
                    title.strip(),
                    module,
                    priority,
                    status
                )

                st.success(
                    "Task added."
                )

                st.rerun()

    st.divider()

    st.subheader("Project Tasks")

    tasks = get_tasks(project_id)

    if not tasks:

        st.info(
            "No tasks added yet."
        )

        return

    for task in tasks:

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 2]
            )

            with col1:

                st.write(
                    f"TASK-{task['id']:03d}"
                )

                st.write(
                    task["title"]
                )

            with col2:

                st.write(
                    f"Module: {task['module']}"
                )

                st.write(
                    f"Priority: {task['priority']}"
                )

            with col3:

                current_status = task["status"]

                new_status = st.selectbox(
                    "Status",
                    STATUSES,
                    index=STATUSES.index(
                        current_status
                    )
                    if current_status in STATUSES
                    else 0,
                    key=f"task_status_{task['id']}"
                )

                if new_status != current_status:

                    update_task_status(
                        task["id"],
                        new_status
                    )

                    st.rerun()
