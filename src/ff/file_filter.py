from pathlib import Path

from src.ff.folder_index import FolderIndex


class FileFilter:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.folder_indices = [FolderIndex(self.root_dir)]

    def filter(self):
        old_index = self.folder_indices[-1].index.values.tolist()
        new_index = FolderIndex(self.root_dir).index.values.tolist()
        for file in new_index:
            searching_list = [old_file for old_file in old_index if old_file[0] == file[0]]
            if any(searching_list):
                if searching_list[0][1] != file[1]:
                    new_index[new_index.index(file)].append("modified")
                else:
                    new_index[new_index.index(file)].append("-")
            else:
                new_index[new_index.index(file)].append("new")
        return [file for file in new_index if file[2] == "modified" or file[2] == "new"]
