import os
import pandas as pd


class FolderIndex:
    def __init__(self, root_dir):
        result = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = root + "\\" + file
                result.append([file_path, os.stat(file_path).st_mtime])
        self.index = pd.DataFrame(result, columns=['path', 'st_mtime'])

