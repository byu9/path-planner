import unittest

from route_engine.graphs import MultiDiGraph
from route_engine.shortest_paths import dijkstra


class TestDijkstra(unittest.TestCase):
    def test1(self):
        graph = MultiDiGraph()
        graph.insert_edge('a', 'b', 'primary', distance=20)
        graph.insert_edge('a', 'b', 'secondary', distance=10)
        graph.insert_edge('a', 'c', 'primary', distance=100)
        graph.insert_edge('b', 'd', 'primary', distance=1)
        graph.insert_edge('a', 'd', 'primary', distance=20)

        distances, parents = dijkstra(graph, 'a', 'd')
        print(distances)
        print(parents)
