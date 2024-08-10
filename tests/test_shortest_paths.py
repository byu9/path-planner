import unittest

from route_engine.graphs import DiGraph
from route_engine.shortest_paths import dijkstra
from route_engine.shortest_paths import dijkstra_bidir


class TestDijkstra(unittest.TestCase):

    def setUp(self):
        self.graph = DiGraph()

        for src, dst, weight in _edges:
            self.graph.insert_edge(src, dst, weight)

    def test1(self):
        src_node, dst_node = 69, 40
        expected_path = [69, 75, 83, 23, 9, 22, 40]
        expected_distance = 81

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test2(self):
        src_node, dst_node = 10, 41
        expected_path = [10, 98, 94, 45, 41]
        expected_distance = 44

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test3(self):
        src_node, dst_node = 98, 37
        expected_path = [98, 87, 70, 26, 19, 92, 27, 65, 37]
        expected_distance = 54

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test4(self):
        src_node, dst_node = 88, 90
        expected_path = [88, 90]
        expected_distance = 15

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test5(self):
        src_node, dst_node = 30, 55
        expected_path = [30, 18, 48, 72, 97, 55]
        expected_distance = 85

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test6(self):
        src_node, dst_node = 32, 29
        expected_path = [32, 95, 80, 34, 68, 29]
        expected_distance = 74

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test7(self):
        src_node, dst_node = 19, 22
        expected_path = [19, 92, 27, 85, 31, 9, 22]
        expected_distance = 60

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test8(self):
        src_node, dst_node = 28, 25
        expected_path = [28, 9, 22, 25]
        expected_distance = 57

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test9(self):
        src_node, dst_node = 82, 44
        expected_path = [82, 27, 65, 37, 72, 44]
        expected_distance = 87

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)

    def test10(self):
        src_node, dst_node = 34, 49
        expected_path = [34, 68, 16, 94, 45, 49]
        expected_distance = 62

        path, distance = dijkstra(self.graph, src_node=src_node)
        self.assertEqual(path[dst_node], expected_path)
        self.assertAlmostEqual(distance[dst_node], expected_distance)


class TestDijkstraBiDir(unittest.TestCase):

    def setUp(self):
        self.graph = DiGraph()

        for src, dst, weight in _edges:
            self.graph.insert_edge(src, dst, weight)

    def test1(self):
        src_node, dst_node = 69, 40
        expected_path = [69, 75, 83, 23, 9, 22, 40]
        expected_distance = 81

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)

        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test2(self):
        src_node, dst_node = 10, 41
        # expected_path = [10, 98, 94, 45, 41]
        expected_distance = 44

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        # The shortest path for this case is not unique
        # self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test3(self):
        src_node, dst_node = 98, 37
        expected_path = [98, 87, 70, 26, 19, 92, 27, 65, 37]
        expected_distance = 54

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test4(self):
        src_node, dst_node = 88, 90
        expected_path = [88, 90]
        expected_distance = 15

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test5(self):
        src_node, dst_node = 30, 55
        expected_path = [30, 18, 48, 72, 97, 55]
        expected_distance = 85

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test6(self):
        src_node, dst_node = 32, 29
        expected_path = [32, 95, 80, 34, 68, 29]
        expected_distance = 74

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test7(self):
        src_node, dst_node = 19, 22
        expected_path = [19, 92, 27, 85, 31, 9, 22]
        expected_distance = 60

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test8(self):
        src_node, dst_node = 28, 25
        expected_path = [28, 9, 22, 25]
        expected_distance = 57

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test9(self):
        src_node, dst_node = 82, 44
        expected_path = [82, 27, 65, 37, 72, 44]
        expected_distance = 87

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)

    def test10(self):
        src_node, dst_node = 34, 49
        expected_path = [34, 68, 16, 94, 45, 49]
        expected_distance = 62

        path, distance = dijkstra_bidir(self.graph, src_node=src_node, dst_node=dst_node)
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(distance, expected_distance)


