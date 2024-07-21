import unittest

from route_engine.graphs import MultiDiGraph


class TestGraph(unittest.TestCase):

    def test1(self):
        graph = MultiDiGraph()
        graph.insert_edge(src='a', dst='b', key='primary', weight=1)
        graph.insert_edge(src='a', dst='b', key='secondary', weight=2)
        graph.insert_edge(src='a', dst='c', key='primary', weight=5)
        graph.insert_edge(src='b', dst='a', key='primary', weight=6)

        with self.assertRaises(ValueError):
            graph.insert_edge(src='a', dst='b', key='primary', weight=1)

        self.assertCountEqual(graph.nodes, ['a', 'b', 'c'])

        self.assertCountEqual(graph.children_of('a'), ['b', 'c'])
        self.assertCountEqual(graph.children_of('b'), ['a'])
        self.assertCountEqual(graph.children_of('c'), [])

        self.assertCountEqual(graph.edges_between('a', 'b'), [
            ('a', 'b', 'primary'),
            ('a', 'b', 'secondary')
        ])

        self.assertCountEqual(graph.edges_between('a', 'c'), [('a', 'c', 'primary')])
        self.assertCountEqual(graph.edges_between('b', 'c'), [])

        self.assertEqual(graph.edge_data(('a', 'b', 'secondary')), {'weight': 2})
        self.assertEqual(graph.edge_data(('a', 'c', 'primary')), {'weight': 5})
