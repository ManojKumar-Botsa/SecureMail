"""
Streamlit UI for SecureMail.
The FastAPI server should be running at localhost:7860.
"""

import requests
import streamlit as st

API = "http://localhost:7860"

st.set_page_config(page_title="SecureMail")
st.title("SecureMail")
st.caption("Classify each email as safe, suspicious, or phishing.")

# Sidebar: task selector
st.sidebar.header("Environment Controls")
try:
    tasks_data = requests.get(f"{API}/tasks", timeout=5).json()
    task_options = {
        f"[{t['difficulty'].upper()}] #{t['index']} - {t['category']}": t["index"]
        for t in tasks_data["tasks"]
    }
    selected_label = st.sidebar.selectbox("Select task", list(task_options.keys()))
    task_index = task_options[selected_label]
except Exception:
    task_index = None
    st.sidebar.warning("Could not load tasks. Is the server running?")

if st.sidebar.button("Reset Environment", use_container_width=True):
    payload = {"task_index": task_index} if task_index is not None else {}
    r = requests.post(f"{API}/reset", json=payload, timeout=10)
    st.session_state["obs"] = r.json()["observation"]
    st.session_state["result"] = None

# Main panel
obs = st.session_state.get("obs")

if obs is None:
    st.info("Press **Reset Environment** in the sidebar to load an email.")
else:
    st.subheader("Email")
    st.code(obs["email_text"], language=None)

    col1, col2, col3 = st.columns(3)
    action = None
    if col1.button("Safe", use_container_width=True):
        action = "safe"
    if col2.button("Suspicious", use_container_width=True):
        action = "suspicious"
    if col3.button("Phishing", use_container_width=True):
        action = "phishing"

    if action:
        r = requests.post(f"{API}/step", json={"label": action}, timeout=10)
        if r.status_code == 200:
            st.session_state["result"] = {**r.json(), "predicted": action}
        else:
            st.error(r.json().get("detail", "Server error"))

result = st.session_state.get("result")
if result:
    reward = result["reward"]
    info = result["info"]
    predicted = result["predicted"]
    expected = info["expected_label"]

    st.divider()
    st.subheader("Result")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Your prediction", predicted.upper())
    col_b.metric("Correct label", expected.upper())
    col_c.metric("Reward", f"{reward:.2f} / 0.99")

    if reward == 0.99:
        st.success("Correct.")
    elif reward == 0.5:
        st.warning(f"Close, but the correct label was **{expected}**.")
    else:
        st.error(f"Incorrect. This email was **{expected}**.")

    with st.expander("Explanation"):
        st.write(info.get("explanation", "No explanation available."))
        st.write(f"**Difficulty:** {info['difficulty']}  |  **Category:** {info['category']}")
