import streamlit as st

# Initialize session state for tasks, generated list, and theme settings
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "generated_tasks" not in st.session_state:
    st.session_state["generated_tasks"] = []
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "main"  # Tracks whether we're on main list or "Go Time" page

# Function to add a new task
def add_task(task_name, duration):
    if task_name and duration:
        st.session_state["tasks"].append({"task": task_name, "duration": duration, "completed": False})

# Function to toggle dark mode
def toggle_theme():
    st.session_state["dark_mode"] = not st.session_state["dark_mode"]

# Function to mark task as completed
def complete_task(index, from_generated=False):
    st.session_state["tasks"][index]["completed"] = True
    if from_generated:
        for gen_task in st.session_state["generated_tasks"]:
            if gen_task["task"] == st.session_state["tasks"][index]["task"]:
                gen_task["completed"] = True

# Function to undo a completed task
def undo_task(index, from_generated=False):
    st.session_state["tasks"][index]["completed"] = False
    if from_generated:
        for gen_task in st.session_state["generated_tasks"]:
            if gen_task["task"] == st.session_state["tasks"][index]["task"]:
                gen_task["completed"] = False

# Function to generate tasks for "Go Time" page
def generate_task_list(available_time):
    st.session_state["generated_tasks"] = []
    total_time = 0
    # Iterate over tasks sorted by duration but get the master list index
    for task in sorted(st.session_state["tasks"], key=lambda x: x["duration"]):
        master_index = st.session_state["tasks"].index(task)
        if total_time + task["duration"] <= available_time and not task["completed"]:
            st.session_state["generated_tasks"].append({**task, "index": master_index})
            total_time += task["duration"]
    st.session_state["page"] = "go_time"  # Switch to Go Time page

# Apply dark mode styling
if st.session_state["dark_mode"]:
    st.markdown(
        """
        <style>
            body { background-color: #121212; color: white; }
            .stButton button { background-color: #333; color: white; }
            .stTextInput input { background-color: #333; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

# MAIN PAGE (Ongoing Task List)
if st.session_state["page"] == "main":
    st.title("Squeeze: Time-Based Task Manager")

    # Theme Toggle
    if st.button("Toggle Dark Mode 🌙/☀️"):
        toggle_theme()

    # Task Input Section
    st.subheader("Your Ongoing Task List")
    task_name = st.text_input("Enter a task:")
    task_duration = st.selectbox("Estimated Duration (minutes)", list(range(5, 125, 5)))  # 5-min increments

    if st.button("Add Task ➕"):
        add_task(task_name, task_duration)

    # Display Task List
    if st.session_state["tasks"]:
        for index, task in enumerate(st.session_state["tasks"]):
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(f"**{task['task']}**")
                st.write(f"*{task['duration']} min*")

            with col2:
                if not task["completed"]:
                    if st.button(f"✅ Done {index}"):
                        complete_task(index)
                        st.success("Task Completed!")

            with col3:
                if task["completed"]:
                    if st.button(f"↩️ Undo {index}"):
                        undo_task(index)
                    st.markdown("🎉 *Completed!*")

    # "Go Time" Section
    st.subheader("Go Time!")
    available_time = st.slider("How much time do you have?", 5, 120, 30, 5)

    if st.button("Generate Focused Task List 🚀"):
        generate_task_list(available_time)

# GO TIME PAGE (Generated Task List)
elif st.session_state["page"] == "go_time":
    st.title("Focused Task List 🚀")

    if st.button("⬅️ Back to Main List"):
        st.session_state["page"] = "main"

    if st.session_state["generated_tasks"]:
        st.subheader("Here’s your focused list:")
        for task in st.session_state["generated_tasks"]:
            col1, col2 = st.columns([8, 2])
            with col1:
                st.write(f"✅ **{task['task']}** ({task['duration']} min)")

            with col2:
                if not task["completed"]:
                    if st.button(f"✅ Done {task['index']} (Go Time)"):
                        complete_task(task["index"], from_generated=True)
                        st.success("Task Completed!")
                else:
                    if st.button(f"↩️ Undo {task['index']} (Go Time)"):
                        undo_task(task["index"], from_generated=True)
                    st.markdown("🎉 *Completed!*")

    # Check if all tasks in the generated list are completed, trigger celebration
    if st.session_state["generated_tasks"] and all(task["completed"] for task in st.session_state["generated_tasks"]):
        st.balloons()
        st.success("You completed all tasks in this session!")

st.write("🎯 Complete your tasks and press 'Go Time' when ready!")
