import streamlit as st
import streamlit.components.v1 as components

# Initialize session state variables
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "generated_tasks" not in st.session_state:
    st.session_state["generated_tasks"] = []
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "main"  # "main" or "go_time"
if "show_modal" not in st.session_state:
    st.session_state["show_modal"] = False

# Functions for task operations
def add_task(task_title, duration):
    if task_title and duration:
        st.session_state["tasks"].append({"task": task_title, "duration": duration, "completed": False})

def complete_task(index, from_generated=False):
    st.session_state["tasks"][index]["completed"] = True
    if from_generated:
        for gen_task in st.session_state["generated_tasks"]:
            if gen_task["task"] == st.session_state["tasks"][index]["task"]:
                gen_task["completed"] = True

def undo_task(index, from_generated=False):
    st.session_state["tasks"][index]["completed"] = False
    if from_generated:
        for gen_task in st.session_state["generated_tasks"]:
            if gen_task["task"] == st.session_state["tasks"][index]["task"]:
                gen_task["completed"] = False

def generate_task_list(available_time):
    st.session_state["generated_tasks"] = []
    total_time = 0
    for task in sorted(st.session_state["tasks"], key=lambda x: x["duration"]):
        master_index = st.session_state["tasks"].index(task)
        if total_time + task["duration"] <= available_time and not task["completed"]:
            st.session_state["generated_tasks"].append({**task, "index": master_index})
            total_time += task["duration"]
    st.session_state["page"] = "go_time"

def toggle_theme():
    st.session_state["dark_mode"] = not st.session_state["dark_mode"]

# Optionally apply dark mode styling
if st.session_state["dark_mode"]:
    st.markdown("""
    <style>
    body { background-color: #121212; color: white; }
    .stButton button { background-color: #333; color: white; }
    </style>
    """, unsafe_allow_html=True)

# MAIN PAGE
if st.session_state["page"] == "main":
    st.title("Squeeze: Time-Based Task Manager")
    
    if st.button("Toggle Dark Mode 🌙/☀️"):
        toggle_theme()

    st.subheader("Your Ongoing Task List")
    
    # Display the master task list
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
                    if st.button(f"↩️ Undo {index}", key=f"undo_{index}"):
                        undo_task(index)
                    st.markdown("🎉 *Completed!*")
    
    st.markdown("---")
    st.markdown("### Tap to Add a New Task")
    
    # Custom HTML component for gesture detection
    tap_html = """
    <html>
      <head>
        <script>
          function handleTap() {
             Streamlit.setComponentValue("tapped");
          }
          document.addEventListener('DOMContentLoaded', function() {
             document.getElementById("tapArea").addEventListener("click", handleTap);
          });
        </script>
      </head>
      <body>
        <div id="tapArea" style="width:100%; height:200px; border:2px dashed #ccc; display:flex; align-items:center; justify-content:center;">
           <h2 style="font-weight:300;">Tap Here to Add a New Task</h2>
        </div>
      </body>
    </html>
    """
    tap_result = components.html(tap_html, height=250)
    if tap_result == "tapped":
        st.session_state["show_modal"] = True
    
    # Modal-like input form triggered by tap
    if st.session_state["show_modal"]:
        st.markdown("### Add Task")
        new_task_title = st.text_input("Task Title", key="new_task_title")
        new_task_duration = st.number_input("Duration (minutes, increments of 5)", min_value=5, step=5, key="new_task_duration")
        if st.button("Done"):
            add_task(new_task_title, new_task_duration)
            st.session_state["show_modal"] = False

    st.markdown("---")
    st.subheader("Go Time!")
    available_time = st.slider("How much time do you have?", 5, 120, 30, 5)
    if st.button("Generate Focused Task List 🚀"):
        generate_task_list(available_time)

# GO TIME PAGE
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
                    if st.button(f"✅ Done {task['index']} (Go Time)", key=f"go_done_{task['index']}"):
                        complete_task(task["index"], from_generated=True)
                        st.success("Task Completed!")
                else:
                    if st.button(f"↩️ Undo {task['index']} (Go Time)", key=f"go_undo_{task['index']}"):
                        undo_task(task["index"], from_generated=True)
                    st.markdown("🎉 *Completed!*")
    if st.session_state["generated_tasks"] and all(task["completed"] for task in st.session_state["generated_tasks"]):
        st.balloons()
        st.success("You completed all tasks in this session!")
    
    st.write("🎯 Complete your tasks and press 'Go Time' when ready!")
