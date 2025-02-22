import streamlit as st
import uuid

class Task:
    def __init__(self, title, estimated_time, is_completed=False, is_starred=False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.estimated_time = estimated_time
        self.is_completed = is_completed
        self.is_starred = is_starred

# Load or initialize tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def add_task(title, estimated_time):
    if title:
        new_task = Task(title, estimated_time)
        st.session_state.tasks.append(new_task)

def toggle_completion(task_id):
    for task in st.session_state.tasks:
        if task.id == task_id:
            task.is_completed = not task.is_completed
            break

def toggle_star(task_id):
    for task in st.session_state.tasks:
        if task.id == task_id:
            task.is_starred = not task.is_starred
            break

def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task.id != task_id]

# UI Layout
st.title("Clear-Inspired Task Manager")

if st.button("Go Time"):
    # Logic for Go Time execution
    st.write("Starting focus mode...")

# Display tasks
for task in sorted(st.session_state.tasks, key=lambda t: (not task.is_starred, task.is_completed)):
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    with col1:
        if st.button(f"{'✔️' if task.is_completed else '⬜'} {task.title}", key=task.id):
            toggle_completion(task.id)
    with col2:
        if st.button("⭐" if task.is_starred else "☆", key=f"star_{task.id}"):
            toggle_star(task.id)
    with col3:
        if st.button("🗑️", key=f"del_{task.id}"):
            delete_task(task.id)

# Add new task by tapping anywhere
if st.button("+ Add Task", key="add_task_button"):
    new_task_title = st.text_input("Task Title")
    new_task_time = st.number_input("Estimated Time (min)", min_value=1, value=5, step=1)
    if st.button("Confirm Add"):
        add_task(new_task_title, new_task_time)
        st.experimental_rerun()
