from pathlib import PosixPath, Path
from streamlit_elements import elements, dashboard
from streamlit_ace import st_ace
from typing import Dict, List
import streamlit as st
import json
from components.controls import Controls
from components.items import Items
from templates.templates import Templates
from config import Config


class Factory:
    """Page factory to generate pages dynamically based on the
    data provided in the loaded bundle."""

    @staticmethod
    def __load_page_data(page_root: PosixPath):
        with open(page_root / Config.PAGE_DATA_FILE) as f:
            st.session_state.data_key = json.load(f)

    @staticmethod
    def __generate_controls(
        elements: List, page_root: PosixPath, page_generate_key: str
    ):
        cols = st.columns(len(elements))
        for i, ele in enumerate(elements):
            with cols[i]:
                getattr(Controls, ele["type"])(ele)

    def __generate_dashboard(items: List, page_root: PosixPath, page_generate_key: str):
        layout = [dashboard.Item(i=i["key"], **i["layout"]) for i in items]
        with elements(f"dashboard_{page_generate_key}"):
            with dashboard.Grid(layout):
                for i in items:
                    getattr(Items, i["item_type"])(i, page_root)

    @staticmethod
    def __generate_template(
        template: str, data, page_root: PosixPath, page_generate_key: str
    ):
        getattr(Templates, template)(data, page_root, page_generate_key)

    @staticmethod
    def generate():
        """Generate the page content for the page stored in page_generate_key."""
        page_generate_key = st.session_state.page_generate_key
        page_root = Path(st.session_state.manger_uploaded_root) / page_generate_key
        # data_key = f"{page_generate_key}_data"
        if not page_generate_key in st.session_state:
            st.session_state.page_generate_key = True
            Factory.__load_page_data(page_root)

        data = st.session_state.data_key

        st.markdown(
            """<style> .block-container {
                        padding-top:    2.0rem;
                        padding-bottom: 0rem;
                        padding-left:   5rem;
                        padding-right:  5rem;
                    } </style>""",
            unsafe_allow_html=True,
        )
        st.title(data["title"])

        # Differentiate between templated pages and constructed pages
        if data["type"] == "template":
            template, data = data["data"]
            Factory.__generate_template(template, data, page_root, page_generate_key)

        elif data["type"] == "constructed":
            components_dict = data["components"]
            if "control" in components_dict:
                Factory.__generate_controls(
                    components_dict["control"], page_root, page_generate_key
                )
            if "dashboard" in components_dict:
                Factory.__generate_dashboard(
                    components_dict["dashboard"], page_root, page_generate_key
                )
