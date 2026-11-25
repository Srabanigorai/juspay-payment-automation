import json
import os
import re
from pathlib import Path

import yaml

from config.settings import ROOT


def load_test_data() -> dict:
    return json.loads((ROOT / "test_data" / "cards.json").read_text())


_VAR = re.compile(r"\$\{([A-Z0-9_]+)\}")


def expand_env(value):
    """Replace ${VAR} with environment values so secrets never live in the repo."""
    if isinstance(value, str):
        return _VAR.sub(lambda m: os.getenv(m.group(1), ""), value)
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    return value


def load_targets(filename: str) -> list[dict]:
    raw = yaml.safe_load(Path(ROOT / "config" / filename).read_text()) or {}
    return [expand_env(t) for t in raw.get("targets", []) if t.get("enabled")]
