from pathlib import Path
import shutil

from src.ff.file_filter import FileFilter


def test_file_filter():
    data_dir = Path("../data/test")
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(exist_ok=True, parents=True)

    file_name = data_dir / "file.txt"
    # with open(file_name, "w") as f:
    #     f.write("123\n")

    file_filter = FileFilter(data_dir)

    with open(file_name, "w") as f:
        f.write("456\n")

    result = file_filter.filter()
    print(result)
