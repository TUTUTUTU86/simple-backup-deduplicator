from pathlib import Path
from fastcdc import fastcdc_py


class Chunker:
    def __init__(self):
        ...

    @staticmethod
    def chunk(file: Path):
        with file.open("rb") as stream:
            chunks = list(fastcdc_py.fastcdc_py(stream))
        return chunks

