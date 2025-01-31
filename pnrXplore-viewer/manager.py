import json
from typing import List
import shutil
import tempfile
import streamlit as st


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
                    page="page_hello_data.py",
                    title="Hello",
                    icon="📊",
                    url_path="pg_hello_data",
                ),
                st.Page(
                    page="page_reset.py", title="Reset", icon="⏏️", url_path="pg_reset"
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
            pages.append(st.Page("page_interactive.py", title="Interactive", icon="💻"))
        else:
            pages = [st.Page("page_upload.py")]
            # pages = [st.Page("page_nodes.py")]
        st.session_state.pages_generated = pages

    def reset(self):
        if (
            p := st.session_state.get("manger_uploaded_root", None)
        ) is not None and p in tempfile.gettempdir():
            shutil.rmtree(p)
        st.session_state["manger_uploaded_root"] = None
        # For debugging
        if st.session_state.get("debug", False):
            st.session_state.manger_uploaded_root = Path("archives/run/").absolute()
            self.__load_page_keys()
        st.rerun()

    def run(self):
        pg = None
        # if st.session_state.get("manger_pages_dict", None) is None:
        self.generate()
        pg = st.navigation(st.session_state.pages_generated)
        if pg.url_path == "pg_reset":
            self.reset()
        st.session_state.page_generate_key = pg.url_path
        pg.run()
