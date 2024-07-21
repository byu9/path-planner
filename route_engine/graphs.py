class MultiDiGraph:
    def __init__(self):
        self._nodes = set()
        self._parallel_edges = dict()

    def insert_edge(self, src, dst, key, **edge_data):

        if (src, dst) not in self._parallel_edges:
            self._parallel_edges[src, dst] = {key: edge_data}

        elif key in self._parallel_edges[src, dst]:
            raise ValueError(f'Edge ({src=:}, {dst=:}, {key=:}) exists.')

        else:
            self._parallel_edges[src, dst][key] = edge_data

        self._nodes.add(src)
        self._nodes.add(dst)

    @property
    def nodes(self):
        yield from self._nodes

    def children_of(self, node):
        """
        Returns children of the given node.
        :param node: Node whose children are to be returned.
        :return: Children of the given node as a sequence, which may be empty.
        """
        for (src, dst) in self._parallel_edges.keys():
            if src == node:
                yield dst

    def edges_between(self, src, dst):
        """
        Returns edges between two nodes as a sequence.

        :param src: Source node
        :param dst: Destination node
        :return: Sequence of tuple(src, dst, key) each uniquely identifying an
        edge between the two nodes. If they are not connected, an empty
        sequence is returned.
        """
        if (src, dst) in self._parallel_edges:
            for key in self._parallel_edges[src, dst].keys():
                yield src, dst, key

    def edge_data(self, edge):
        """
        Returns the data stored in the edge as a modifiable dictionary
        :param edge: tuple(src, dst, key) uniquely identifying the edge
        :return: Data stored in the edge as a modifiable dictionary
        """
        src, dst, key = edge

        if (src, dst) not in self._parallel_edges:
            raise ValueError(f'No edges exist between {src=:} and {dst=:}')

        if key not in self._parallel_edges[src, dst]:
            raise ValueError(
                f'No edge with {key=:} exists between {src=:} and {dst=:}'
            )

        return self._parallel_edges[src, dst][key]
