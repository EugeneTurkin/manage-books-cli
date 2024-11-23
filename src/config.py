from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Final


class Config:
    """Configs are supposed to be configurable, but this one just holds constants because I realised this task's
    constraints too late.
    """

    ROOT_PATH: Final = Path(__file__).parent.parent
    DATA_PATH: Final = ROOT_PATH / "src" / "data" / "storage.jsonl"
    SHOW_STACK_TRACE: Final = False


config = Config()
