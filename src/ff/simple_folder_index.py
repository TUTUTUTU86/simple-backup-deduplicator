
import os
import pandas as pd
from pathlib import Path


def process(root_dir: Path):
    result = []
    for p in root_dir.iterdir():
        if p.is_dir():
            continue
        result.append(p)
    return result

