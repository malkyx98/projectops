import streamlit as st

from auth import sign_in, sign_up, sign_out, get_current_user
from database import initialize_database
from modules import projects


st.set_page_config(
    page_title="ProjectOps",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)


st.markdown(
    """
    <style>

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .block-container {
        max-width: 430px;
        padding-top: 12vh;
        padding-bottom: 4rem;
    }

    html, body, [class*="css"] {
        font-family: "Segoe UI", Arial, sans-serif;
    }

    .projectops-heading {
        text-align: center;
        font-family: "Brush Script MT", "Segoe Script", cursive;
        font-size: 4.2rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: var(--text-color);
        margin-bottom: 0.1rem;
        line-height: 1.1;
    }

    .login-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .login-description {
        color: var(--secondary-text-color);
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 1.6rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 2rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: var(--text-color);
    }

    .stTextInput label {
        font-weight: 600;
        color: var(--text-color);
    }

    .stTextInput input {
        border-radius: 8px;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 44px;
    }

    .login-footer {
        text-align: center;
        color: var(--secondary-text-color);
        font-size: 0.78rem;
        margin-top: 3rem;
    }

    :root {
        --text-color: #0f172a;
        --secondary-text-color: #64748b;
        --border-color: #e2e8f0;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #f8fafc;
            --secondary-text-color: #94a3b8;
            --border-color: #334155;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


def login_screen():

    st.markdown(
        '<div class="projectops-heading">ProjectOps</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">Welcome back</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-description">Sign in to continue to your workspace.</div>',
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        ["Sign In", "Create Account"]
    )

    with login_tab:

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True
        ):

            if not email.strip() or not password:
                st.error("Please enter your email and password.")
                return

            try:

                response = sign_in(
                    email.strip(),
                    password
                )

                if response.get("user"):

                    st.session_state["user"] = response["user"]
                    st.session_state["access_token"] = response.get(
                        "access_token"
                    )
                    st.session_state["refresh_token"] = response.get(
                        "refresh_token"
                    )

                    st.rerun()

            except Exception as error:

                st.error(f"Sign in failed: {error}")

    with signup_tab:

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Repeat your password",
            key="signup_confirm_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not email.strip():
                st.error("Please enter your email.")
                return

            if not password:
                st.error("Please enter a password.")
                return

            if password != confirm_password:
                st.error("Passwords do not match.")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters.")
                return

            try:

                response = sign_up(
                    email.strip(),
                    password
                )

                if response.get("user"):

                    if response.get("access_token"):

                        st.session_state["user"] = response["user"]
                        st.session_state["access_token"] = response.get(
                            "access_token"
                        )
                        st.session_state["refresh_token"] = response.get(
                            "refresh_token"
                        )

                        st.rerun()

                    else:

                        st.success(
                            "Account created. Check your email to confirm your account."
                        )

            except Exception as error:

                st.error(f"Account creation failed: {error}")

    st.markdown(
        '<div class="login-footer">ProjectOps · Secure project management</div>',
        unsafe_allow_html=True
    )


def main():

    if "user" not in st.session_state:

        login_screen()
        return

    user = get_current_user()

    if not user:

        st.session_state.pop("user", None)
        login_screen()
        return

    with st.sidebar:

        st.write("Signed in as")

        st.caption(
            user.get("email", "User")
            if isinstance(user, dict)
            else "User"
        )

        if st.button(
            "Sign out",
            use_container_width=True
        ):

            sign_out()
            st.rerun()

    initialize_database()

    projects.show()


if __name__ == "__main__":
    main()
