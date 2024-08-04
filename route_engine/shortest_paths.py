from math import inf

from .graphs import MultiDiGraph


def _compute_full_path(dst, src, parent_edges):
    path = list()

    node = dst
    while node != src:
        parent_edge = parent_edges[node]
        path.append(parent_edge)
        node, _, _ = parent_edge

    path.reverse()
    return path


def _get_distance(graph, edge):
    distance = graph.edge_data(edge)['distance']
    return distance


def dijkstra(graph: MultiDiGraph, src, dst=None, distance_func=_get_distance):
    distances = {
        node: 0.0 if node == src else inf
        for node in graph.nodes
    }

    # Parent of a node in the shortest path starting from src
    parent_edges = dict()

    unvisited_nodes = set(graph.nodes)
    while unvisited_nodes:

        # Evict the closest node from unvisited nodes
        closest = min(unvisited_nodes, key=distances.get)
        unvisited_nodes.remove(closest)

        # For each unvisited child of the closest node, update the path if traveling to
        # that child via the closest node results in a smaller distance.
        for child in graph.children_of(closest):
            if child in unvisited_nodes:

                # Select one of the edges if there are multiple parallel edges
                selected_edge = min(graph.edges_between(closest, child),
                                    key=lambda edge: distance_func(graph, edge))

                selected_edge_distance = distance_func(graph, selected_edge)

                if not selected_edge_distance >= 0:
                    raise ValueError(
                        f'Edge {selected_edge} has a negative distance of '
                        f'{selected_edge_distance}.'
                    )

                new_distance = distances[closest] + selected_edge_distance

                if new_distance < distances[child]:
                    distances[child] = new_distance
                    parent_edges[child] = selected_edge

    shortest_paths = {
        node: _compute_full_path(node, src, parent_edges)
        for node in graph.nodes
        if node != src
    }

    if dst is None:
        return shortest_paths, distances

    else:
        return shortest_paths[dst], distances[dst]
