import requests
import streamlit as st


def get_supabase_headers():
    return {
        "apikey": st.secrets["SUPABASE_KEY"],
        "Content-Type": "application/json"
    }


def sign_up(email, password):

    url = (
        st.secrets["SUPABASE_URL"]
        + "/auth/v1/signup"
    )

    response = requests.post(
        url,
        headers=get_supabase_headers(),
        json={
            "email": email,
            "password": password
        },
        timeout=30
    )

    if not response.ok:
        raise RuntimeError(
            response.json().get(
                "msg",
                response.text
            )
        )

    return response.json()


def sign_in(email, password):

    url = (
        st.secrets["SUPABASE_URL"]
        + "/auth/v1/token?grant_type=password"
    )

    response = requests.post(
        url,
        headers=get_supabase_headers(),
        json={
            "email": email,
            "password": password
        },
        timeout=30
    )

    if not response.ok:
        raise RuntimeError(
            response.json().get(
                "msg",
                response.text
            )
        )

    return response.json()


def sign_out():
    st.session_state.pop("user", None)
    st.session_state.pop("access_token", None)
    st.session_state.pop("refresh_token", None)


def get_current_user():
    return st.session_state.get("user")
