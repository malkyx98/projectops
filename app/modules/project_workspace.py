import streamlit as st


def show(project):

    project_id = project["id"]
    project_name = project["name"]

    st.title(project_name)

    if project["description"]:
        st.caption(project["description"])

    st.divider()

    section = st.radio(
        "Project Workspace",
        [
            "Overview",
            "Requirements",
            "Features",
            "Tasks",
            "Change Requests",
            "Issues",
            "Notes",
            "Progress"
        ],
        horizontal=True
    )

    st.divider()

    if section == "Overview":

        st.subheader("Project Overview")

        st.info(
            "This is the project workspace. "
            "Requirements, features, tasks, changes, "
            "issues and notes will be managed inside this project."
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Requirements", "0")

        with col2:
            st.metric("Features", "0")

        with col3:
            st.metric("Tasks", "0")

        with col4:
            st.metric("Progress", "0%")

    elif section == "Requirements":

        st.subheader("Requirements")

        st.info(
            "Project requirements will be managed here."
        )

    elif section == "Features":

        st.subheader("Features")

        st.info(
            "Project features will be managed here."
        )

    elif section == "Tasks":

        st.subheader("Tasks")

        st.info(
            "Project tasks will be managed here."
        )

    elif section == "Change Requests":

        st.subheader("Change Requests")

        st.info(
            "Requirement changes will be tracked here."
        )

    elif section == "Issues":

        st.subheader("Issues")

        st.info(
            "Project issues will be tracked here."
        )

    elif section == "Notes":

        st.subheader("Notes")

        st.info(
            "Project notes will be stored here."
        )

    elif section == "Progress":

        st.subheader("Project Progress")

        st.info(
            "Project progress tracking will be implemented here."
        )
