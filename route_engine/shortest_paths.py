from math import inf


class _SingleSourceShortestPathResult:
    def __init__(self, src_node, segments, distances):
        self._src_node = src_node
        self._segments = segments
        self._distances = distances

    def _scan_segments(self, dst_node):
        path = list()

        node = dst_node
        while node != self._src_node:
            segment = self._segments[node]
            path.append(segment)
            node, _, _ = segment

        path.reverse()
        return path

    def _scan_waypoints(self, dst_node):
        waypoints = list()

        node = dst_node
        waypoints.append(node)

        while node != self._src_node:
            segment = self._segments[node]
            node, _, _ = segment
            waypoints.append(node)

        waypoints.reverse()
        return waypoints

    def distance_to(self, dst_node):
        return self._distances[dst_node]

    def path_to(self, dst_node):
        return self._scan_segments(dst_node)

    def waypoints_to(self, dst_node):
        return self._scan_waypoints(dst_node)


class DijkstraShortestPath:
    def __init__(self, graph):
        self._graph = graph

    def _length(self, edge):
        length = self._graph.edge_data(*edge)['length']

        if not length >= 0:
            raise ValueError(f'Edge "{edge}" has negative length "{length}".')

        return length

    def _edge_between(self, src_node, dst_node):
        parallel_edges = (
            (edge_src, edge_dst, edge_key)
            for edge_src, edge_dst, edge_key in self._graph.edges
            if (edge_src == src_node) and (edge_dst == dst_node)
        )

        shortest_edge = min(parallel_edges, key=self._length)
        return shortest_edge

    def solve(self, src_node):
        # Stores the optimal distance from the source node terminating at a
        # certain destination node.
        distances = {node: inf for node in self._graph.nodes}
        distances[src_node] = 0.0

        # Stores the last edge segment of the shortest path from the source
        # node terminating at a certain destination node
        segments = dict()

        unexplored_nodes = set(self._graph.nodes)
        while unexplored_nodes:

            # Evicts a node closest to the source to explore.
            # Previously explored nodes are never explored again because they would have a shorter
            # distance than the node currently being explored and all its children.
            closest = min(unexplored_nodes, key=distances.get)
            unexplored_nodes.remove(closest)

            # For each unexplored child, update the path if traveling through the current node
            # to that child results in a smaller distance than previously recorded.
            for child in self._graph.children_of(closest):
                if child in unexplored_nodes:
                    edge = self._edge_between(src_node=closest, dst_node=child)
                    if edge is not None:
                        new_distance = distances[closest] + self._length(edge)

                        if new_distance < distances[child]:
                            distances[child] = new_distance
                            segments[child] = edge

        return _SingleSourceShortestPathResult(
            src_node=src_node,
            segments=segments,
            distances=distances,
        )
