
import streamlit as st
import base64

class PageHelper:
    @staticmethod
    def image_path_to_base64(image_path):
        try:
            with open(image_path, "rb") as image_file:
                binary_data = image_file.read()
                base64_bytes = base64.b64encode(binary_data)
                base64_string = base64_bytes.decode('utf-8')
            return base64_string
        except Exception as e:
            st.error(f"Cannot load render {e}")
            return None
