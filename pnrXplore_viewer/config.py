from dataclasses import dataclass
from pathlib import Path, PosixPath


class Config:
    BUNDLES_DIR: PosixPath = Path("./bundles")
