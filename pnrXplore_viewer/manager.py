import json
from typing import List
import shutil
import tempfile
import streamlit as st
from pathlib import Path
from factory import Factory


class Manager:
    def __init__(self) -> None:
        # self.reset()
        st.set_page_config(
            page_title="pnrXplore", layout="wide", initial_sidebar_state="collapsed"
        )

    @staticmethod
    def __load_index():
        if (p := st.session_state.get("manger_uploaded_root", None)) is not None:
            with open(Path(p) / "index.json") as f:
                st.session_state.manger_pages_dict = json.load(f)

    def generate(self) -> List:
        self.__load_index()
        if st.session_state.get("manger_uploaded_root", None) is not None:
            pages = [
                st.Page(
                    page="static/page_hello_data.py",
                    title="Hello",
                    icon="📊",
                    url_path="pg_hello_data",
                ),
                st.Page(
                    page="static/page_reset.py",
                    title="Reset",
                    icon="⏏️",
                    url_path="pg_reset",
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
        else:
            pages = [st.Page("static/page_upload.py")]
            # pages = [st.Page("static/page_debug.py")]
        st.session_state.pages_generated = pages

    def reset(self):
        if (
            p := st.session_state.get("manger_uploaded_root", None)
        ) is not None and p in tempfile.gettempdir():
            shutil.rmtree(p)

        # TODO: is there a better way to handle these states?
        del st.session_state["sel_quick_from_existing_folder_init"]
        del st.session_state["manger_uploaded_root"]
        st.rerun()

    def run(self):
        pg = None
        self.generate()
        pg = st.navigation(st.session_state.pages_generated)
        if pg.url_path == "pg_reset":
            self.reset()
        st.session_state.page_generate_key = pg.url_path
        pg.run()
