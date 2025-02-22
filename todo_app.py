import streamlit as st
import uuid

st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def add_task(title, estimated_time):
    task = {"id": str(uuid.uuid4()), "title": title, "estimated_time": estimated_time, "completed": False, "starred": False}
    st.session_state.tasks.append(task)
    st.rerun()

def toggle_complete(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
    st.rerun()

def toggle_star(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["starred"] = not task["starred"]
    st.rerun()

def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != task_id]
    st.rerun()

st.markdown("# Squeeze - Smart To-Do List")

if st.button("Go Time"):
    st.session_state.tasks = sorted(st.session_state.tasks, key=lambda x: (not x["starred"], x["completed"]))
    st.rerun()

for task in st.session_state.tasks:
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    with col1:
        task_color = "#FFA500" if not task["completed"] else "#32CD32"
        st.markdown(f"<span style='color:{task_color}; font-size:20px;'>{task['title']}</span>", unsafe_allow_html=True)
    with col2:
        if st.button("✔", key=f"complete_{task['id']}"):
            toggle_complete(task["id"])
    with col3:
        if st.button("⭐" if task["starred"] else "☆", key=f"star_{task['id']}"):
            toggle_star(task["id"])
    with col4:
        if st.button("🗑", key=f"delete_{task['id']}"):
            delete_task(task["id"])

st.markdown("---")

new_task_title = st.text_input("Enter Task Title", "")
new_task_time = st.number_input("Estimated Time (minutes)", min_value=1, max_value=120, value=5, step=5)
if st.button("Add Task") and new_task_title:
    add_task(new_task_title, new_task_time)
