import os
import streamlit as st
from manager import Manager

st.session_state["debug"] = os.environ.get("PNRXPLORE_DEBUG", False)

if "manager" not in st.session_state:
    st.session_state.manager = Manager()

st.session_state.manager.run()
