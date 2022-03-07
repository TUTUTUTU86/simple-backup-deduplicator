import os
import pandas as pd
from pathlib import Path


class FolderIndex:
    def __init__(self, root_dir: Path):
        result = []
        for p in root_dir.iterdir():
            if p.is_dir():
                continue
            result.append([p, os.stat(p).st_mtime])
        self.index = pd.DataFrame(result, columns=['path', 'st_mtime'])

