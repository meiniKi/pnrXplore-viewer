from pathlib import PosixPath, Path
from streamlit_elements import elements, dashboard
from streamlit_ace import st_ace
from typing import Dict, List
import streamlit as st
import json
from ..components.controls import Controls
from ..components.items import Items


class Factory:
    @staticmethod
    def __load_page_data(data_key: str, path: PosixPath):
        with open(path) as f:
            st.session_state.data_key = json.load(f)

    @staticmethod
    def __generate_controls(
        elements: List, page_root: PosixPath, page_generate_key: str
    ):
        cols = st.columns(len(elements))
        for i, ele in enumerate(elements):
            with cols[i]:
                if ele["type"] == "PnrXploreControlSliderSelect":
                    Controls.PnrXploreControlSliderSelect(ele)
                if ele["type"] == "PnrXploreControlBoxSelect":
                    Controls.PnrXploreControlBoxSelect(ele)
            # TODO: Add further control components here

    def __generate_dashboard(items: List, page_root: PosixPath, page_generate_key: str):
        layout = [dashboard.Item(i=i["key"], **i["layout"]) for i in items]
        with elements(f"dashboard_{page_generate_key}"):
            with dashboard.Grid(layout):
                for i in items:
                    if i["item_type"] == "PnrXploreDashLine":
                        Items.PnrXploreDashLine(i)
                    if i["item_type"] == "PnrXploreDashStateImage":
                        Items.PnrXploreDashStateImage(i, page_root)
                    if i["item_type"] == "PnrXploreDashVideo":
                        Items.PnrXploreDashVideo(i, page_root)

    @staticmethod
    def __generate_template(
        template: str, items: List, page_root: PosixPath, page_generate_key: str
    ):
        pass

    @staticmethod
    def generate():
        page_generate_key = st.session_state.page_generate_key
        page_root = Path(st.session_state.manger_uploaded_root) / page_generate_key
        data_key = f"{page_generate_key}_data"
        if not page_generate_key in st.session_state:
            st.session_state.page_generate_key = True
            Factory.__load_page_data(data_key, page_root / "data.json")

        data = st.session_state.data_key

        st.markdown(
            """<style> .block-container {
                        padding-top:    0.8rem;
                        padding-bottom: 0rem;
                        padding-left:   5rem;
                        padding-right:  5rem;
                    } </style>""",
            unsafe_allow_html=True,
        )
        st.title(data["title"])

        components_dict = data["components"]
        if "controls" in components_dict:
            Factory.__generate_controls(
                components_dict["controls"], page_root, page_generate_key
            )
        if "dashboard" in components_dict:
            Factory.__generate_dashboard(
                components_dict["dashboard"], page_root, page_generate_key
            )
        if "template" in components_dict:
            Factory.__generate_template(
                components_dict["template"], page_root, page_generate_key
            )
