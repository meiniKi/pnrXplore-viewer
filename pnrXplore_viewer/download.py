import os
import io
import zipfile
import tarfile
import base64
import streamlit as st


class Download:
    """Collection of functionality for downloading a new bundle."""
    @staticmethod
    def create_archive() -> io.BytesIO:
        buffer = io.BytesIO()
        file_format = st.session_state["sel_download_format"]
        folder_path = st.session_state["manger_uploaded_root"]
        if file_format == ".zip":
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        path_full = os.path.join(root, file)
                        bundle_name = os.path.relpath(path_full, start=folder_path)
                        zf.write(path_full, bundle_name)
        elif file_format == ".tar":
            with tarfile.open(fileobj=buffer, mode="w") as tf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        path_full = os.path.join(root, file)
                        bundle_name = os.path.relpath(path_full, start=folder_path)
                        tf.add(path_full, bundle_name)
        else:
            raise ValueError("Unsupported archive format. Use '.zip' or '.tar'.")

        buffer.seek(0)
        return buffer
