import streamlit as st
from streamlit_image_select import image_select
from PIL import Image, ImageDraw, ImageFont

from pathlib import Path
import zipfile
import tarfile
import shutil
import tempfile
import io


def copy_to_proc_root(bundle_file, from_buffer=False):
    if from_buffer:
        bundle_bfr = io.BytesIO()
        bundle_bfr.write(bundle_file.read())
        bundle_bfr.seek(0)
    else:
        bundle_bfr = bundle_file

    if (f := st.session_state.get("manger_uploaded_root", None)) is not None:
        shutil.rmtree(f)
        st.session_state["manger_pages_keys"] = None

    tf = tempfile.mkdtemp()
    st.session_state["manger_uploaded_root"] = tf
    st.session_state["manger_uploaded_name"] = Path(bundle_file).stem

    suffix = Path(bundle_file).suffix
    if suffix == ".zip":
        zf = zipfile.ZipFile(bundle_bfr)
        zf.extractall(tf)
    elif suffix == ".tar":
        if from_buffer:
            bundle_bfr.extractall(path=tf)
        else:
            with tarfile.open(bundle_file, "r") as tar:
                tar.extractall(path=tf)
    else:
        raise ValueError("Invalid suffix for bundle.")

    st.rerun()


def load_from_existing(name: str):
    if st.session_state.get("debug", False):
        st.session_state["manger_uploaded_root"] = "./archives/{}".format(
            Path(name).stem
        )
        st.session_state["manger_uploaded_name"] = Path(name).stem
        st.rerun()
    st.session_state["manger_uploaded_name"] = Path(name).stem
    copy_to_proc_root((Path("./archives") / Path(name)).absolute())


def render_text_to_image(text, image_size=256, max_lines=4, initial_font_size=40):
    image = Image.new("RGB", (image_size, image_size), "#0E1117")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    font_size = initial_font_size
    while font_size > 10:
        font = ImageFont.load_default(font_size)
        lines = []
        words = text.split()

        while words and len(lines) < max_lines:
            line = ""
            while (
                words
                and draw.textbbox((0, 0), line + " " + words[0], font=font)[2]
                < image_size
            ):
                line += (" " if line else "") + words.pop(0)
            lines.append(line)
        if not words:
            break
        font_size -= 2

    text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
    y_offset = (image_size - text_height) // 2

    for line in lines:
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        x_offset = (image_size - text_width) // 2
        draw.text((x_offset, y_offset), line, font=font, fill="white")
        y_offset += draw.textbbox((0, 0), line, font=font)[3]
    return image


st.title("Upload or Select pnrXplor Archive")

uploaded_archive = st.file_uploader(
    label="Upload an archvie", label_visibility="hidden", accept_multiple_files=False
)

st.divider()
bundles = list(
    {
        str(file.name)
        for file in (
            list(Path("./archives").rglob("*.zip"))
            + list(Path("./archives").rglob("*.tar"))
        )
        if file.is_file()
    }
)

sel_bundle_quick = image_select(
    "Quick Links",
    [render_text_to_image(b) for b in bundles],
    use_container_width=False,
    return_value="index",
    key="sel_quick_from_existing_folder",
)

if not "sel_quick_from_existing_folder_init" in st.session_state:
    st.session_state["sel_quick_from_existing_folder_init"] = True
else:
    load_from_existing(bundles[sel_bundle_quick])

sel_bundle = st.selectbox(
    label="Or Select from Default Folder",
    key="sel_from_existing_folder",
    options=bundles,
)


if st.button("Analyze"):
    if st.session_state.get("debug", False):
        st.session_state["manger_uploaded_root"] = (
            "/home/user/Documents/repos/pnrXplore-viewer/archives/run"
        )
        st.rerun()

    if uploaded_archive is not None:
        copy_to_proc_root(uploaded_archive, True)
    else:
        load_from_existing(st.session_state.get("sel_from_existing_folder"))
