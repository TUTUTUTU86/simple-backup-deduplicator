class SparseIndex:
    def __init__(self):
        self.sparse_index = {}
        self.max_segments_id = 2

    def add(self, hook, segment_id):
        id_list = self.sparse_index.get(hook)
        if id_list is None:
            self.sparse_index.update({hook: [segment_id]})
        else:
            if len(id_list) < self.max_segments_id:
                id_list.append(segment_id)
                self.sparse_index.update({hook: id_list})
            else:
                id_list.pop(0)
                id_list.append(segment_id)
                self.sparse_index.update({hook: id_list})




