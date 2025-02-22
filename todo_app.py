import streamlit as st
from dataclasses import dataclass, field
import uuid

# ------------------------------
# Task Model
# ------------------------------
@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    duration: int = 5
    completed: bool = False

# ------------------------------
# Initialize Session State
# ------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ------------------------------
# Helper Functions
# ------------------------------
def add_task(title, duration):
    st.session_state.tasks.append(Task(title=title, duration=duration))

def update_task(task_id, title, duration):
    for i, task in enumerate(st.session_state.tasks):
        if task.id == task_id:
            st.session_state.tasks[i].title = title
            st.session_state.tasks[i].duration = duration
            break

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t.id != task_id]

def mark_task_complete(task_id):
    for task in st.session_state.tasks:
        if task.id == task_id:
            task.completed = True
            break

def recover_task(task_id):
    for task in st.session_state.tasks:
        if task.id == task_id:
            task.completed = False
            break

def get_active_tasks():
    return [t for t in st.session_state.tasks if not t.completed]

def get_completed_tasks():
    return [t for t in st.session_state.tasks if t.completed]

# ------------------------------
# Main App UI
# ------------------------------
st.title("Squeeze - Task Manager")

# Navigation Sidebar
page = st.sidebar.radio("Navigation", ["Tasks", "Go Time"])

# ------------------------------
# TASKS PAGE
# ------------------------------
if page == "Tasks":
    st.header("Tasks")

    # Add New Task Form
    with st.expander("Add New Task", expanded=True):
        with st.form("add_task_form"):
            new_title = st.text_input("Task Title")
            new_duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, step=5, value=5)
            submitted = st.form_submit_button("Add Task")
            if submitted:
                if new_title.strip():
                    add_task(new_title.strip(), new_duration)
                    st.success("Task added!")
                else:
                    st.error("Please enter a task title.")

    # Active Tasks
    st.subheader("Active Tasks")
    active = get_active_tasks()
    if active:
        for task in active:
            col1, col2, col3, col4 = st.columns([3,1,1,1])
            with col1:
                st.write(f"**{task.title}** ({task.duration} min)")
            with col2:
                if st.button("Edit", key=f"edit_{task.id}"):
                    st.session_state[f"edit_{task.id}"] = True
            with col3:
                if st.button("Complete", key=f"complete_{task.id}"):
                    mark_task_complete(task.id)
                    st.experimental_rerun()
            with col4:
                if st.button("Delete", key=f"delete_{task.id}"):
                    delete_task(task.id)
                    st.experimental_rerun()

            # Inline Edit Form for the Task
            if st.session_state.get(f"edit_{task.id}", False):
                with st.form(f"edit_form_{task.id}"):
                    new_title_edit = st.text_input("Edit Title", value=task.title)
                    new_duration_edit = st.number_input("Edit Duration", min_value=5, max_value=120, step=5, value=task.duration)
                    if st.form_submit_button("Save"):
                        if new_title_edit.strip():
                            update_task(task.id, new_title_edit.strip(), new_duration_edit)
                            st.session_state[f"edit_{task.id}"] = False
                            st.success("Task updated!")
                            st.experimental_rerun()
                        else:
                            st.error("Task title cannot be empty.")
    else:
        st.info("No active tasks.")

    # Completed Tasks
    st.subheader("Completed Tasks")
    completed = get_completed_tasks()
    if completed:
        for task in completed:
            col1, col2, col3, col4 = st.columns([3,1,1,1])
            with col1:
                st.write(f"~~**{task.title}** ({task.duration} min)~~")
            with col2:
                if st.button("Edit", key=f"edit_{task.id}"):
                    st.session_state[f"edit_{task.id}"] = True
            with col3:
                if st.button("Recover", key=f"recover_{task.id}"):
                    recover_task(task.id)
                    st.experimental_rerun()
            with col4:
                if st.button("Delete", key=f"delete_{task.id}"):
                    delete_task(task.id)
                    st.experimental_rerun()

            # Inline Edit Form for Completed Task
            if st.session_state.get(f"edit_{task.id}", False):
                with st.form(f"edit_form_{task.id}"):
                    new_title_edit = st.text_input("Edit Title", value=task.title)
                    new_duration_edit = st.number_input("Edit Duration", min_value=5, max_value=120, step=5, value=task.duration)
                    if st.form_submit_button("Save"):
                        if new_title_edit.strip():
                            update_task(task.id, new_title_edit.strip(), new_duration_edit)
                            st.session_state[f"edit_{task.id}"] = False
                            st.success("Task updated!")
                            st.experimental_rerun()
                        else:
                            st.error("Task title cannot be empty.")
    else:
        st.info("No completed tasks yet.")

# ------------------------------
# GO TIME PAGE
# ------------------------------
elif page == "Go Time":
    st.header("Go Time")
    with st.form("go_time_form"):
        available_time = st.number_input("How much time do you have? (minutes)", min_value=5, max_value=120, step=5, value=30)
        submit_go_time = st.form_submit_button("Show Focused Tasks")

    if submit_go_time:
        total = 0
        focused_tasks = []
        # Sort active tasks by duration (shorter first)
        for task in sorted(get_active_tasks(), key=lambda t: t.duration):
            if total + task.duration <= available_time:
                focused_tasks.append(task)
                total += task.duration
        st.write(f"**Available Time:** {available_time} minutes")
        st.write(f"**Total Scheduled:** {total} minutes")
        if focused_tasks:
            for task in focused_tasks:
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"**{task.title}** ({task.duration} min)")
                with col2:
                    if st.button("Mark Complete", key=f"go_complete_{task.id}"):
                        mark_task_complete(task.id)
                        st.experimental_rerun()
        else:
            st.info("No tasks fit into your available time.")
