# streamlit_app/auth_helpers.py
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ============================
# BACKEND URL
# ============================
def get_backend_url() -> str:
    url = os.getenv("BACKEND_URL")
    if url:
        return url.rstrip("/")  # sacamos / final si lo hubiera
    return "http://127.0.0.1:8000"


# ============================
# SESSION AUTH
# ============================
def set_auth_session(data: dict) -> None:
    if not isinstance(data, dict):
        return

    token = data.get("access_token") or data.get("token") or data.get("jwt")
    if token:
        st.session_state["auth_token"] = token

    user = data.get("user")
    if not isinstance(user, dict):
        user = data if isinstance(data, dict) else {}

    st.session_state["user"] = user

    premium_val = user.get("premium", data.get("premium", 0))
    try:
        premium_val = int(premium_val or 0)
    except Exception:
        premium_val = 0

    st.session_state["premium"] = premium_val
    user["premium"] = premium_val
    st.session_state["user"] = user

    roles_raw = user.get("roles") or user.get("role") or data.get("roles") or []
    if isinstance(roles_raw, str):
        roles_raw = [roles_raw]

    roles = []
    for r in roles_raw:
        if isinstance(r, dict):
            name = r.get("name") or r.get("role") or r.get("code") or r.get("codigo")
            if name:
                roles.append(str(name).upper())
        else:
            roles.append(str(r).upper())

    st.session_state["roles"] = roles
    st.session_state["auth_roles"] = roles
    st.session_state["is_admin"] = "ADMIN" in roles

    uid = user.get("id") or user.get("user_id") or data.get("user_id") or data.get("id")
    if uid:
        st.session_state["auth_user_id"] = uid

    st.session_state["auth_user_name"] = user.get("nombre") or user.get("email")
    st.session_state["auth_user_email"] = user.get("email")


# ============================
# HELPERS COMPARTIDOS
# ============================
def auth_headers() -> dict:
    tok = st.session_state.get("auth_token")
    return {"Authorization": f"Bearer {tok}"} if tok else {}


def require_login():
    if "auth_token" not in st.session_state:
        st.warning("Tenés que iniciar sesión.")
        st.page_link("pages/0_Login.py", label="Ir a Login", icon="🔐")
        st.stop()


def require_admin():
    require_login()
    roles = [str(r).upper() for r in st.session_state.get("roles", [])]
    if "ADMIN" not in roles:
        st.error("No tenés permisos para acceder a este panel.")
        st.stop()
