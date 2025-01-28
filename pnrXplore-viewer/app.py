
import streamlit as st
from manager import Manager
import json

#st.session_state["debug"] = True


if "manager" not in st.session_state:
    st.session_state.manager = Manager()


st.session_state.manager.run()
