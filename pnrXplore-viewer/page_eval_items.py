
from typing import Dict
import streamlit as st
from pathlib import PosixPath
from streamlit_elements import elements, mui, nivo, html, media
from page_helper import PageHelper
from pydoc import locate

class PageEvalItems:
    @staticmethod
    def PnrXploreControlSliderSelect(item: Dict):
        st.select_slider(
            label=item["label"],
            key=item["key"],
            options=item["options"])
        
    def PnrXploreControlBoxSelect(item: Dict):
        st.selectbox(
            label=item["label"],
            key=item["key"],
            options=item["options"])

    @staticmethod
    def PnrXploreDashLine(item: Dict):
        marker_dict = {"markers": [{"axis": "x",
                                    "value": st.session_state.get("pstatic_sel_iter", 0),
                                    "lineStyle": { "stroke": "#aba803", "strokeWidth": 2 },
                                    "legendOrientation": "vertical"}]}

        with elements(item["key"]):
            with mui.Box(key=item["key"]):
                nivo.Line(**item["item_content"]|marker_dict)


    @staticmethod
    def PnrXploreDashStateImage(item: Dict, page_root: PosixPath):
        vals = tuple([locate(i[0])(st.session_state.get(i[1])) for i in item["item_content"]["format_keys"]])
        with mui.Paper(key=item["key"]):
            with mui.Typography:
                html.img(
                    src="data:image/png;base64,{}".format(
                            PageHelper.image_path_to_base64(
                                page_root/(item["item_content"]["relpath_template"] % vals))),
                    style={'width': '100%',
                           'height': 'auto',
                           'display': 'block'}
                        )
