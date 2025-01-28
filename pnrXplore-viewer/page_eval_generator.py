
from pathlib import PosixPath, Path
from streamlit_elements import elements, dashboard
from typing import Dict, List
import streamlit as st
import json
from page_eval_items import PageEvalItems, media
from page_helper import PageHelper

class PageEvalGenerator:

    @staticmethod
    def __load_page_data(data_key: str, path: PosixPath):
        with open(path) as f:
            st.session_state.data_key = json.load(f)

    @staticmethod
    def __generate_controls(elements: List, page_root: PosixPath, page_generate_key:str):
        cols = st.columns(len(elements))
        for i, ele in enumerate(elements):
            with cols[i]:
                if ele["type"] == "PnrXploreControlSliderSelect":
                    PageEvalItems.PnrXploreControlSliderSelect(ele)
                if ele["type"] == "PnrXploreControlBoxSelect":
                    PageEvalItems.PnrXploreControlBoxSelect(ele)
            # TODO: Add further control components here
        
    def __generate_dashboard(items: List, page_root: PosixPath, page_generate_key:str):
        layout = [dashboard.Item(i=i["key"], **i["layout"]) for i in items]
        with elements(f"dashboard_{page_generate_key}"):
            with dashboard.Grid(layout):
                for i in items:
                    if i["item_type"] == "PnrXploreDashLine":
                       PageEvalItems.PnrXploreDashLine(i)
                    if i["item_type"] == "PnrXploreDashStateImage":
                       PageEvalItems.PnrXploreDashStateImage(i, page_root)
                    if i["item_type"] == "PnrXploreDashVideo":
                       PageEvalItems.PnrXploreDashVideo(i, page_root)

    @staticmethod
    def __generate_video_select(items: List, page_root: PosixPath, page_generate_key:str):
        k = "{}_video_select".format(page_root.name)
        st.selectbox(
            label="Select Video",
            options=list(items[0].keys()),
            key=k
        )
        #with mui.Paper(key=item["key"]):
        video_data = PageHelper.image_path_to_base64(page_root/items[0][st.session_state[k]])
        with elements("{}_player".format(page_root.name)):
            media.Player(
                url="data:video/mpeg;base64," + video_data,
                controls=True,
                width="100%",
                height="10%"
            )

    @staticmethod
    def generate():
        page_generate_key = st.session_state.page_generate_key
        page_root = Path(st.session_state.manger_uploaded_root)/page_generate_key
        data_key = f"{page_generate_key}_data"
        if not page_generate_key in st.session_state:
            st.session_state.page_generate_key = True
            PageEvalGenerator.__load_page_data(data_key, page_root/"data.json")

        data = st.session_state.data_key

        st.markdown("""<style> .block-container {
                        padding-top:    0.8rem;
                        padding-bottom: 0rem;
                        padding-left:   5rem;
                        padding-right:  5rem;
                    } </style>""", unsafe_allow_html=True)
        st.title(data["title"])

        elements_dict = data["elements"]
        if "controls" in elements_dict:
            PageEvalGenerator.__generate_controls(elements_dict["controls"], page_root, page_generate_key)
        if "dashboard" in elements_dict:
            PageEvalGenerator.__generate_dashboard(elements_dict["dashboard"], page_root, page_generate_key)
        if "video_select" in elements_dict:
            PageEvalGenerator.__generate_video_select(elements_dict["video_select"], page_root, page_generate_key)