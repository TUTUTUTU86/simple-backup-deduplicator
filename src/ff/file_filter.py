from pathlib import Path

from src.ff.folder_index import FolderIndex


class FileFilter:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.folder_indices = [FolderIndex(self.root_dir)]

    def filter(self):
        old_index = self.folder_indices[-1].index
        new_index = FolderIndex(self.root_dir).index
        result = new_index.merge(old_index, indicator=True, how='left')
        result = result[result._merge == 'left_only']
        result.drop('_merge', axis=1, inplace=True)
        return result;

