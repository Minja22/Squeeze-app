import streamlit as st
import uuid

st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")
st.markdown("<h1 style='text-align: center;'>SQUEEZE</h1>", unsafe_allow_html=True)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def add_task(title, est):
    st.session_state.tasks.append({
        "id": str(uuid.uuid4()),
        "title": title,
        "estimated_time": est,
        "completed": False,
        "starred": False
    })
    st.experimental_rerun()

def toggle_complete(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
    st.experimental_rerun()

def toggle_star(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["starred"] = not task["starred"]
    st.experimental_rerun()

def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != task_id]
    st.experimental_rerun()

# Display tasks: Task text first, then a button row below it.
st.markdown("## To Do")
for task in st.session_state.tasks:
    # Task text row
    st.markdown(
        f"<div style='font-size:20px;color:{'#FFA500' if not task['completed'] else '#32CD32'};'>"
        f"{task['title']} <small style='color:#666;'>({task['estimated_time']} mins)</small></div>",
        unsafe_allow_html=True
    )
    # Button row: using st.columns to keep them in one row.
    btn_cols = st.columns(3)
    with btn_cols[0]:
        if st.button("✔", key=f"complete_{task['id']}"):
            toggle_complete(task["id"])
    with btn_cols[1]:
        if st.button("⭐" if task["starred"] else "☆", key=f"star_{task['id']}"):
            toggle_star(task["id"])
    with btn_cols[2]:
        if st.button("🗑", key=f"delete_{task['id']}"):
            delete_task(task["id"])
    st.markdown("---")
