
import streamlit as st
from streamlit_ace import st_ace


if not "debug_edit" in st.session_state:
    st.session_state["debug_edit"] = False

if not "debug_content" in st.session_state:
    st.session_state["debug_content"] = "Debug"

if st.session_state["debug_edit"] == False:
    if st.button("Edit"):
        st.session_state["debug_edit"] = True
        st.rerun()
    st.markdown(st.session_state["debug_content"])
else:
    content = st_ace(
        value=st.session_state["debug_content"],
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

    if content != st.session_state["debug_content"]:
        st.session_state["debug_content"] = content
        st.session_state["debug_edit"] = False
        st.rerun()