import streamlit as st
from typing import List
from pathlib import PosixPath
from pnrXplore_viewer.utils.helper import Helper
import json
from pathlib import Path
from io import StringIO


class Templates:
    @classmethod
    def PnrXploreCinema(cls, data, page_root: PosixPath, page_generate_key: str):
        from streamlit_elements import elements, media

        k = "{}_video_select".format(page_root.name)
        st.selectbox(label="Select Video", options=list(data[0].keys()), key=k)
        # with mui.Paper(key=item["key"]):
        video_data = Helper.image_path_to_base64(
            page_root / data[0][st.session_state[k]]
        )
        with elements("{}_player".format(page_root.name)):
            media.Player(
                url="data:video/mpeg;base64," + video_data,
                controls=True,
                width="100%",
                height="10%",
            )

    @classmethod
    def PnrXploreNotes(cls, data, page_root: PosixPath, page_generate_key: str):
        from streamlit_ace import st_ace

        def __load_markdown(data):
            with open(page_root / data[0]["file"], "r") as f:
                return f.read()

        def __store_markdown(data, text: str):
            with open(page_root / data[0]["file"], "w") as f:
                f.write(text)

        is_editing = page_generate_key + "_editing"
        if not is_editing in st.session_state:
            st.session_state[is_editing] = False

        if st.session_state[is_editing] == False:
            if st.button("Edit"):
                st.session_state[is_editing] = True
                st.rerun()
            st.markdown(__load_markdown(data))
        else:
            content = st_ace(
                value=__load_markdown(data),
                language="markdown",
                theme="clouds_midnight",
                keybinding="vscode",
                font_size=18,
                tab_size=2,
                show_gutter=True,
                wrap=True,
                auto_update=False,
                readonly=False,
                min_lines=25,
                key="ace",
            )

            if content != __load_markdown(data):
                __store_markdown(data, content)
                st.session_state[is_editing] = False
                st.rerun()

    @classmethod
    def PnrXplorePlayground(cls, data, page_root: PosixPath, page_generate_key: str):
        from streamlit_ace import st_ace
        from contextlib import redirect_stdout
        import matplotlib.pyplot as plt
        import numpy as np

        def __load_python(data):
            with open(page_root / data[0]["file"], "r") as f:
                return f.read()

        def __store_python(data, code: str):
            with open(page_root / data[0]["file"], "w") as f:
                f.write(code)

        def get_pages():
            return st.session_state.get("manger_pages_dict", [])

        def get_page_data(page: str):
            if (p := st.session_state.get("manger_uploaded_root", None)) is not None:
                with open(Path(p) / page / "data.json") as f:
                    return json.load(f)

        st.markdown(
            """<style> .block-container {
                        padding-top:    0.8rem;
                        padding-bottom: 0rem;
                        padding-left:   5rem;
                        padding-right:  5rem;
                    } </style>""",
            unsafe_allow_html=True,
        )
        st.title("Interactive Data Explorer")

        cedit, cplot = st.columns(2)

        with cedit:
            content = st_ace(
                value=__load_python(data),
                language="python",
                theme="clouds_midnight",
                keybinding="vscode",
                font_size=18,
                tab_size=2,
                show_gutter=True,
                wrap=True,
                auto_update=False,
                readonly=False,
                min_lines=25,
                key="ace",
            )

        with cplot:
            if content:
                __store_python(data, content)
                # Note: If the environment is not trusted this is highly insecure!
                # use epicbox or similar
                default_prexif = "plt.style.use('dark_background')\n"
                f = StringIO()
                with redirect_stdout(f):
                    exec(default_prexif + content)
                st.markdown("```\n {} \n```".format(f.getvalue()))

    @classmethod
    def PnrXploreOverview(cls, data, page_root: PosixPath, page_generate_key: str):
        import pandas as pd

        st.markdown(
            """<style> .block-container {
                        padding-top:    0.8rem;
                        padding-bottom: 0rem;
                        padding-left:   5rem;
                        padding-right:  5rem;
                    } </style>""",
            unsafe_allow_html=True,
        )

        for s in data[0]["sections"]:
            df = pd.DataFrame(s["data"])
            st.markdown("## {}".format(s["title"]))

            cc = {}
            for k, v in s["column_config"].items():
                if type(v) == str:
                    cc[k] = v
                else:
                    cc[k] = getattr(st.column_config, v[0])(v[1])

            st.dataframe(df, hide_index=True, column_config=cc)
