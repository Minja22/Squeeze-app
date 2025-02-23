import streamlit as st
import uuid

###############################################################################
# CUSTOM CSS
###############################################################################
st.markdown(
    """
    <style>
    /* Force the container around each button to be inline-block */
    .inline-button-container {
        display: inline-block;
        margin-right: 0.5rem; /* Adjust spacing between buttons */
    }
    /* Shrink the default button padding/margin */
    .inline-button-container button {
        padding: 0.3rem 0.6rem;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

###############################################################################
# APP SETUP
###############################################################################
st.set_page_config(page_title="Squeeze - Smart To-Do List", layout="centered")

# Big centered header for the app
st.markdown("<h1 style='text-align: center;'>SQUEEZE</h1>", unsafe_allow_html=True)

# Initialize session state if needed
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "optimized_tasks" not in st.session_state:
    st.session_state.optimized_tasks = []
if "go_time_prompt" not in st.session_state:
    st.session_state.go_time_prompt = False
if "show_task_input" not in st.session_state:
    st.session_state.show_task_input = False

###############################################################################
# HELPER FUNCTIONS
###############################################################################
def add_task(title, estimated_time):
    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "estimated_time": estimated_time,
        "completed": False,
        "starred": False,
    }
    st.session_state.tasks.append(task)
    st.session_state.show_task_input = False
    st.rerun()

def toggle_complete(task_id):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["completed"] = not t["completed"]
    st.rerun()

def toggle_star(task_id):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["starred"] = not t["starred"]
    st.rerun()

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    st.rerun()

def generate_optimized_tasks(time_available):
    pending = [t for t in st.session_state.tasks if not t["completed"]]
    starred = [t for t in pending if t["starred"]]
    non_starred = [t for t in pending if not t["starred"]]

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

###############################################################################
# TOP: OPTIMIZED TASK LIST
###############################################################################
if st.session_state.optimized_tasks and all(t["completed"] for t in st.session_state.optimized_tasks):
    st.session_state.optimized_tasks = []

if st.session_state.optimized_tasks:
    st.markdown("## Optimized Task List")
    if st.button("Out of Time", key="out_of_time"):
        st.session_state.optimized_tasks = []
        st.rerun()

    for task in st.session_state.optimized_tasks:
        with st.container():
            # Title
            color = "#FFA500" if not task["completed"] else "#32CD32"
            st.markdown(
                f"<span style='color:{color}; font-size:20px;'>{task['title']}</span> "
                f"<small style='color:#666;'>({task['estimated_time']} mins)</small>",
                unsafe_allow_html=True,
            )
            # Buttons (inline)
            # We'll only show the "Complete" button in the optimized list
            c_button_container = st.container()
            with c_button_container:
                # Place the button in an inline-block container
                with st.markdown("<div class='inline-button-container'>", unsafe_allow_html=True):
                    if st.button("✔", key=f"opt_complete_{task['id']}"):
                        toggle_complete(task["id"])
                # Close the container
                st.markdown("</div>", unsafe_allow_html=True)

    total_time = sum(t["estimated_time"] for t in st.session_state.optimized_tasks)
    st.markdown(f"**Total Scheduled Time:** {total_time} minutes")

st.markdown("---")

###############################################################################
# BUTTONS: NEW TASK & LET'S GO
###############################################################################
btn_cols = st.columns(2)
with btn_cols[0]:
    if st.button("➕", key="show_task_input_button"):
        st.session_state.show_task_input = not st.session_state.show_task_input
        st.rerun()

with btn_cols[1]:
    if st.button("Let's Go", key="lets_go_button"):
        st.session_state.go_time_prompt = not st.session_state.go_time_prompt
        st.rerun()

###############################################################################
# NEW TASK INPUT
###############################################################################
if st.session_state.show_task_input:
    new_title = st.text_input("Task Title", key="new_task_title")
    new_time = st.number_input(
        "Time (mins)",
        min_value=1,
        max_value=120,
        value=5,
        step=5,
        key="new_task_time"
    )
    add_cols = st.columns([1, 1])
    with add_cols[0]:
        if st.button("Add", key="add_task_button"):
            if new_title:
                add_task(new_title, new_time)
    with add_cols[1]:
        if st.button("Cancel", key="cancel_task_button"):
            st.session_state.show_task_input = False
            st.rerun()

###############################################################################
# TIME PROMPT
###############################################################################
if st.session_state.go_time_prompt:
    time_val = st.slider(
        "Available Time (mins)",
        min_value=5,
        max_value=120,
        value=30,
        step=5,
        key="time_slider"
    )
    time_cols = st.columns([1, 1])
    with time_cols[0]:
        if st.button("Generate Optimized List", key="generate_optimized"):
            st.session_state.optimized_tasks = generate_optimized_tasks(time_val)
            st.session_state.go_time_prompt = False
            st.rerun()
    with time_cols[1]:
        if st.button("Cancel", key="cancel_time_button"):
            st.session_state.go_time_prompt = False
            st.rerun()

st.markdown("---")

###############################################################################
# MASTER TASK LIST ("TO DO")
###############################################################################
st.markdown("## To Do")
for task in st.session_state.tasks:
    with st.container():
        # Show title/time
        color = "#FFA500" if not task["completed"] else "#32CD32"
        st.markdown(
            f"<span style='color:{color}; font-size:20px;'>{task['title']}</span> "
            f"<small style='color:#666;'>({task['estimated_time']} mins)</small>",
            unsafe_allow_html=True,
        )

        # Now place the buttons inline
        button_container = st.container()
        with button_container:
            # COMPLETE
            with st.markdown("<div class='inline-button-container'>", unsafe_allow_html=True):
                if st.button("✔", key=f"complete_{task['id']}"):
                    toggle_complete(task["id"])
            st.markdown("</div>", unsafe_allow_html=True)

            # STAR
            with st.markdown("<div class='inline-button-container'>", unsafe_allow_html=True):
                if st.button("⭐" if task["starred"] else "☆", key=f"star_{task['id']}"):
                    toggle_star(task["id"])
            st.markdown("</div>", unsafe_allow_html=True)

            # DELETE
            with st.markdown("<div class='inline-button-container'>", unsafe_allow_html=True):
                if st.button("🗑", key=f"delete_{task['id']}"):
                    delete_task(task["id"])
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
