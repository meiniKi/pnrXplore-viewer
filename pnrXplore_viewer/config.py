import os
from pathlib import Path, PosixPath
import streamlit as st


class Config:
    """Viewer configurations."""
    # When the debug flag is set, data will be taken from a folder called _debug_
    # in the _bundles_ directory. This directory shall contain the uncompressed bundle.
    # Thus, faster debug iterations are possible. Note that no copy of the data is taken.
    # Unlike in productive use, all modifications are applied in place.
    #
    DEBUG: bool = os.environ.get("PNRXPLORE_DEBUG", False)

    # Directory where to search for bundles listed in the welcome page.
    #
    BUNDLES_DIR: PosixPath = Path(os.environ.get("PNRXPLORE_BUNDLES_DIR", "./bundles"))

    # Base name of the bundle that is created when clicking the download button.
    # It will be stored in the _bundles_ directory.
    #
    FILENAME_BASE_DOWNLAOD: str = "latest_download"

    # File that contains the bundle index.
    #
    PAGE_INDEX_FILE: str = "index.json"

    # File that contains the page-specific data
    #
    PAGE_DATA_FILE: str = "data.json"

    @classmethod
    def apply(self):
        st.session_state["debug"] = self.DEBUG
