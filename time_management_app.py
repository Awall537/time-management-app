import streamlit as st
import pandas as pd
import uuid

# Assign a unique session ID to each user when they open the app
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize DataFrames for this session's master list and holding spot
if "master_list" not in st.session_state:
    st.session_state.master_list = pd.DataFrame(columns=["Task", "Category", "Due Date", "Status", "Priority"])

if "holding_spot" not in st.session_state:
    st.session_state.holding_spot = pd.DataFrame(columns=["Idea", "Captured On"])

categories = ["Health", "Leisure", "Daily Living Tasks", "Personal", "Professional", "Miscellaneous"]

st.title(f"📝 Time Management Tool - Session ID: {st.session_state.session_id}")

# Add Task to Master List
with st.form("Add Task"):
    st.subheader("Add a New Task")
    task = st.text_input("Task")
    category = st.selectbox("Category", categories)
    due_date = st.date_input("Due Date")
    status = st.selectbox("Status", ["Pending", "Completed"])
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submit_task = st.form_submit_button("Add Task")

    if submit_task:
        new_task = pd.DataFrame({
            "Task": [task],
            "Category": [category],
            "Due Date": [due_date],
            "Status": [status],
            "Priority": [priority]
        })
        st.session_state.master_list = pd.concat([st.session_state.master_list, new_task], ignore_index=True)
        st.success("Task added successfully!")

# Capture Quick Idea
with st.form("Capture Idea"):
    st.subheader("Capture a Quick Idea")
    idea = st.text_input("Quick Idea")
    submit_idea = st.form_submit_button("Capture Idea")

    if submit_idea:
        new_idea = pd.DataFrame({"Idea": [idea], "Captured On": [pd.Timestamp.now()]})
        st.session_state.holding_spot = pd.concat([st.session_state.holding_spot, new_idea], ignore_index=True)
        st.success("Idea captured successfully!")

# View Master List
if st.button("View Master List"):
    st.subheader("Master List")
    st.dataframe(st.session_state.master_list)

# View Holding Spot
if st.button("View Holding Spot"):
    st.subheader("Holding Spot")
    st.dataframe(st.session_state.holding_spot)
