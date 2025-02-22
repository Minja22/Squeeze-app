import streamlit as st
import uuid

st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")

if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "editing_task" not in st.session_state:
    st.session_state.editing_task = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "go_time_mode" not in st.session_state:
    st.session_state.go_time_mode = False
if "available_time" not in st.session_state:
    st.session_state.available_time = 30
if "generated_tasks" not in st.session_state:
    st.session_state.generated_tasks = []

# Helper Functions
def add_task(title, duration):
    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "duration": duration,
        "completed": False,
        "starred": False
    }
    st.session_state.tasks.append(task)
    st.session_state.show_add_form = False

def edit_task(task_id, new_title, new_duration, starred):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            task["duration"] = new_duration
            task["starred"] = starred
    st.session_state.editing_task = None

def toggle_complete(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]

def toggle_star(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["starred"] = not task["starred"]

def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != task_id]

def generate_go_time_tasks():
    total = 0
    st.session_state.generated_tasks = []
    pending = [t for t in st.session_state.tasks if not t["completed"]]
    # Sort: starred first, then by duration
    pending.sort(key=lambda x: (not x["starred"], x["duration"]))
    for task in pending:
        if total + task["duration"] <= st.session_state.available_time:
            st.session_state.generated_tasks.append(task)
            total += task["duration"]

# UI Components

# Dark Mode Toggle (simulation)
if st.button("Toggle Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

# Display tasks in sections
active_tasks = [t for t in st.session_state.tasks if not t["completed"]]
completed_tasks = [t for t in st.session_state.tasks if t["completed"]]

st.markdown("# Squeeze - Smart To-Do List")
st.markdown("## Active Tasks")
for task in active_tasks:
    cols = st.columns([6, 1, 1, 1])
    with cols[0]:
        star_label = "⭐" if task["starred"] else "☆"
        st.markdown(f"<span style='font-size:18px; color: {'#FFA500' if not task['completed'] else '#32CD32'};'>{task['title']} ({task['duration']} min)</span>", unsafe_allow_html=True)
    with cols[1]:
        if st.button("Edit", key=f"edit_{task['id']}"):
            st.session_state.editing_task = task
    with cols[2]:
        if st.button("✔", key=f"complete_{task['id']}"):
            toggle_complete(task["id"])
    with cols[3]:
        if st.button("🗑", key=f"delete_{task['id']}"):
            delete_task(task["id"])

st.markdown("## Completed Tasks")
for task in completed_tasks:
    cols = st.columns([6, 1])
    with cols[0]:
        st.markdown(f"<span style='font-size:18px; color:#32CD32;'>{task['title']} ({task['duration']} min)</span>", unsafe_allow_html=True)
    with cols[1]:
        if st.button("Recover", key=f"recover_{task['id']}"):
            toggle_complete(task["id"])

# Go Time Section
st.markdown("---")
if st.button("Go Time"):
    st.session_state.go_time_mode = True
if st.session_state.go_time_mode:
    st.markdown("### How much time do you have?")
    st.session_state.available_time = st.number_input("Available Time (minutes)", min_value=5, max_value=120, value=st.session_state.available_time, step=5)
    if st.button("Show Focused Tasks"):
        generate_go_time_tasks()
    if st.session_state.generated_tasks:
        st.markdown("#### Focused Tasks")
        for task in st.session_state.generated_tasks:
            col1, col2 = st.columns([6,1])
            with col1:
                st.markdown(f"{task['title']} ({task['duration']} min)")
            with col2:
                if st.button("Complete", key=f"complete_go_{task['id']}"):
                    toggle_complete(task["id"])
                    # Optionally remove from generated_tasks after marking complete

# Add Task Form (simulated modal)
if st.button("Add Task"):
    st.session_state.show_add_form = True

if st.session_state.show_add_form:
    st.markdown("### Add New Task")
    with st.form("add_task_form"):
        title = st.text_input("Task Title")
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=5, step=5)
        submitted = st.form_submit_button("Add Task")
        if submitted and title:
            add_task(title, duration)

# Edit Task Form (simulated modal)
if st.session_state.editing_task:
    task = st.session_state.editing_task
    st.markdown("### Edit Task")
    with st.form("edit_task_form"):
        new_title = st.text_input("Task Title", value=task["title"])
        new_duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=task["duration"], step=5)
        new_starred = st.checkbox("Star Task", value=task["starred"])
        submitted = st.form_submit_button("Save")
        if submitted:
            edit_task(task["id"], new_title, new_duration, new_starred)
