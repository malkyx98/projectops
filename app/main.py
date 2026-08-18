import streamlit as st

from database import initialize_database
from modules import projects


initialize_database()


st.set_page_config(
    page_title="ProjectOps",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown(
    """
    <style>

    /* Remove Streamlit navigation/sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    /* Main application */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Global typography */
    html, body, [class*="css"] {
        font-family: "Segoe UI", Arial, sans-serif;
    }

    /* Main title */
    .app-brand {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.15rem;
    }

    .app-subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* Project cards */
    .project-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    .project-card:hover {
        border-color: #94a3b8;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.08);
    }

    .project-name {
        font-size: 1.15rem;
        font-weight: 650;
        color: #0f172a;
    }

    .project-description {
        color: #64748b;
        margin-top: 0.45rem;
        margin-bottom: 0.9rem;
        line-height: 1.5;
    }

    .status-active {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .status-completed {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .status-archived {
        display: inline-block;
        background: #f1f5f9;
        color: #475569;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Section headings */
    .section-title {
        font-size: 1.25rem;
        font-weight: 650;
        color: #0f172a;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Workspace header */
    .workspace-header {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .workspace-title {
        font-size: 1.7rem;
        font-weight: 700;
        color: #0f172a;
    }

    .workspace-subtitle {
        color: #64748b;
        margin-top: 0.4rem;
    }

    /* Metrics */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #0f172a;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding-left: 1rem;
        padding-right: 1rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


projects.show()
