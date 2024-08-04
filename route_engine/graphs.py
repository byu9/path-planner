class MultiDiGraph:
    def __init__(self):
        self._node_data = dict()
        self._edge_data = dict()
        self._node_children = dict()
        self._node_parents = dict()

    def insert_node(self, node):
        if node in self._node_data:
            raise ValueError(f'Node "{node}" exists.')

        self._node_data[node] = dict()
        self._node_children[node] = set()
        self._node_parents[node] = set()

    @property
    def nodes(self):
        yield from self._node_data.keys()

    def children_of(self, node):
        if node not in self._node_children:
            raise LookupError(f'Node "{node}" does not exist.')

        yield from self._node_children[node]

    def parents_of(self, node):
        if node not in self._node_parents:
            raise LookupError(f'Node "{node}" does not exist.')

        yield from self._node_parents[node]

    def node_data(self, node):
        if node not in self._node_data:
            raise LookupError(f'Node "{node}" does not exist.')

        return self._node_data[node]

    def insert_edge(self, src_node, dst_node, edge_key):
        if src_node not in self._node_data:
            raise ValueError(f'Source node "{src_node}" does not exist.')

        if dst_node not in self._node_data:
            raise ValueError(f'Destination node "{dst_node}" does not exist.')

        if (src_node, dst_node) in self._edge_data:
            if edge_key in self._edge_data[src_node, dst_node]:
                raise ValueError(f'Edge "({src_node}, {dst_node}, {edge_key})" exists.')

            else:
                self._edge_data[src_node, dst_node][edge_key] = dict()

        else:
            self._edge_data[src_node, dst_node] = {edge_key: dict()}

        self._node_children[src_node].add(dst_node)
        self._node_parents[dst_node].add(src_node)

    @property
    def edges(self):
        for (src_node, dst_node), data_dicts in self._edge_data.items():
            for edge_key in data_dicts.keys():
                yield src_node, dst_node, edge_key

    def edge_data(self, src_node, dst_node, edge_key):
        if (src_node, dst_node) in self._edge_data:
            if edge_key in self._edge_data[src_node, dst_node]:
                return self._edge_data[src_node, dst_node][edge_key]

        raise ValueError(f'Edge "({src_node}, {dst_node}, {edge_key})" does not exist.')
