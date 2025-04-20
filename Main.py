import streamlit as st
import pandas as pd

# --- Initialize session state ---
if "parents" not in st.session_state:
    st.session_state.parents = []
if "tree_data" not in st.session_state:
    st.session_state.tree_data = {}

st.title("Dynamic Tree Pane for File Grouping")

# --- File Upload Section ---
uploaded_files = st.file_uploader("Upload files", type=['csv', 'txt'], accept_multiple_files=True)
filenames = [file.name for file in uploaded_files] if uploaded_files else []

if filenames:
    st.write("### Uploaded Files")
    st.dataframe(pd.DataFrame(filenames, columns=["Filename"]))

# --- Add/Delete Parent Section ---
st.write("### Manage Batches")

col1, col2 = st.columns([2, 1])
with col1:
    new_parent = st.text_input("New Parent Name")
with col2:
    if st.button("Add Parent"):
        if new_parent and new_parent not in st.session_state.parents:
            st.session_state.parents.append(new_parent)
            st.session_state.tree_data[new_parent] = []

if st.session_state.parents:
    parent_to_remove = st.selectbox("Select parent to delete", st.session_state.parents)
    if st.button("Delete Parent"):
        st.session_state.parents.remove(parent_to_remove)
        st.session_state.tree_data.pop(parent_to_remove, None)

# --- Assign Files to Each Parent ---
if st.session_state.parents:
    st.write("### Assign Files to Parents")
    for parent in st.session_state.parents:
        selected_files = st.multiselect(f"Select files for {parent}", filenames, 
                                        default=st.session_state.tree_data.get(parent, []),
                                        key=f"select_{parent}")
        st.session_state.tree_data[parent] = selected_files

# --- Display Tree Pane ---
if st.session_state.tree_data:
    st.write("### Tree Pane")
    for parent, children in st.session_state.tree_data.items():
        with st.expander(parent):
            if children:
                for child in children:
                    st.write(f"• {child}")
            else:
                st.write("*No files assigned*")
