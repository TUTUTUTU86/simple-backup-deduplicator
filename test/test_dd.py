from pathlib import Path
import shutil

from src.dd.chunker import Chunker


def test_chunker():
    data_dir = Path("../data/dd_test")
    file_name = data_dir / "11.Queen - Now I'm Here.flac"
    results = list(Chunker.chunk(file_name))
    print([chunk.length for chunk in results])
