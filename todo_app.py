import streamlit as st
import uuid

st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")

# Initialize session state variables
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "optimized_tasks" not in st.session_state:
    st.session_state.optimized_tasks = []
if "go_time_prompt" not in st.session_state:
    st.session_state.go_time_prompt = False

def add_task(title, estimated_time):
    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "estimated_time": estimated_time,
        "completed": False,
        "starred": False,
    }
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

def generate_optimized_tasks(time_available):
    # Filter only pending tasks
    pending_tasks = [task for task in st.session_state.tasks if not task["completed"]]
    # Sort tasks by estimated time (ascending)
    pending_tasks.sort(key=lambda x: x["estimated_time"])
    optimized = []
    total = 0
    for task in pending_tasks:
        if total + task["estimated_time"] <= time_available:
            optimized.append(task)
            total += task["estimated_time"]
    return optimized

st.markdown("# Squeeze - Smart To-Do List")

# Activate the time prompt when "Go Time" is clicked.
if st.button("Go Time"):
    st.session_state.go_time_prompt = True
    st.rerun()

# Display the time prompt if active.
if st.session_state.go_time_prompt:
    # Let the number input manage its state via a unique key.
    time_value = st.number_input(
        "How much time do you have? (in minutes)",
        min_value=1,
        max_value=480,
        value=30,
        key="time_input"
    )
    if st.button("Generate Optimized List", key="generate_optimized"):
        st.session_state.optimized_tasks = generate_optimized_tasks(time_value)
        st.session_state.go_time_prompt = False
        # No st.rerun() here so that the widget's value persists naturally.

st.markdown("## Master Task List")
for task in st.session_state.tasks:
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    with col1:
        task_color = "#FFA500" if not task["completed"] else "#32CD32"
        st.markdown(
            f"<span style='color:{task_color}; font-size:20px;'>{task['title']}</span>",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("✔", key=f"complete_{task['id']}"):
            toggle_complete(task["id"])
    with col3:
        if st.button("⭐" if task["starred"] else "☆", key=f"star_{task['id']}"):
            toggle_star(task["id"])
    with col4:
        if st.button("🗑", key=f"delete_{task['id']}"):
