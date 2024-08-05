import unittest

from route_engine.graphs import DiGraph


class TestMultiDiGraph(unittest.TestCase):

    def test1(self):
        graph = DiGraph()

        graph.insert_edge(src_node='a', dst_node='b', weight=0)
        graph.insert_edge(src_node='a', dst_node='c', weight=2)
        graph.insert_edge(src_node='b', dst_node='a', weight=3)

        # Inserting duplicate edges must raise error
        with self.assertRaises(ValueError):
            graph.insert_edge(src_node='a', dst_node='b', weight=0)

        self.assertCountEqual(graph.nodes, ['a', 'b', 'c'])
        self.assertCountEqual(graph.edges, [
            ('a', 'b'),
            ('a', 'c'),
            ('b', 'a')
        ])

        self.assertCountEqual(graph.children_of('a'), ['b', 'c'])
        self.assertCountEqual(graph.children_of('b'), ['a'])
        self.assertCountEqual(graph.children_of('c'), [])

        self.assertCountEqual(graph.parents_of('a'), ['b'])
        self.assertCountEqual(graph.parents_of('b'), ['a'])
        self.assertCountEqual(graph.parents_of('c'), ['a'])
