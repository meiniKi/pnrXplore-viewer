import streamlit as st
from nextpnr_viewer import nextpnr_viewer
import json

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run nextpnr_viewer/example.py`

# st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.
s = ""
with open(
    "/home/user/Documents/repos/pnrXplore-viewer/routed.json",
    "r",
) as f:
    s = f.read()

nextpnr_viewer("ecp5", "25k", s)
# st.markdown("You've clicked %s times!" % int(num_clicks))

# st.markdown("---")
# st.subheader("Component with variable args")

# Create a second instance of our component whose `name` arg will vary
# based on a text_input widget.
#
# We use the special "key" argument to assign a fixed identity to this
# component instance. By default, when a component's arguments change,
# it is considered a new instance and will be re-mounted on the frontend
# and lose its current state. In this case, we want to vary the component's
# "name" argument without having it get recreated.
# name_input = st.text_input("Enter a name", value="Streamlit")
# num_clicks = nextpnr_viewer(name_input, key="foo")
# st.markdown("You've clicked %s times!" % int(num_clicks))
