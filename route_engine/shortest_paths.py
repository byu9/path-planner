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
    # Stores the optimal distance from the source node terminating at a
    # certain descendant node.
    distances = {node: inf for node in graph.nodes}
    distances[src_node] = 0.0

    # Stores the parent in the shortest path terminating at a certain descendant node
    parents = {src_node: src_node}

    unexplored_nodes = set(graph.nodes)
    while unexplored_nodes:

        # Evicts a node closest to the source to explore.
        # Previously explored nodes are never explored again because they would have a shorter
        # distance than the node currently being explored and all its children.
        closest = min(unexplored_nodes, key=distances.get)
        unexplored_nodes.remove(closest)

        # For each unexplored child, update the path if traveling through the current node
        # to that child results in a smaller distance than previously recorded.
        for child in graph.children_of(closest):
            if child in unexplored_nodes:

                edge = (closest, child)
                new_distance = distances[closest] + graph.weight_of(edge)

                if new_distance < distances[child]:
                    distances[child] = new_distance
                    parents[child] = closest

    return _ShortestPathResult(parents=parents, distances=distances)
