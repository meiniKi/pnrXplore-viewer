
import streamlit as st
from pathlib import Path
import zipfile
import shutil
import tempfile
import io

def copy_to_proc_root(zip_file, from_buffer=False):
    if from_buffer:
        zip_buffer = io.BytesIO()
        zip_buffer.write(zip_file.read())
        zip_buffer.seek(0)
    else:
        zip_buffer = zip_file

    if (f := st.session_state.get("manger_uploaded_root", None)) is not None:
        shutil.rmtree(f)
        st.session_state["manger_pages_keys"] = None

    tf = tempfile.mkdtemp()
    st.session_state["manger_uploaded_root"] = tf
    zf = zipfile.ZipFile(zip_buffer) 
    zf.extractall(tf)
    st.rerun()


st.title("Upload or Select pnrXplor Archive")

uploaded_archive = st.file_uploader(
    label="Upload an archvie",
    label_visibility="hidden",
    accept_multiple_files=False
)

st.selectbox(
    label="Or Select from Default Folder",
    key="sel_from_archives_folder",
    options = list({str(file.stem) for file in Path("./archives").rglob('*.zip') if file.is_file()}),
)

if st.button("Analyze"):
    st.session_state["manger_uploaded_root"] = "/home/user/Documents/repos/pnrXplore/archives/run"
    st.rerun()

    #if uploaded_archive is not None:
    #    copy_to_proc_root(uploaded_archive, True)
    #else:
    #    copy_to_proc_root((Path("./archives")/Path(st.session_state.get("sel_from_archives_folder")).with_suffix('.zip')).absolute())

