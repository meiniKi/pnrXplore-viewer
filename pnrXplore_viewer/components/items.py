from typing import Dict
import streamlit as st
from pathlib import PosixPath
from streamlit_elements import elements, mui, nivo, html
from pydoc import locate
from pnrXplore_viewer.utils.helper import Helper


class Items:
    @staticmethod
    def PnrXploreDashLine(item: Dict, page_root: PosixPath):
        """Line plot dashboard item. Currently restricted to a subset of options available in the viewer."""
        # Get values for markers
        if "markers" in item["item_content"]:
            for m in item["item_content"]["markers"]:
                m["value"] = st.session_state.get(m["value"], 0)

        with elements(item["key"]):
            with mui.Box(key=item["key"]):
                nivo.Line(**item["item_content"])

    @staticmethod
    def PnrXploreDashStateImage(item: Dict, page_root: PosixPath):
        """Dashboard item to display an image of a certain state, e.g., the current placement solution"""

        vals = list()
        for i in item["item_content"]["format_keys"]:
            if isinstance(i[0], list):
                for t in i[0]:
                    t = locate(t)
                    try:
                        v = t(st.session_state.get(i[1], t()))
                        vals.append(v)
                        break
                    except (ValueError, TypeError):
                        continue
            else:
                vals.append(locate(i[0])(st.session_state.get(i[1], 0)))

        assert len(vals) == len(
            item["item_content"]["format_keys"]
        ), "Any type has not been found."
        vals = tuple(vals)

        if isinstance(item["item_content"]["relpath_template"], list):
            for fmt in item["item_content"]["relpath_template"]:
                try:
                    if "%" in fmt:
                        result = fmt % vals
                    else:
                        result = fmt.format(*vals)
                    break
                except (TypeError, ValueError) as e:
                    continue
            else:
                raise TypeError
        else:
            result = item["item_content"]["relpath_template"] % vals

        with mui.Paper(key=item["key"]):
            with mui.Typography:
                html.img(
                    src="data:image/png;base64,{}".format(
                        Helper.image_path_to_base64(page_root / result)
                    ),
                    style={"width": "100%", "height": "auto", "display": "block"},
                )
