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
    distance_from_src = {node: inf for node in graph.nodes}
    distance_from_src[src_node] = 0.0

    # Stores the parent in the shortest path terminating at a certain descendant node
    last_segment_from_src = {src_node: src_node}

    settled_nodes = set()
    nodes_to_settle = {src_node}

    while nodes_to_settle:

        # The closest unsettled node is considered settled
        just_settled_node = min(nodes_to_settle, key=distance_from_src.get)
        nodes_to_settle.remove(just_settled_node)
        settled_nodes.add(just_settled_node)

        # Visit children of the just settled node and update their paths if a better one is found.
        for child in graph.children_of(just_settled_node):
            if child not in settled_nodes:
                nodes_to_settle.add(child)

                edge_weight = graph.weight_of(edge=(just_settled_node, child))
                existing_distance = distance_from_src[child]
                new_distance = distance_from_src[just_settled_node] + edge_weight

                if new_distance < existing_distance:
                    distance_from_src[child] = new_distance
                    last_segment_from_src[child] = just_settled_node

    shortest_path = {
        end_node: _link_segments(end_node, segment_dict=last_segment_from_src, reverse=True)
        for end_node in last_segment_from_src
    }

    return shortest_path, distance_from_src


def dijkstra_bidir(graph: DiGraph, src_node, dst_node):
    f_distances = {node: inf for node in graph.nodes}
    b_distances = {node: inf for node in graph.nodes}
    f_distances[src_node] = 0.0
    b_distances[dst_node] = 0.0

    return _ShortestPathResult(parents=parents, distances=distances)
