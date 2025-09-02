from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG_PATH = Path("config/config.json")


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)
