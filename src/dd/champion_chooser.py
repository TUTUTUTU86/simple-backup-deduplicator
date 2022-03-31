from src.dd.align.segmenter import Manifest


class ChampionChooser:
    def __init__(self, max_champions):
        self.max_champions = max_champions
        self.index = {}

    def choose(self, hooks) -> list:
        ...
    #     choose champions

    def add(self, manifest: Manifest):
        ...
        # update sparse_index