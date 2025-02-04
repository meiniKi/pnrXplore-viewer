from typing import Dict
import streamlit as st
from pathlib import PosixPath
from streamlit_elements import elements, mui, nivo, html
from pydoc import locate
from pnrXplore_viewer.utils.helper import Helper


class Items:
    @staticmethod
    def PnrXploreDashLine(item: Dict, page_root: PosixPath):
        # Get values for markers
        if "markers" in item["item_content"]:
            for m in item["item_content"]["markers"]:
                m["value"] = st.session_state.get(m["value"], 0)

        with elements(item["key"]):
            with mui.Box(key=item["key"]):
                nivo.Line(**item["item_content"])

    @staticmethod
    def PnrXploreDashStateImage(item: Dict, page_root: PosixPath):
        vals = tuple(
            [
                locate(i[0])(st.session_state.get(i[1], 0))
                for i in item["item_content"]["format_keys"]
            ]
        )
        with mui.Paper(key=item["key"]):
            with mui.Typography:
                html.img(
                    src="data:image/png;base64,{}".format(
                        Helper.image_path_to_base64(
                            page_root
                            / (item["item_content"]["relpath_template"] % vals)
                        )
                    ),
                    style={"width": "100%", "height": "auto", "display": "block"},
                )
