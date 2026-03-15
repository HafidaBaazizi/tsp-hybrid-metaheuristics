
from __future__ import annotations
from pathlib import Path
from typing import Dict

def load_best_known_solutions(path: str | Path) -> Dict[str, int]:
    text = Path(path).read_text(encoding='utf-8').replace(':', ' : ').split()
    out: Dict[str, int] = {}
    i = 0
    while i < len(text) - 2:
        name = text[i]
        if text[i + 1] == ':':
            value = text[i + 2]
            # some values contain annotations like 18660188 (CEIL_2D)
            try:
                out[name] = int(value)
            except ValueError:
                pass
            i += 3
        else:
            i += 1
    return out
