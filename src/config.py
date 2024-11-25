from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Final


class Config:
    ROOT_PATH: Final = Path(__file__).parent.parent
    DATA_PATH: Final = ROOT_PATH / "src" / "data" / "storage.jsonl"


config = Config()
