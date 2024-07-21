from math import inf

from .graphs import MultiDiGraph


def dijkstra(graph: MultiDiGraph, src, dst):
    distances = {
        node: 0.0 if node == src else inf
        for node in graph.nodes
    }

    # Parent of a node in the shortest path starting from src
    parent_edges = dict()

    unvisited_nodes = set(graph.nodes)
    while unvisited_nodes:

        parent = min(unvisited_nodes, key=distances.get)
        unvisited_nodes.remove(parent)

        for child in graph.children_of(parent):
            if child in unvisited_nodes:
                edge = min(graph.edges_between(parent, child),
                           key=lambda e: graph.edge_data(e)['distance'])

                distance = distances[parent] + graph.edge_data(edge)['distance']

                if distance < distances[child]:
                    distances[child] = distance
                    parent_edges[child] = edge

    return distances, parent_edges
