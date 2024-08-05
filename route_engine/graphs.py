def _must_be_non_negative(val):
    if not val >= 0:
        raise ValueError(f'Value {val} is not non-negative.')


class DiGraph:
    def __init__(self):
        self._nodes = dict()
        self._edge_weights = dict()
        self._node_children = dict()
        self._node_parents = dict()

    def _node_must_exist(self, node):
        if node not in self._nodes:
            raise ValueError(f'Node "{node}" does not exist.')

    def _node_must_not_exist(self, node):
        if node in self._nodes:
            raise ValueError(f'Node "{node}" exists.')

    def _edge_must_exist(self, edge):
        if edge not in self._edge_weights:
            raise ValueError(f'Edge "{edge}" does not exist.')

    def _edge_must_not_exist(self, edge):
        if edge in self._edge_weights:
            raise ValueError(f'Edge "{edge}" exists.')

    def _check_insert_node(self, node):
        if node not in self._nodes:
            self._nodes[node] = dict()
            self._node_children[node] = set()
            self._node_parents[node] = set()

    @property
    def nodes(self):
        return self._nodes.keys()

    def children_of(self, node):
        self._node_must_exist(node)
        return self._node_children[node]

    def parents_of(self, node):
        self._node_must_exist(node)
        return self._node_parents[node]

    def node_data(self, node):
        self._node_must_exist(node)
        return self._nodes[node]

    def insert_edge(self, src_node, dst_node, weight):
        edge = src_node, dst_node
        self._edge_must_not_exist(edge)
        _must_be_non_negative(weight)

        self._check_insert_node(src_node)
        self._check_insert_node(dst_node)

        self._edge_weights[edge] = weight
        self._node_children[src_node].add(dst_node)
        self._node_parents[dst_node].add(src_node)

    @property
    def edges(self):
        return self._edge_weights.keys()

    def weight_of(self, edge):
        self._edge_must_exist(edge)
        return self._edge_weights[edge]
