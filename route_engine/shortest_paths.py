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
        end_node: _link_segments(end_node, last_segment_from_src, reverse=True)
        for end_node in last_segment_from_src
    }

    shortest_path_distance = distance_from_src
    return shortest_path, shortest_path_distance


def dijkstra_bidir(graph: DiGraph, src_node, dst_node):
    # The bidirectional variant is similar to the uni-directional variant, but we search from
    # both sides, and terminate when the two fronts meet. The source front is expanding to
    # descendants, and the destination front is expanding to ancestors.
    distance_from_src = {node: inf for node in graph.nodes}
    distance_from_src[src_node] = 0.0
    distance_to_dst = {node: inf for node in graph.nodes}
    distance_to_dst[dst_node] = 0.0

    last_segment_from_src = {src_node: src_node}
    first_segment_to_dst = {dst_node: dst_node}

    settled_nodes_from_src = set()
    nodes_to_settle_from_src = {src_node}
    settled_nodes_to_dst = set()
    nodes_to_settle_to_dst = {dst_node}

    while nodes_to_settle_from_src or nodes_to_settle_to_dst:

        just_settled_from_src = min(nodes_to_settle_from_src, key=distance_from_src.get)
        just_settled_to_dst = min(nodes_to_settle_to_dst, key=distance_to_dst.get)

        if distance_from_src[just_settled_from_src] < distance_to_dst[just_settled_to_dst]:
            nodes_to_settle_from_src.remove(just_settled_from_src)
            settled_nodes_from_src.add(just_settled_from_src)

            for child in graph.children_of(just_settled_from_src):
                if child not in settled_nodes_from_src:
                    nodes_to_settle_from_src.add(child)

                    edge_weight = graph.weight_of(edge=(just_settled_from_src, child))
                    existing_distance = distance_from_src[child]
                    new_distance = distance_from_src[just_settled_from_src] + edge_weight

                    if new_distance < existing_distance:
                        distance_from_src[child] = new_distance
                        last_segment_from_src[child] = just_settled_from_src
        else:
            nodes_to_settle_to_dst.remove(just_settled_to_dst)
            settled_nodes_to_dst.add(just_settled_to_dst)

            for parent in graph.parents_of(just_settled_to_dst):
                if parent not in settled_nodes_to_dst:
                    nodes_to_settle_to_dst.add(parent)

                    edge_weight = graph.weight_of(edge=(parent, just_settled_to_dst))
                    existing_distance = distance_to_dst[parent]
                    new_distance = distance_to_dst[just_settled_to_dst] + edge_weight

                    if new_distance < existing_distance:
                        distance_to_dst[parent] = new_distance
                        first_segment_to_dst[parent] = just_settled_to_dst
        # We stop if we find a node whose path is settled from both sides. However, the path
        # connected by the meeting node may not be optimal, since it may be on the tip of a
        # triangle where a direct shorter path exists between one of its parents and one of its
        # children. To make sure the path is optimal, we also need to check all such connections.
        if set.intersection(settled_nodes_from_src, settled_nodes_to_dst):
            break

    visited_from_both_sides = set.intersection(
        set.union(settled_nodes_from_src, nodes_to_settle_from_src),
        set.union(settled_nodes_to_dst, nodes_to_settle_to_dst))

    distances = {
        u: distance_from_src[u] + distance_to_dst[u]
        for u in visited_from_both_sides
    }

    best_node = min(distances, key=distances.get)

    return_path = _link_segments(best_node, last_segment_from_src, reverse=True)
    forward_path = _link_segments(best_node, first_segment_to_dst)

    path = [*return_path[:-1], best_node, *forward_path[1:]]
    distance = distances[best_node]

    return path, distance
