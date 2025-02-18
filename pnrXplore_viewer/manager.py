import json
from typing import List
import shutil
import tempfile
import streamlit as st
from pathlib import Path
from factory import Factory
from download import Download
from config import Config


class Manager:
    """Manages the shown pages. Initially, the page to select or upload a bundle is shown.
    Once a bundle is provided, all generated pages are displayed. Also, it handles
    resetting a bundle and downloading it via the browser."""

    def __init__(self) -> None:
        st.set_page_config(
            page_title="pnrXplore", layout="wide", initial_sidebar_state="collapsed"
        )

    @staticmethod
    def __load_index():
        """Load bundle index json into st.manger_pages_dict."""
        if (p := st.session_state.get("manger_uploaded_root", None)) is not None:
            with open(Path(p) / Config.PAGE_INDEX_FILE) as f:
                st.session_state.manger_pages_dict = json.load(f)

    def generate(self) -> List:
        """Generate all pages to be shown. Either the welcome page for uploads or
        pages according to allocations in the bundle."""
        self.__load_index()
        if st.session_state.get("manger_uploaded_root", None) is not None:
            pages = [
                st.Page(
                    page="static/page_hello_data.py",
                    title="Hello",
                    icon="👋",
                    url_path="pg_hello_data",
                ),
            ]
            for p in st.session_state.get("manger_pages_dict", []):
                pages.append(
                    st.Page(
                        page=Factory.generate,
                        title=p["title"],
                        url_path=p["key"],
                        default=False,
                    )
                )
            with st.sidebar:
                if st.button("⏏️ Reset", use_container_width=True):
                    self.reset()
                if st.button("💾 Download", use_container_width=True):
                    self.download()
        else:
            pages = [st.Page("static/page_upload.py")]
        st.session_state.pages_generated = pages

    @st.dialog("file", width="large")
    def download(self):
        st.selectbox(
            label="Select Format", key="sel_download_format", options=[".tar", ".zip"]
        )
        # Until this issue is resolve, there is a 2-way step to create the archive
        # and then download it
        # https://github.com/streamlit/streamlit/issues/5053
        st.markdown("Note: 2-step process until streamlit/issues/5053 is resolved")
        path = None
        if st.button("1) Click me to create the archive"):
            with st.spinner(""):
                buffer = Download.create_archive()
                path = Config.BUNDLES_DIR / (
                    Config.FILENAME_BASE_DOWNLAOD
                    + st.session_state["sel_download_format"]
                )
                with open(path, "wb") as f:
                    f.write(buffer.getbuffer())
        if path:
            with open(path, "rb") as f:
                st.download_button(
                    label="2) Now, click me to download",
                    data=f,
                    file_name=st.session_state["manger_uploaded_name"]
                    + st.session_state["sel_download_format"],
                    mime="application/zip",
                )

    def reset(self):
        """Reset to the welcome page; includes removing temporarily creates files."""
        if (
            p := st.session_state.get("manger_uploaded_root", None)
        ) is not None and p in tempfile.gettempdir():
            shutil.rmtree(p)

        # TODO: is there a better way to handle these states?
        del st.session_state["sel_quick_from_existing_folder_init"]
        del st.session_state["manger_uploaded_root"]
        st.rerun()

    def run(self):
        """Main function to run the manager."""
        pg = None
        self.generate()
        pg = st.navigation(st.session_state.pages_generated)
        # page_generate_key stores the currently displayed page
        # Thus, only this page needs to be rendered
        st.session_state.page_generate_key = pg.url_path
        pg.run()
