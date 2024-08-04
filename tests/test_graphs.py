import unittest

from route_engine.graphs import MultiDiGraph


class TestMultiDiGraph(unittest.TestCase):

    def test1(self):
        graph = MultiDiGraph()

        graph.insert_node('a')
        graph.insert_node('b')
        graph.insert_node('c')

        graph.node_data('a')['name'] = 'a'
        graph.node_data('b')['name'] = 'b'
        graph.node_data('c')['name'] = 'c'

        self.assertEqual(graph.node_data('a')['name'], 'a')
        self.assertEqual(graph.node_data('b')['name'], 'b')
        self.assertEqual(graph.node_data('c')['name'], 'c')

        # Insert duplicate nodes must raise error
        with self.assertRaises(ValueError):
            graph.insert_node('a')

        graph.insert_edge(src_node='a', dst_node='b', edge_key='0')
        graph.insert_edge(src_node='a', dst_node='b', edge_key='1')
        graph.insert_edge(src_node='a', dst_node='c', edge_key='0')
        graph.insert_edge(src_node='b', dst_node='a', edge_key='0')

        graph.edge_data('a', 'b', '0')['name'] = 'e0'
        graph.edge_data('a', 'b', '1')['name'] = 'e1'
        graph.edge_data('a', 'c', '0')['name'] = 'e2'
        graph.edge_data('b', 'a', '0')['name'] = 'e3'

        self.assertEqual(graph.edge_data('a', 'b', '0')['name'], 'e0')
        self.assertEqual(graph.edge_data('a', 'b', '1')['name'], 'e1')
        self.assertEqual(graph.edge_data('a', 'c', '0')['name'], 'e2')
        self.assertEqual(graph.edge_data('b', 'a', '0')['name'], 'e3')

        # Inserting duplicate edges must raise error
        with self.assertRaises(ValueError):
            graph.insert_edge(src_node='a', dst_node='b', edge_key='0')

        self.assertCountEqual(graph.nodes, ['a', 'b', 'c'])
        self.assertCountEqual(graph.edges, [
            ('a', 'b', '0'),
            ('a', 'b', '1'),
            ('a', 'c', '0'),
            ('b', 'a', '0')
        ])

        self.assertCountEqual(graph.children_of('a'), ['b', 'c'])
        self.assertCountEqual(graph.children_of('b'), ['a'])
        self.assertCountEqual(graph.children_of('c'), [])

        self.assertCountEqual(graph.parents_of('a'), ['b'])
        self.assertCountEqual(graph.parents_of('b'), ['a'])
        self.assertCountEqual(graph.parents_of('c'), ['a'])
