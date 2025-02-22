import streamlit as st
import uuid

# Setup page config
st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")

# Initialize session state variables if not present
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

# --------------------------------
# Helper Functions
# --------------------------------
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

def edit_task(task_id, new_title, new_duration, new_starred):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            task["duration"] = new_duration
            task["starred"] = new_starred
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
    # Sort: starred tasks first, then by duration (ascending)
    pending.sort(key=lambda x: (not x["starred"], x["duration"]))
    for task in pending:
        if total + task["duration"] <= st.session_state.available_time:
            st.session_state.generated_tasks.append(task)
            total += task["duration"]

# --------------------------------
# Header and Dark Mode Toggle
# --------------------------------
st.markdown("# Squeeze - Smart To-Do List")

if st.button("Toggle Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply simple dark mode styling via CSS
bg_color = "#333333" if st.session_state.dark_mode else "#FFFFFF"
text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
st.markdown(f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
    </style>
    """, unsafe_allow_html=True)

# --------------------------------
# Task Sections: Active & Completed
# --------------------------------
active_tasks = [t for t in st.session_state.tasks if not t["completed"]]
completed_tasks = [t for t in st.session_state.tasks if t["completed"]]

st.markdown("## Active Tasks")
if active_tasks:
    for task in active_tasks:
        cols = st.columns([6, 1, 1, 1, 1])
        with cols[0]:
            # Display task title with duration and star indicator
            star_icon = "⭐" if task["starred"] else "☆"
            color = "#FFA500"  # Orange for active tasks
            st.markdown(f"<span style='font-size:18px; color:{color};'>{task['title']} ({task['duration']} min) {star_icon}</span>", unsafe_allow_html=True)
        with cols[1]:
            if st.button("Edit", key=f"edit_{task['id']}"):
                st.session_state.editing_task = task
        with cols[2]:
            if st.button("Complete", key=f"complete_{task['id']}"):
                toggle_complete(task["id"])
        with cols[3]:
            if st.button("Star", key=f"star_{task['id']}"):
                toggle_star(task["id"])
        with cols[4]:
            if st.button("Delete", key=f"delete_{task['id']}"):
                delete_task(task["id"])
else:
    st.markdown("No active tasks.")

st.markdown("## Completed Tasks")
if completed_tasks:
    for task in completed_tasks:
        cols = st.columns([7, 1, 1])
        with cols[0]:
            st.markdown(f"<span style='font-size:18px; color:#32CD32;'>{task['title']} ({task['duration']} min)</span>", unsafe_allow_html=True)
        with cols[1]:
            if st.button("Recover", key=f"recover_{task['id']}"):
                toggle_complete(task["id"])
        with cols[2]:
            if st.button("Delete", key=f"delete_completed_{task['id']}"):
                delete_task(task["id"])
else:
    st.markdown("No completed tasks.")

# --------------------------------
# Go Time Section
# --------------------------------
st.markdown("---")
if st.button("Go Time"):
    st.session_state.go_time_mode = True

if st.session_state.go_time_mode:
    st.markdown("### Go Time: Select Your Available Time")
    st.session_state.available_time = st.number_input("Available Time (minutes)", min_value=5, max_value=120, value=st.session_state.available_time, step=5)
    if st.button("Show Focused Tasks"):
        generate_go_time_tasks()
    if st.session_state.generated_tasks:
        st.markdown("#### Focused Tasks")
        for task in st.session_state.generated_tasks:
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(f"{task['title']} ({task['duration']} min)")
            with cols[1]:
                if st.button("Complete", key=f"complete_go_{task['id']}"):
                    toggle_complete(task["id"])
                    # Refresh the focused tasks after marking one complete
                    generate_go_time_tasks()

# --------------------------------
# Add Task Section
# --------------------------------
st.markdown("---")
if st.button("Add Task"):
    st.session_state.show_add_form = True

if st.session_state.show_add_form:
    st.markdown("### Add New Task")
    with st.form("add_task_form"):
        new_title = st.text_input("Task Title")
        new_duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=5, step=5)
        submitted = st.form_submit_button("Add Task")
        if submitted and new_title:
            add_task(new_title, new_duration)
            st.experimental_rerun()

# --------------------------------
# Edit Task Section
# --------------------------------
if st.session_state.editing_task is not None:
    task = st.session_state.editing_task
    st.markdown("### Edit Task")
    with st.form("edit_task_form"):
        updated_title = st.text_input("Task Title", value=task["title"])
        updated_duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=task["duration"], step=5)
        updated_starred = st.checkbox("Star Task", value=task["starred"])
        submitted = st.form_submit_button("Save")
        if submitted and updated_title:
            edit_task(task["id"], updated_title, updated_duration, updated_starred)
            st.experimental_rerun()
