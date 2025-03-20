from typing import Dict
import streamlit as st


class Controls:
    @staticmethod
    def PnrXploreControlSliderSelect(item: Dict):
        """Slider to select one of a discrete number of options."""
        st.select_slider(label=item["label"], key=item["key"], options=item["options"])

    @staticmethod
    def PnrXploreControlBoxSelect(item: Dict):
        """Box, e.g., drop-down to select one of a discrete number of options."""
        st.selectbox(label=item["label"], key=item["key"], options=item["options"])
