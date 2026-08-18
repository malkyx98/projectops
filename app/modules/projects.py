import streamlit as st

from services.project_service import (
    get_projects,
    add_project,
    delete_project,
)

from modules import project_workspace


def show():

    st.title("ProjectOps")

    st.caption(
        "Manage projects, requirements, tasks and changes from one workspace."
    )

    projects = get_projects()

    # ---------------------------------------------------------
    # SESSION STATE
    # ---------------------------------------------------------

    if "show_create_project" not in st.session_state:
        st.session_state["show_create_project"] = False

    if "selected_project_id" not in st.session_state:
        st.session_state["selected_project_id"] = None

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    header_col, button_col = st.columns([5, 1])

    with header_col:
        st.subheader("Projects")

    with button_col:

        if st.button(
            "+ New Project",
            type="primary",
            use_container_width=True,
            key="new_project_button",
        ):

            st.session_state["show_create_project"] = True
            st.session_state["selected_project_id"] = None

            st.rerun()

    # ---------------------------------------------------------
    # CREATE PROJECT
    # ---------------------------------------------------------

    if st.session_state["show_create_project"]:

        with st.container(border=True):

            st.subheader("Create New Project")

            with st.form("create_project_form"):

                name = st.text_input(
                    "Project name",
                    placeholder="Example: CXP Service Desk & Call Center",
                )

                description = st.text_area(
                    "Description",
                    placeholder="Describe the purpose of this project.",
                )

                col1, col2 = st.columns(2)

                with col1:

                    create = st.form_submit_button(
                        "Create Project",
                        type="primary",
                        use_container_width=True,
                    )

                with col2:

                    cancel = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

                if cancel:

                    st.session_state["show_create_project"] = False

                    st.rerun()

                if create:

                    if not name.strip():

                        st.error(
                            "Project name cannot be empty."
                        )

                    else:

                        add_project(
                            name.strip(),
                            description.strip(),
                        )

                        st.session_state[
                            "show_create_project"
                        ] = False

                        st.rerun()

    # ---------------------------------------------------------
    # NO PROJECTS
    # ---------------------------------------------------------

    if not projects:

        st.info(
            "No projects yet. Click '+ New Project' "
            "to create your first project."
        )

        return

    # ---------------------------------------------------------
    # PROJECT LIST
    # ---------------------------------------------------------

    st.divider()

    project_columns = st.columns(2)

    for index, project in enumerate(projects):

        with project_columns[index % 2]:

            with st.container(border=True):

                st.subheader(project["name"])

                status = project["status"]

                if status == "Active":

                    st.success("ACTIVE")

                elif status == "Completed":

                    st.info("COMPLETED")

                elif status == "On Hold":

                    st.warning("ON HOLD")

                else:

                    st.caption(status)

                description = project["description"]

                if description:

                    st.write(description)

                else:

                    st.caption(
                        "No description provided."
                    )

                st.divider()

                metric1, metric2 = st.columns(2)

                with metric1:

                    st.caption("Project ID")

                    st.write(
                        f"PRJ-{project['id']:03d}"
                    )

                with metric2:

                    st.caption("Status")

                    st.write(status)

                # -------------------------------------------------
                # OPEN PROJECT
                # -------------------------------------------------

                if st.button(
                    "Open Project",
                    key=f"open_project_{project['id']}",
                    type="primary",
                    use_container_width=True,
                ):

                    st.session_state[
                        "selected_project_id"
                    ] = project["id"]

                    st.session_state[
                        "show_create_project"
                    ] = False

                    st.rerun()

                # -------------------------------------------------
                # DELETE PROJECT
                # -------------------------------------------------

                if st.button(
                    "Delete Project",
                    key=f"delete_project_{project['id']}",
                    use_container_width=True,
                ):

                    try:

                        delete_project(
                            project["id"]
                        )

                        if (
                            st.session_state[
                                "selected_project_id"
                            ]
                            == project["id"]
                        ):

                            st.session_state[
                                "selected_project_id"
                            ] = None

                        st.success(
                            f"Project '{project['name']}' deleted."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to delete project: {error}"
                        )

    # ---------------------------------------------------------
    # PROJECT WORKSPACE
    # ---------------------------------------------------------

    selected_project_id = (
        st.session_state["selected_project_id"]
    )

    if selected_project_id:

        selected_project = next(
            (
                project
                for project in projects
                if project["id"] == selected_project_id
            ),
            None,
        )

        if selected_project:

            st.divider()

            # IMPORTANT:
            # Do NOT add another Back to Projects button here.
            # project_workspace.py already contains it.

            project_workspace.show(
                selected_project
            )