_edges = [
    (0, 3, 43.0),
    (0, 17, 48.0),
    (0, 67, 29.0),
    (0, 83, 43.0),
    (0, 97, 35.0),
    (1, 57, 21.0),
    (1, 82, 26.0),
    (2, 18, 37.0),
    (2, 37, 4.0),
    (2, 57, 22.0),
    (3, 0, 1.0),
    (3, 55, 28.0),
    (3, 86, 20.0),
    (3, 87, 24.0),
    (4, 27, 34.0),
    (4, 53, 12.0),
    (4, 72, 1.0),
    (4, 78, 32.0),
    (4, 79, 43.0),
    (5, 89, 38.0),
    (6, 3, 18.0),
    (6, 4, 21.0),
    (6, 13, 8.0),
    (6, 41, 46.0),
    (6, 44, 37.0),
    (6, 50, 27.0),
    (7, 26, 2.0),
    (7, 57, 43.0),
    (7, 68, 20.0),
    (7, 76, 18.0),
    (7, 86, 1.0),
    (8, 14, 44.0),
    (8, 37, 24.0),
    (8, 40, 21.0),
    (8, 48, 49.0),
    (8, 60, 9.0),
    (8, 73, 9.0),
    (8, 75, 25.0),
    (8, 91, 16.0),
    (9, 1, 48.0),
    (9, 5, 45.0),
    (9, 22, 10.0),
    (9, 30, 6.0),
    (9, 37, 21.0),
    (9, 38, 38.0),
    (9, 50, 4.0),
    (9, 58, 14.0),
    (9, 77, 4.0),
    (9, 84, 39.0),
    (10, 15, 14.0),
    (10, 23, 31.0),
    (10, 34, 34.0),
    (10, 48, 16.0),
    (10, 98, 8.0),
    (11, 4, 49.0),
    (11, 6, 45.0),
    (11, 16, 18.0),
    (11, 26, 19.0),
    (11, 28, 28.0),
    (11, 37, 16.0),
    (11, 57, 43.0),
    (11, 83, 50.0),
    (11, 93, 20.0),
    (12, 41, 42.0),
    (12, 56, 46.0),
    (12, 66, 25.0),
    (12, 76, 6.0),
    (12, 78, 49.0),
    (13, 48, 26.0),
    (13, 55, 16.0),
    (13, 65, 30.0),
    (14, 18, 21.0),
    (14, 31, 36.0),
    (14, 60, 20.0),
    (14, 84, 18.0),
    (14, 90, 30.0),
    (15, 8, 22.0),
    (15, 18, 38.0),
    (15, 79, 22.0),
    (15, 87, 37.0),
    (15, 88, 45.0),
    (15, 91, 49.0),
    (15, 95, 16.0),
    (16, 57, 31.0),
    (16, 94, 1.0),
    (17, 74, 12.0),
    (17, 91, 22.0),
    (18, 30, 43.0),
    (18, 48, 15.0),
    (19, 21, 33.0),
    (19, 30, 34.0),
    (19, 47, 12.0),
    (19, 76, 24.0),
    (19, 85, 42.0),
    (19, 92, 6.0),
    (20, 0, 37.0),
    (20, 12, 45.0),
    (20, 14, 29.0),
    (20, 50, 8.0),
    (20, 74, 3.0),
    (20, 87, 17.0),
    (20, 94, 26.0),
    (21, 19, 29.0),
    (21, 35, 28.0),
    (21, 67, 2.0),
    (21, 91, 17.0),
    (21, 98, 28.0),
    (22, 3, 47.0),
    (22, 18, 43.0),
    (22, 21, 16.0),
    (22, 25, 7.0),
    (22, 40, 25.0),
    (22, 47, 8.0),
    (22, 49, 38.0),
    (23, 9, 8.0),
    (23, 12, 20.0),
    (23, 16, 33.0),
    (23, 33, 9.0),
    (23, 41, 20.0),
    (23, 54, 3.0),
    (23, 56, 3.0),
    (23, 61, 10.0),
    (23, 68, 44.0),
    (23, 97, 31.0),
    (24, 22, 47.0),
    (24, 28, 41.0),
    (24, 39, 16.0),
    (24, 51, 21.0),
    (24, 78, 46.0),
    (24, 82, 17.0),
    (24, 90, 34.0),
    (25, 17, 49.0),
    (25, 46, 47.0),
    (25, 54, 35.0),
    (25, 57, 49.0),
    (25, 67, 39.0),
    (25, 89, 26.0),
    (26, 4, 1.0),
    (26, 7, 2.0),
    (26, 8, 30.0),
    (26, 19, 10.0),
    (26, 85, 36.0),
    (27, 43, 37.0),
    (27, 47, 48.0),
    (27, 65, 12.0),
    (27, 85, 18.0),
    (28, 3, 50.0),
    (28, 9, 40.0),
    (28, 19, 13.0),
    (28, 29, 28.0),
    (28, 30, 7.0),
    (28, 32, 8.0),
    (28, 36, 5.0),
    (28, 55, 27.0),
    (28, 80, 43.0),
    (28, 89, 33.0),
    (28, 92, 24.0),
    (28, 99, 43.0),
    (29, 64, 8.0),
    (29, 89, 18.0),
    (30, 10, 50.0),
    (30, 18, 33.0),
    (30, 98, 48.0),
    (31, 9, 20.0),
    (31, 65, 11.0),
    (31, 98, 42.0),
    (32, 12, 50.0),
    (32, 45, 13.0),
    (32, 64, 15.0),
    (32, 65, 9.0),
    (32, 90, 47.0),
    (32, 95, 10.0),
    (33, 36, 46.0),
    (33, 52, 23.0),
    (33, 72, 21.0),
    (33, 82, 48.0),
    (33, 87, 17.0),
    (34, 68, 1.0),
    (34, 70, 32.0),
    (34, 78, 49.0),
    (35, 12, 26.0),
    (35, 32, 17.0),
    (35, 50, 17.0),
    (36, 32, 46.0),
    (36, 58, 40.0),
    (36, 68, 41.0),
    (36, 71, 21.0),
    (36, 76, 28.0),
    (36, 82, 30.0),
    (37, 17, 3.0),
    (37, 48, 43.0),
    (37, 53, 19.0),
    (37, 54, 11.0),
    (37, 72, 8.0),
    (37, 87, 32.0),
    (38, 36, 3.0),
    (38, 55, 39.0),
    (38, 58, 44.0),
    (38, 65, 18.0),
    (39, 31, 42.0),
    (39, 91, 15.0),
    (39, 94, 12.0),
    (40, 30, 8.0),
    (40, 65, 34.0),
    (40, 89, 33.0),
    (41, 17, 46.0),
    (41, 72, 42.0),
    (41, 82, 39.0),
    (41, 87, 14.0),
    (41, 91, 2.0),
    (41, 95, 24.0),
    (42, 23, 38.0),
    (42, 32, 31.0),
    (42, 50, 38.0),
    (43, 22, 29.0),
    (43, 58, 3.0),
    (43, 67, 4.0),
    (43, 68, 43.0),
    (43, 74, 5.0),
    (43, 77, 11.0),
    (43, 94, 12.0),
    (44, 16, 30.0),
    (44, 21, 5.0),
    (44, 39, 31.0),
    (44, 55, 13.0),
    (44, 70, 13.0),
    (44, 84, 15.0),
    (45, 15, 27.0),
    (45, 41, 2.0),
    (45, 49, 17.0),
    (45, 80, 17.0),
    (45, 82, 40.0),
    (46, 14, 33.0),
    (46, 22, 49.0),
    (46, 33, 28.0),
    (46, 66, 25.0),
    (46, 72, 5.0),
    (46, 85, 19.0),
    (46, 87, 45.0),
    (47, 19, 43.0),
    (48, 7, 35.0),
    (48, 35, 12.0),
    (48, 64, 39.0),
    (48, 68, 9.0),
    (48, 72, 12.0),
    (48, 87, 33.0),
    (49, 4, 5.0),
    (49, 25, 24.0),
    (49, 27, 11.0),
    (49, 82, 6.0),
    (49, 93, 27.0),
    (50, 12, 20.0),
    (50, 30, 37.0),
    (51, 15, 22.0),
    (51, 24, 19.0),
    (51, 29, 32.0),
    (51, 76, 21.0),
    (52, 10, 28.0),
    (52, 12, 39.0),
    (52, 33, 44.0),
    (52, 57, 22.0),
    (52, 63, 15.0),
    (52, 77, 14.0),
    (52, 81, 17.0),
    (52, 90, 8.0),
    (53, 15, 22.0),
    (53, 27, 35.0),
    (53, 31, 21.0),
    (53, 66, 40.0),
    (53, 70, 26.0),
    (53, 74, 25.0),
    (53, 84, 41.0),
    (54, 67, 43.0),
    (55, 17, 6.0),
    (55, 62, 38.0),
    (55, 84, 47.0),
    (55, 92, 47.0),
    (55, 97, 9.0),
    (56, 45, 46.0),
    (56, 76, 10.0),
    (56, 81, 15.0),
    (57, 11, 26.0),
    (57, 42, 48.0),
    (57, 98, 41.0),
    (58, 9, 16.0),
    (58, 11, 38.0),
    (58, 41, 5.0),
    (58, 42, 38.0),
    (58, 54, 13.0),
    (58, 57, 25.0),
    (58, 63, 8.0),
    (59, 30, 30.0),
    (59, 38, 13.0),
    (59, 46, 2.0),
    (59, 53, 6.0),
    (59, 57, 34.0),
    (59, 62, 1.0),
    (59, 70, 45.0),
    (59, 91, 3.0),
    (60, 51, 36.0),
    (60, 69, 1.0),
    (61, 28, 15.0),
    (61, 34, 4.0),
    (61, 54, 38.0),
    (61, 74, 14.0),
    (61, 77, 20.0),
    (61, 82, 1.0),
    (61, 85, 5.0),
    (62, 3, 44.0),
    (62, 22, 26.0),
    (62, 25, 35.0),
    (62, 47, 15.0),
    (62, 59, 21.0),
    (63, 15, 50.0),
    (63, 58, 34.0),
    (63, 85, 45.0),
    (64, 92, 25.0),
    (64, 95, 41.0),
    (65, 31, 48.0),
    (65, 37, 11.0),
    (65, 91, 17.0),
    (66, 12, 38.0),
    (66, 28, 41.0),
    (66, 49, 48.0),
    (67, 4, 25.0),
    (67, 12, 7.0),
    (67, 19, 49.0),
    (67, 44, 49.0),
    (67, 48, 27.0),
    (67, 51, 8.0),
    (67, 85, 44.0),
    (68, 16, 20.0),
    (68, 29, 23.0),
    (68, 32, 40.0),
    (68, 44, 21.0),
    (69, 20, 46.0),
    (69, 75, 19.0),
    (69, 82, 41.0),
    (70, 26, 3.0),
    (70, 51, 41.0),
    (70, 78, 50.0),
    (71, 2, 47.0),
    (71, 4, 32.0),
    (71, 9, 20.0),
    (71, 15, 25.0),
    (71, 20, 25.0),
    (71, 23, 42.0),
    (71, 28, 22.0),
    (71, 40, 39.0),
    (71, 77, 41.0),
    (72, 44, 19.0),
    (72, 45, 25.0),
    (72, 73, 46.0),
    (72, 97, 23.0),
    (73, 26, 11.0),
    (74, 1, 24.0),
    (74, 41, 2.0),
    (74, 70, 21.0),
    (74, 83, 37.0),
    (74, 90, 31.0),
    (75, 2, 43.0),
    (75, 63, 14.0),
    (75, 73, 37.0),
    (75, 83, 8.0),
    (76, 10, 37.0),
    (76, 18, 30.0),
    (76, 20, 40.0),
    (76, 56, 5.0),
    (76, 59, 32.0),
    (76, 73, 18.0),
    (76, 89, 45.0),
    (77, 20, 9.0),
    (77, 38, 10.0),
    (77, 49, 41.0),
    (77, 89, 21.0),
    (78, 11, 7.0),
    (78, 16, 43.0),
    (78, 40, 16.0),
    (78, 69, 34.0),
    (78, 83, 22.0),
    (78, 84, 15.0),
    (78, 91, 38.0),
    (79, 5, 38.0),
    (79, 42, 42.0),
    (79, 64, 1.0),
    (79, 91, 19.0),
    (80, 34, 20.0),
    (80, 59, 27.0),
    (80, 60, 2.0),
    (80, 73, 25.0),
    (81, 38, 30.0),
    (81, 46, 33.0),
    (81, 89, 35.0),
    (81, 95, 35.0),
    (82, 27, 37.0),
    (83, 16, 26.0),
    (83, 23, 11.0),
    (83, 33, 23.0),
    (83, 38, 8.0),
    (83, 54, 1.0),
    (83, 59, 17.0),
    (83, 60, 8.0),
    (84, 5, 38.0),
    (84, 12, 45.0),
    (84, 15, 29.0),
    (84, 45, 50.0),
    (85, 0, 9.0),
    (85, 4, 22.0),
    (85, 31, 5.0),
    (86, 5, 34.0),
    (86, 61, 17.0),
    (86, 80, 36.0),
    (86, 81, 4.0),
    (86, 83, 35.0),
    (86, 84, 33.0),
    (86, 89, 41.0),
    (87, 65, 40.0),
    (87, 70, 4.0),
    (87, 72, 34.0),
    (87, 90, 5.0),
    (88, 7, 10.0),
    (88, 13, 15.0),
    (88, 37, 27.0),
    (88, 45, 12.0),
    (88, 64, 39.0),
    (88, 90, 15.0),
    (88, 96, 40.0),
    (89, 12, 46.0),
    (89, 21, 30.0),
    (89, 22, 42.0),
    (89, 81, 38.0),
    (90, 5, 10.0),
    (90, 15, 11.0),
    (90, 40, 19.0),
    (90, 46, 40.0),
    (90, 83, 28.0),
    (90, 84, 6.0),
    (91, 0, 16.0),
    (91, 13, 2.0),
    (91, 68, 44.0),
    (91, 74, 26.0),
    (91, 75, 18.0),
    (92, 20, 44.0),
    (92, 27, 1.0),
    (92, 34, 28.0),
    (92, 68, 15.0),
    (92, 88, 17.0),
    (92, 89, 40.0),
    (93, 15, 33.0),
    (93, 20, 49.0),
    (93, 36, 42.0),
    (93, 37, 3.0),
    (93, 43, 44.0),
    (93, 55, 39.0),
    (93, 59, 16.0),
    (93, 66, 23.0),
    (93, 81, 22.0),
    (93, 88, 42.0),
    (93, 90, 41.0),
    (94, 22, 30.0),
    (94, 27, 37.0),
    (94, 33, 31.0),
    (94, 45, 23.0),
    (94, 70, 42.0),
    (94, 72, 44.0),
    (94, 96, 45.0),
    (95, 2, 15.0),
    (95, 80, 20.0),
    (95, 85, 44.0),
    (95, 89, 33.0),
    (96, 61, 38.0),
    (96, 76, 16.0),
    (96, 89, 36.0),
    (96, 94, 31.0),
    (97, 11, 23.0),
    (97, 16, 32.0),
    (97, 23, 11.0),
    (97, 28, 41.0),
    (97, 38, 43.0),
    (97, 55, 2.0),
    (97, 64, 1.0),
    (98, 0, 42.0),
    (98, 16, 28.0),
    (98, 17, 22.0),
    (98, 50, 43.0),
    (98, 67, 13.0),
    (98, 75, 41.0),
    (98, 87, 7.0),
    (98, 94, 11.0),
    (99, 4, 28.0),
    (99, 6, 27.0),
    (99, 14, 17.0),
    (99, 20, 32.0),
    (99, 26, 30.0),
    (99, 48, 46.0),
    (99, 49, 2.0),
    (99, 51, 23.0),
    (99, 54, 34.0),
    (99, 78, 13.0),
    (99, 85, 38.0),
    (99, 91, 40.0),
]
