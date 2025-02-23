import streamlit as st
import uuid

st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")

# Big centered header for the app
st.markdown("<h1 style='text-align: center;'>SQUEEZE</h1>", unsafe_allow_html=True)

# Initialize session state variables if not already set
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "optimized_tasks" not in st.session_state:
    st.session_state.optimized_tasks = []
if "go_time_prompt" not in st.session_state:
    st.session_state.go_time_prompt = False
if "show_task_input" not in st.session_state:
    st.session_state.show_task_input = False

def add_task(title, estimated_time):
    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "estimated_time": estimated_time,
        "completed": False,
        "starred": False,
    }
    st.session_state.tasks.append(task)
    st.session_state.show_task_input = False  # hide task input after adding
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
    pending_tasks = [task for task in st.session_state.tasks if not task["completed"]]
    starred = [t for t in pending_tasks if t["starred"]]
    non_starred = [t for t in pending_tasks if not t["starred"]]
    starred.sort(key=lambda x: x["estimated_time"])
    non_starred.sort(key=lambda x: x["estimated_time"])
    
    optimized = []
    total = 0
    # Add starred tasks first
    for task in starred:
        if total + task["estimated_time"] <= time_available:
            optimized.append(task)
            total += task["estimated_time"]
    # Then add non-starred tasks
    for task in non_starred:
        if total + task["estimated_time"] <= time_available:
            optimized.append(task)
            total += task["estimated_time"]
    return optimized

# --- Optimized Task List (displayed at the very top) ---
if st.session_state.optimized_tasks and all(task["completed"] for task in st.session_state.optimized_tasks):
    st.session_state.optimized_tasks = []

if st.session_state.optimized_tasks:
    st.markdown("## Optimized Task List")
    if st.button("Out of Time", key="out_of_time"):
        st.session_state.optimized_tasks = []
        st.rerun()
    for task in st.session_state.optimized_tasks:
        col1, col2 = st.columns([6, 0.8])
        with col1:
            task_color = "#FFA500" if not task["completed"] else "#32CD32"
            st.markdown(
                f"<span style='color:{task_color}; font-size:20px;'>{task['title']}</span> "
                f"<small style='color:#666;'>({task['estimated_time']} mins)</small>",
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("✔", key=f"opt_complete_{task['id']}"):
                toggle_complete(task["id"])
    total_time = sum(task["estimated_time"] for task in st.session_state.optimized_tasks)
    st.markdown(f"**Total Scheduled Time:** {total_time} minutes")
st.markdown("---")

# --- Row for Task Creation and "Let's Go" Buttons ---
cols = st.columns(2)
with cols[0]:
    if st.button("➕", key="show_task_input_button"):
        st.session_state.show_task_input = not st.session_state.show_task_input
        st.rerun()
with cols[1]:
    if st.button("Let's Go", key="lets_go_button"):
        st.session_state.go_time_prompt = not st.session_state.go_time_prompt
        st.rerun()

# --- Input Fields Below the Button Row ---
if st.session_state.show_task_input:
    new_task_title = st.text_input("Task Title", key="new_task_title")
    new_task_time = st.number_input(
        "Time (mins)",
        min_value=1,
        max_value=120,
        value=5,
        step=5,
        key="new_task_time"
    )
    input_cols = st.columns([1, 1])
    with input_cols[0]:
        if st.button("Add", key="add_task_button"):
            if new_task_title:
                add_task(new_task_title, new_task_time)
    with input_cols[1]:
        if st.button("Cancel", key="cancel_task_button"):
            st.session_state.show_task_input = False
            st.rerun()

# --- Available Time Prompt directly below "Let's Go" ---
if st.session_state.go_time_prompt:
    time_value = st.slider(
        "Available Time (mins)",
        min_value=5,
        max_value=120,  # max is 2 hours (120 minutes)
        value=30,
        step=5,
        key="time_slider"
    )
    prompt_cols = st.columns([1, 1])
    with prompt_cols[0]:
        if st.button("Generate Optimized List", key="generate_optimized"):
            st.session_state.optimized_tasks = generate_optimized_tasks(time_value)
            st.session_state.go_time_prompt = False
            st.rerun()
    with prompt_cols[1]:
        if st.button("Cancel", key="cancel_time_button"):
            st.session_state.go_time_prompt = False
            st.rerun()

st.markdown("---")

# --- To Do (Master Task List) ---
st.markdown("## To Do")
for task in st.session_state.tasks:
    # Adjust column ratios for minimal spacing between the action buttons
    col1, col2, col3, col4 = st.columns([4, 0.1, 0.1, 0.1])
    with col1:
        task_color = "#FFA500" if not task["completed"] else "#32CD32"
        st.markdown(
            f"<span style='color:{task_color}; font-size:20px;'>{task['title']}</span> "
            f"<small style='color:#666;'>({task['estimated_time']} mins)</small>",
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
            delete_task(task["id"])
st.markdown("---")
