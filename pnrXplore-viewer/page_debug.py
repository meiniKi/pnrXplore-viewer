
import streamlit as st
from pathlib import Path
import zipfile
import shutil
import tempfile
import io
from streamlit_elements import elements, mui, html
from streamlit_elements import dashboard, media
from page_helper import PageHelper

st.title("Debugging Page")

if st.session_state.get("page_video_playing", None) is None:
    st.session_state["page_video_playing"] = False

with elements("dashboard"):
    layout = [
        dashboard.Item("first_item", 0, 0, 1, 1),
        dashboard.Item("second_item", 1, 1, 1, 1, isDraggable=True, isResizable=True),        dashboard.Item("second_item", 2, 2, 4, 4, isDraggable=True, isResizable=True),
        dashboard.Item("third_item", 1, 2, 1, 1, isDraggable=True, isResizable=True),
    ]

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    def toggle_playing():
        if st.session_state["page_video_playing"] == False:
            st.session_state["page_video_playing"] = True
        else:
            st.session_state["page_video_playing"] = False
        print(st.session_state["page_video_playing"])


    st.button(
        label="Button",
        key="playpause",
        on_click=toggle_playing
    )

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")

        with mui.Paper(key="second_item"):
            media.Player(
                url="data:video/mpeg;base64,"+PageHelper.image_path_to_base64("/home/user/Documents/repos/pnrXplore/pos_FF.mp4"),
                controls=True,
                width="100%",
                height="100%",
                playing=st.session_state["page_video_playing"]
                )
            
        with mui.Paper(key="third_item"):
            m1 = media.Player(
                url="data:video/mpeg;base64,"+PageHelper.image_path_to_base64("/home/user/Documents/repos/pnrXplore/pos_FF.mp4"),
                controls=True,
                width="100%",
                height="100%",
                playing=st.session_state["page_video_playing"]
                )