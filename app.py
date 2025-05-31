import streamlit as st
import shutil
import os
from datetime import datetime
import time

# Set page config for a better look
st.set_page_config(page_title="File Backup Pro", page_icon="📂", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; padding: 20px; border-radius: 10px; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px 20px; }
    .stButton>button:hover { background-color: #45a049; }
    .stTextInput>div>div>input { border-radius: 5px; padding: 8px; }
    .status-box { padding: 15px; border-radius: 8px; margin-top: 10px; }
    .success { background-color: #d4edda; color: #155724; }
    .error { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("📂 File Backup Pro")
st.markdown("Automate your file backups with ease! Select directories, filter files, and track progress.")

# Layout with columns for better organization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source")
    source_dir = st.text_input("Source Directory", "C:/Users/YourName/Documents", help="Folder containing files to back up")
    file_filter = st.text_input("File Filter (e.g., *.txt)", "*", help="Use * for all files or *.ext for specific types (e.g., *.pdf)")

with col2:
    st.subheader("Destination")
    dest_dir = st.text_input("Destination Directory", "C:/Users/YourName/Backup", help="Folder where backups will be saved")

# Advanced options in an expander
with st.expander("Advanced Options"):
    overwrite = st.checkbox("Overwrite existing files", value=False, help="If checked, overwrites files in backup if they exist")
    include_subdirs = st.checkbox("Include subdirectories", value=False, help="If checked, backs up files in subfolders too")

# Button to trigger backup
if st.button("Start Backup"):
    try:
        # Create backup folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(dest_dir, f"backup_{timestamp}")
        os.makedirs(backup_path, exist_ok=True)

        # Get list of files to copy
        copied_files = []
        total_files = 0
        copied_count = 0

        # Count total files for progress
        if include_subdirs:
            for root, _, files in os.walk(source_dir):
                for filename in files:
                    if file_filter == "*" or filename.endswith(file_filter[1:]):
                        total_files += 1
        else:
            for filename in os.listdir(source_dir):
                if file_filter == "*" or filename.endswith(file_filter[1:]):
                    total_files += 1

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Copy files
        if include_subdirs:
            for root, _, files in os.walk(source_dir):
                for filename in files:
                    if file_filter == "*" or filename.endswith(file_filter[1:]):
                        source_file = os.path.join(root, filename)
                        rel_path = os.path.relpath(source_file, source_dir)
                        dest_file = os.path.join(backup_path, rel_path)
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        if os.path.isfile(source_file):
                            if not os.path.exists(dest_file) or overwrite:
                                shutil.copy2(source_file, dest_file)
                                copied_files.append(filename)
                                copied_count += 1
                                progress_bar.progress(min(copied_count / total_files, 1.0))
                                status_text.text(f"Copying: {filename} ({copied_count}/{total_files})")
        else:
            for filename in os.listdir(source_dir):
                if file_filter == "*" or filename.endswith(file_filter[1:]):
                    source_file = os.path.join(source_dir, filename)
                    dest_file = os.path.join(backup_path, filename)
                    if os.path.isfile(source_file):
                        if not os.path.exists(dest_file) or overwrite:
                            shutil.copy2(source_file, dest_file)
                            copied_files.append(filename)
                            copied_count += 1
                            progress_bar.progress(min(copied_count / total_files, 1.0))
                            status_text.text(f"Copying: {filename} ({copied_count}/{total_files})")

        # Display success
        st.markdown(f"<div class='status-box success'>Backup complete! Saved to: {backup_path}</div>", unsafe_allow_html=True)
        st.subheader("Copied Files")
        for file in copied_files:
            st.write(f"✓ {file}")
        st.balloons()

    except Exception as e:
        # Display error
        st.markdown(f"<div class='status-box error'>An error occurred: {str(e)}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("**Note:** Ensure directories exist and you have permissions. Use '*' for all files or '*.ext' for specific types.")
