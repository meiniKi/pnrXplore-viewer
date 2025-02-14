import os
import io
import zipfile
import tarfile
import base64
import streamlit as st


class Download:
    @staticmethod
    def create_archive():
        buffer = io.BytesIO()
        file_format = st.session_state["sel_download_format"]
        folder_path = st.session_state["manger_uploaded_root"]
        if file_format == ".zip":
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        fullpath = os.path.join(root, file)
                        arcname = os.path.relpath(fullpath, start=folder_path)
                        zf.write(fullpath, arcname)
        elif file_format == ".tar":
            with tarfile.open(fileobj=buffer, mode="w") as tf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        fullpath = os.path.join(root, file)
                        arcname = os.path.relpath(fullpath, start=folder_path)
                        tf.add(fullpath, arcname)
        else:
            raise ValueError("Unsupported archive format. Use '.zip' or '.tar'.")

        buffer.seek(0)
        return buffer
