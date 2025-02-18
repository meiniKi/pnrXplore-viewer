import os
import streamlit as st
from manager import Manager
from config import Config

# Apply configs to streamlit before starting the manager
#
Config.apply()

# Start the manager
#
if "manager" not in st.session_state:
    st.session_state.manager = Manager()

st.session_state.manager.run()
