from pathlib import Path

from src.dd.align.data_aligner import DataAligner

from src.dd.align.chunker import Chunker


def test_chunker():
    data_dir = Path("../data/dd_test")
    file_name = data_dir / "11.Queen - Now I'm Here.flac"
    chunker = Chunker()
    results = list(chunker.do(file_name))
    print([chunk.length for chunk in results])


def test_data_aligner():
    data_dir = Path("../data/dd_test")
    file_name = data_dir / "11.Queen - Now I'm Here.flac"
    data_aligner = DataAligner(chunk_size=8192, segment_size=2_000_000)
    total_size = 0
    for segment in data_aligner.do(files=[file_name]):
        total_size += segment.size
    print(f'total_size={total_size}, file_size={file_name.stat().st_size}')
    assert total_size == file_name.stat().st_size

