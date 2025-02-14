from typing import Dict
import streamlit as st


class Controls:
    @staticmethod
    def PnrXploreControlSliderSelect(item: Dict):
        st.select_slider(label=item["label"], key=item["key"], options=item["options"])

    @staticmethod
    def PnrXploreControlBoxSelect(item: Dict):
        st.selectbox(label=item["label"], key=item["key"], options=item["options"])
