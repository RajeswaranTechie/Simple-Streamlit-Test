import streamlit as st
import pandas as pd

# Sample data
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 42, 73]
}
df = pd.DataFrame(data)

# Apply color styling based on value
def color_score(val):
    color = 'green' if val >= 70 else 'red'
    return f'color: {color}'

# Apply style
styled_df = df.style.applymap(color_score, subset=['Score'])

# Display in Streamlit
st.write("### Student Scores")
st.dataframe(styled_df, use_container_width=True)


# Sample data
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 42, 73]
}
df = pd.DataFrame(data)

# Convert Score to colored HTML strings
def format_row(row):
    color = 'green' if row['Score'] >= 70 else 'red'
    return f"<span style='color:{color};'>{row['Score']}</span>"

# Add a new column for display only
df['Colored Score'] = df.apply(format_row, axis=1)

# Editable version (Score column only)
edited_df = st.data_editor(
    df[['Name', 'Score']],  # only editable columns
    num_rows="dynamic",
    use_container_width=True
)

# Update colored column based on edits
edited_df['Colored Score'] = edited_df.apply(format_row, axis=1)

# Show updated styled result
st.markdown("### Colored Result Preview")
st.write(edited_df.to_html(escape=False, index=False), unsafe_allow_html=True)



# --- Initialize session state ---
if "parents" not in st.session_state:
    st.session_state.parents = []
if "tree_data" not in st.session_state:
    st.session_state.tree_data = {}

st.title("Dynamic Tree Pane with File Cleanup")

# --- File Upload Section ---
uploaded_files = st.file_uploader("Upload files", type=['csv', 'txt'], accept_multiple_files=True)
filenames = [file.name for file in uploaded_files] if uploaded_files else []

# --- Cleanup tree_data from removed files ---
if filenames and st.session_state.tree_data:
    current_files_set = set(filenames)
    for parent in st.session_state.tree_data:
        old_files = st.session_state.tree_data[parent]
        st.session_state.tree_data[parent] = [f for f in old_files if f in current_files_set]

# --- Display Uploaded Files ---
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
if st.session_state.parents and filenames:
    st.write("### Assign Files to Parents")
    for parent in st.session_state.parents:
        selected_files = st.multiselect(
            f"Select files for {parent}",
            filenames,
            default=st.session_state.tree_data.get(parent, []),
            key=f"select_{parent}"
        )
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
