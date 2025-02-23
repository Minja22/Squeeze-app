import streamlit as st
import uuid

st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")
st.markdown("<h1 style='text-align: center;'>SQUEEZE</h1>", unsafe_allow_html=True)

# For demo purposes, initialize some tasks if none exist.
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": str(uuid.uuid4()), "title": "Task One", "estimated_time": 15, "completed": False, "starred": False},
        {"id": str(uuid.uuid4()), "title": "Task Two", "estimated_time": 30, "completed": False, "starred": True},
    ]

def toggle_complete(task_id):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["completed"] = not t["completed"]
    st.experimental_rerun()

def toggle_star(task_id):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["starred"] = not t["starred"]
    st.experimental_rerun()

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    st.experimental_rerun()

st.markdown("## To Do")
for task in st.session_state.tasks:
    # Create a single row with minimal spacing using very narrow columns for the buttons.
    cols = st.columns([7, 0.5, 0.5, 0.5])
    with cols[0]:
        color = "#FFA500" if not task["completed"] else "#32CD32"
        st.markdown(
            f"<span style='font-size:20px; color:{color};'>{task['title']}</span> "
            f"<small>({task['estimated_time']} mins)</small>",
            unsafe_allow_html=True,
        )
    with cols[1]:
        if st.button("✔", key=f"complete_{task['id']}"):
            toggle_complete(task["id"])
    with cols[2]:
        if st.button("⭐" if task["starred"] else "☆", key=f"star_{task['id']}"):
            toggle_star(task["id"])
    with cols[3]:
        if st.button("🗑", key=f"delete_{task['id']}"):
            delete_task(task["id"])
