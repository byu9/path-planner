from math import inf

from .graphs import DiGraph


class _ShortestPathResult:
    def __init__(self, parents, distances):
        self._parents = parents
        self._distances = distances

    def path_to(self, dst_node):
        path = list()
        iterator = dst_node

        while True:
            path.append(iterator)

            if iterator == self._parents[iterator]:
                break

            iterator = self._parents[iterator]

        path.reverse()
        return path

    def distance_to(self, dst_node):
        return self._distances[dst_node]


def dijkstra(graph: DiGraph, src_node):
    # Stores the optimal distance from the source node terminating at a certain descendant node.
    distance_from_src = {node: inf for node in graph.nodes}
    distance_from_src[src_node] = 0.0

    # Stores the parent in the shortest path terminating at a certain descendant node
    last_segment_from_src = {src_node: src_node}

    nodes_to_settle = set(graph.nodes)
    while nodes_to_settle:

        # The closest unsettled node is considered settled
        just_settled_node = min(nodes_to_settle, key=distance_from_src.get)
        nodes_to_settle.remove(just_settled_node)

        # Visit children of the just settled node and update their paths if a better one is found.
        for child in graph.children_of(just_settled_node):
            if child in nodes_to_settle:
                edge_weight = graph.weight_of(edge=(just_settled_node, child))

                existing_distance = distance_from_src[child]
                new_distance = distance_from_src[just_settled_node] + edge_weight

                if new_distance < existing_distance:
                    distance_from_src[child] = new_distance
                    last_segment_from_src[child] = just_settled_node

    return _ShortestPathResult(parents=from_src_via, distances=distance_from_src)


def dijkstra_bidir(graph: DiGraph, src_node, dst_node):
    f_distances = {node: inf for node in graph.nodes}
    b_distances = {node: inf for node in graph.nodes}
    f_distances[src_node] = 0.0
    b_distances[dst_node] = 0.0

    return _ShortestPathResult(parents=parents, distances=distances)
