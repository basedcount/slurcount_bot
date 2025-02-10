from __future__ import annotations

import json
import re
from pathlib import Path


def load_slur_data() -> re.Pattern[str]:
    """Load slur data from the JSON file and compile the regex."""
    with Path("slurs.json").open("r") as fp:
        data = json.load(fp)
        slurs = data.get("slurs", [])
        slur_groups = data.get("slur_groups", [])

    if not slurs or not slur_groups:
        raise ValueError("Missing required keys 'slurs' or 'slur_groups' in slurs.json")

    return re.compile("|".join(f"(?P<{name}>{p})" for name, p in zip(slur_groups, slurs, strict=True)), re.IGNORECASE)


SLUR_REGEX = load_slur_data()
