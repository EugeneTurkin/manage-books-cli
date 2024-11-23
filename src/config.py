from __future__ import annotations

import os
from pathlib import Path
from typing import Final


class Config:
    ROOT_PATH: Final = Path(__file__).parent.parent
    DATA_PATH: Final = ROOT_PATH / "src" / "data" / "storage.jsonl"


config = Config()
