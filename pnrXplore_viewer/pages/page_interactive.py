
import streamlit as st
from streamlit_ace import st_ace
import json
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
import matplotlib.pyplot as plt
import numpy as np


def get_pages():
    return st.session_state.get("manger_pages_dict", [])

def get_page_data(page: str):
    if (p := st.session_state.get("manger_uploaded_root", None)) is not None:
        with open(Path(p)/page/"data.json") as f:
            return json.load(f)


st.markdown("""<style> .block-container {
                padding-top:    0.8rem;
                padding-bottom: 0rem;
                padding-left:   5rem;
                padding-right:  5rem;
            } </style>""", unsafe_allow_html=True)
st.title("Interactive Data Explorer")

cedit, cplot = st.columns(2)

default_code = """
print("Pages: {}".format(get_pages()))

d = get_page_data("pstatic_plots")

data = d["elements"]["dashboard"][0]["item_content"]["data"][0]["data"]

x = [e["x"] for e in data]
y = [e["y"] for e in data]


fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)
"""

with cedit:
    content = st_ace(
        value=default_code,
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
        # Note: If the environment is not trusted this is highly insecure!
        # use epicbox or similar
        default_prexif = "plt.style.use('dark_background')\n"
        f = StringIO()
        with redirect_stdout(f):
            exec(default_prexif + content)
        st.markdown("```\n {} \n```".format(f.getvalue()))

        #arr = np.random.normal(1, 1, size=100)
        #fig, ax = plt.subplots()
        #ax.hist(arr, bins=20)
#
        #st.pyplot(fig)