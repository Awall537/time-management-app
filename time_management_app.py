import streamlit as st
import pandas as pd
import uuid
import datetime

# Assign a unique session ID to each user when they open the app
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize DataFrames for this session's master list and holding spot
if "master_list" not in st.session_state:
    st.session_state.master_list = pd.DataFrame(
        columns=["Task", "Category", "Due Date", "Status", "Priority"]
    )

if "holding_spot" not in st.session_state:
    st.session_state.holding_spot = pd.DataFrame(columns=["Idea", "Captured On"])

# Session Timeout: Clear session after 30 minutes of inactivity
if "last_activity" in st.session_state and \
   (datetime.datetime.now() - st.session_state["last_activity"]).seconds > 1800:
    st.session_state.clear()
    st.warning("Session has expired due to inactivity. Refresh to start a new session.")

st.session_state["last_activity"] = datetime.datetime.now()

# Categories for tasks
categories = ["Health", "Leisure", "Daily Living Tasks", "Personal", "Professional", "Miscellaneous"]

# Privacy Notice
st.markdown("""
### Privacy Notice:
This app stores your tasks only temporarily for the duration of your session.
Once you close the browser or the session times out, your tasks will be lost. 
Please avoid entering personal or sensitive information.
""")

st.title(f"📝 Time Management Tool - Session ID: {st.session_state.session_id}")

# Add Task with Validation and Error Handling
with st.form("Add Task"):
    st.subheader("Add a New Task")
    task = st.text_input("Task", max_chars=100, help="Describe your task (max 100 characters).")
    category = st.selectbox("Category", categories)
    due_date = st.date_input("Due Date")
    status = st.selectbox("Status", ["Pending", "Completed"])
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submit_task = st.form_submit_button("Add Task")

    if submit_task:
        try:
            # Validate input length
            if len(task.strip()) == 0:
                st.warning("Task description cannot be empty.")
            else:
                new_task = pd.DataFrame({
                    "Task": [task],
                    "Category": [category],
                    "Due Date": [due_date],
                    "Status": [status],
                    "Priority": [priority]
                })
                st.session_state.master_list = pd.concat([st.session_state.master_list, new_task], ignore_index=True)
                st.success("Task added successfully!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Capture Quick Idea with Error Handling
with st.form("Capture Idea"):
    st.subheader("Capture a Quick Idea")
    idea = st.text_input("Quick Idea", max_chars=100, help="Add a quick idea or note (max 100 characters).")
    submit_idea = st.form_submit_button("Capture Idea")

    if submit_idea:
        try:
            if len(idea.strip()) == 0:
                st.warning("Idea cannot be empty.")
            else:
                new_idea = pd.DataFrame({"Idea": [idea], "Captured On": [pd.Timestamp.now()]})
                st.session_state.holding_spot = pd.concat([st.session_state.holding_spot, new_idea], ignore_index=True)
                st.success("Idea captured successfully!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Rate Limiting: Prevent spamming by checking submission interval
if "last_submit" in st.session_state:
    time_since_last = (datetime.datetime.now() - st.session_state["last_submit"]).seconds
    if time_since_last < 10:
        st.warning("Please wait a few seconds before adding another entry.")
else:
    st.session_state["last_submit"] = datetime.datetime.now()

# View Master List
if st.button("View Master List"):
    if st.session_state.master_list.empty:
        st.info("Your master list is empty.")
    else:
        st.subheader("Master List")
        st.dataframe(st.session_state.master_list)

# View Holding Spot
if st.button("View Holding Spot"):
    if st.session_state.holding_spot.empty:
        st.info("Your holding spot is empty.")
    else:
        st.subheader("Holding Spot")
        st.dataframe(st.session_state.holding_spot)

