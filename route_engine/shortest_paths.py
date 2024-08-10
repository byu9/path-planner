from itertools import product as cross_product
from math import inf

from .graphs import DiGraph


def _link_segments(end_node, segment_dict, reverse=False) -> list:
    path = list()

    while end_node in segment_dict:
        path.append(end_node)

        previous_link = segment_dict[end_node]
        if end_node == previous_link:
            break

        end_node = previous_link

    if reverse:
        path.reverse()

    return path


def dijkstra(graph: DiGraph, src_node):
    # Stores the optimal distance from the source node terminating at a certain descendant node.
    distances = {node: inf for node in graph.nodes}
    distances[src_node] = 0.0

    # Stores the parent in the shortest path terminating at a certain descendant node
    segments = {src_node: src_node}

    settled = set()
    visited = {src_node}

    while visited:

        # The closest unsettled node is considered settled
        just_settled = min(visited, key=distances.get)
        visited.remove(just_settled)
        settled.add(just_settled)

        # Visit children of the just settled node and update their paths if a better one is found.
        for child in graph.children_of(just_settled):
            if child not in settled:
                visited.add(child)

                edge_weight = graph.weight_of(edge=(just_settled, child))
                existing_distance = distances[child]
                new_distance = distances[just_settled] + edge_weight

                if new_distance < existing_distance:
                    distances[child] = new_distance
                    segments[child] = just_settled

    shortest_path = {
        end_node: _link_segments(end_node, segments, reverse=True)
        for end_node in segments
    }

    shortest_path_distance = distances
    return shortest_path, shortest_path_distance


def dijkstra_bidir(graph: DiGraph, src_node, dst_node):
    # The bidirectional variant is similar to the uni-directional variant, but we search from
    # both sides, and terminate when the two fronts meet. The source front is expanding to
    # descendants, and the destination front is expanding to ancestors.
    distances_src = {node: inf for node in graph.nodes}
    distances_src[src_node] = 0.0

    distances_dst = {node: inf for node in graph.nodes}
    distances_dst[dst_node] = 0.0

    segments_src = {src_node: src_node}
    segments_dst = {dst_node: dst_node}

    settled_src = set()
    settled_dst = set()

    visited_src = {src_node}
    visited_dst = {dst_node}

    while visited_src or visited_dst:

        just_settled_src = min(visited_src, key=distances_src.get)
        just_settled_dst = min(visited_dst, key=distances_dst.get)

        visited_src.remove(just_settled_src)
        visited_dst.remove(just_settled_dst)

        settled_src.add(just_settled_src)
        settled_dst.add(just_settled_dst)

        # We stop if we find a node whose path is settled from both sides, indicating that the
        # two fronts have met. However, the path may not be optimal. After we break out of the
        # loop, we need to keep searching among nodes visited by both sides.
        if set.intersection(settled_src, settled_dst):
            break

        for child in graph.children_of(just_settled_src):
            if child not in settled_src:
                visited_src.add(child)

                edge_weight = graph.weight_of(edge=(just_settled_src, child))
                existing_distance = distances_src[child]
                new_distance = distances_src[just_settled_src] + edge_weight

                if new_distance < existing_distance:
                    distances_src[child] = new_distance
                    segments_src[child] = just_settled_src

        for parent in graph.parents_of(just_settled_dst):
            if parent not in settled_dst:
                visited_dst.add(parent)

                edge_weight = graph.weight_of(edge=(parent, just_settled_dst))
                existing_distance = distances_dst[parent]
                new_distance = distances_dst[just_settled_dst] + edge_weight

                if new_distance < existing_distance:
                    distances_dst[parent] = new_distance
                    segments_dst[parent] = just_settled_dst

    overlapped_nodes = set.intersection(
        set.union(settled_src, visited_src),
        set.union(settled_dst, visited_dst)
    )

    overlapped_distances = {
        node: distances_src[node] + distances_dst[node]
        for node in overlapped_nodes
    }

    best_overlapped_node = min(overlapped_distances, key=overlapped_distances.get)
    shortest_return_path = _link_segments(best_overlapped_node, segments_src, reverse=True)
    shortest_forward_path = _link_segments(best_overlapped_node, segments_dst)

    shortest_path = [*shortest_return_path[:-1], best_overlapped_node, *shortest_forward_path[1:]]
    shortest_path_distance = overlapped_distances[best_overlapped_node]

    return shortest_path, shortest_path_distance


class ContractionRouter:
    def __init__(self):
        pass

    def preprocess(self, graph, contraction_order):
        for node in contraction_order:
            self._contract(graph, node)

    def shortest_path(self, src_node, dst_node):
        pass

    def _contract(self, graph, node):
        parents = graph.parents_of(node)
        children = graph.children_of(node)

        for parent, child in cross_product(parents, children):
            result = dijkstra_bidir(graph, parent, child)

            if result is not None:
                path, distance = result

                if node in path:
                    graph.add_shortcut(parent, child, distance)
