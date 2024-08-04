import unittest

from route_engine.graphs import MultiDiGraph
from route_engine.shortest_paths import dijkstra


class TestDijkstra(unittest.TestCase):

    def setUp(self):
        self.graph = MultiDiGraph()

        for src, dst, edge_data in _edges:
            self.graph.insert_edge(src, dst, key=1, **edge_data)

    def test1(self):
        path, distance = dijkstra(self.graph, src=69, dst=40)
        self.assertEqual(path, [
            (69, 75, 1),
            (75, 83, 1),
            (83, 23, 1),
            (23, 9, 1),
            (9, 22, 1),
            (22, 40, 1)
        ])
        self.assertAlmostEqual(distance, 81)

    def test2(self):
        path, distance = dijkstra(self.graph, src=10, dst=41)
        self.assertEqual(path, [
            (10, 98, 1),
            (98, 94, 1),
            (94, 45, 1),
            (45, 41, 1),
        ])
        self.assertAlmostEqual(distance, 44)

    def test3(self):
        path, distance = dijkstra(self.graph, src=98, dst=37)
        self.assertEqual(path, [
            (98, 87, 1),
            (87, 70, 1),
            (70, 26, 1),
            (26, 19, 1),
            (19, 92, 1),
            (92, 27, 1),
            (27, 65, 1),
            (65, 37, 1)
        ])
        self.assertAlmostEqual(distance, 54)

    def test4(self):
        path, distance = dijkstra(self.graph, src=88, dst=90)
        self.assertEqual(path, [
            (88, 90, 1),
        ])
        self.assertAlmostEqual(distance, 15)

    def test5(self):
        path, distance = dijkstra(self.graph, src=30, dst=55)
        self.assertEqual(path, [
            (30, 18, 1),
            (18, 48, 1),
            (48, 72, 1),
            (72, 97, 1),
            (97, 55, 1)
        ])
        self.assertAlmostEqual(distance, 85)

    def test6(self):
        path, distance = dijkstra(self.graph, src=32, dst=29)
        self.assertEqual(path, [
            (32, 95, 1),
            (95, 80, 1),
            (80, 34, 1),
            (34, 68, 1),
            (68, 29, 1)
        ])
        self.assertAlmostEqual(distance, 74)

    def test7(self):
        path, distance = dijkstra(self.graph, src=19, dst=22)
        self.assertEqual(path, [
            (19, 92, 1),
            (92, 27, 1),
            (27, 85, 1),
            (85, 31, 1),
            (31, 9, 1),
            (9, 22, 1)
        ])
        self.assertAlmostEqual(distance, 60)

    def test8(self):
        path, distance = dijkstra(self.graph, src=28, dst=25)
        self.assertEqual(path, [
            (28, 9, 1),
            (9, 22, 1),
            (22, 25, 1),
        ])
        self.assertAlmostEqual(distance, 57)

    def test9(self):
        path, distance = dijkstra(self.graph, src=82, dst=44)
        self.assertEqual(path, [
            (82, 27, 1),
            (27, 65, 1),
            (65, 37, 1),
            (37, 72, 1),
            (72, 44, 1)
        ])
        self.assertAlmostEqual(distance, 87)

    def test10(self):
        path, distance = dijkstra(self.graph, src=34, dst=49)
        self.assertEqual(path, [
            (34, 68, 1),
            (68, 16, 1),
            (16, 94, 1),
            (94, 45, 1),
            (45, 49, 1)
        ])
        self.assertAlmostEqual(distance, 62)


_edges = [
    (0, 3, {'distance': 43}),
    (0, 17, {'distance': 48}),
    (0, 67, {'distance': 29}),
    (0, 83, {'distance': 43}),
    (0, 97, {'distance': 35}),
    (1, 57, {'distance': 21}),
    (1, 82, {'distance': 26}),
    (2, 18, {'distance': 37}),
    (2, 37, {'distance': 4}),
    (2, 57, {'distance': 22}),
    (3, 0, {'distance': 1}),
    (3, 55, {'distance': 28}),
    (3, 86, {'distance': 20}),
    (3, 87, {'distance': 24}),
    (4, 27, {'distance': 34}),
    (4, 53, {'distance': 12}),
    (4, 72, {'distance': 1}),
    (4, 78, {'distance': 32}),
    (4, 79, {'distance': 43}),
    (5, 89, {'distance': 38}),
    (6, 3, {'distance': 18}),
    (6, 4, {'distance': 21}),
    (6, 13, {'distance': 8}),
    (6, 41, {'distance': 46}),
    (6, 44, {'distance': 37}),
    (6, 50, {'distance': 27}),
    (7, 26, {'distance': 2}),
    (7, 57, {'distance': 43}),
    (7, 68, {'distance': 20}),
    (7, 76, {'distance': 18}),
    (7, 86, {'distance': 1}),
    (8, 14, {'distance': 44}),
    (8, 37, {'distance': 24}),
    (8, 40, {'distance': 21}),
    (8, 48, {'distance': 49}),
    (8, 60, {'distance': 9}),
    (8, 73, {'distance': 9}),
    (8, 75, {'distance': 25}),
    (8, 91, {'distance': 16}),
    (9, 1, {'distance': 48}),
    (9, 5, {'distance': 45}),
    (9, 22, {'distance': 10}),
    (9, 30, {'distance': 6}),
    (9, 37, {'distance': 21}),
    (9, 38, {'distance': 38}),
    (9, 50, {'distance': 4}),
    (9, 58, {'distance': 14}),
    (9, 77, {'distance': 4}),
    (9, 84, {'distance': 39}),
    (10, 15, {'distance': 14}),
    (10, 23, {'distance': 31}),
    (10, 34, {'distance': 34}),
    (10, 48, {'distance': 16}),
    (10, 98, {'distance': 8}),
    (11, 4, {'distance': 49}),
    (11, 6, {'distance': 45}),
    (11, 16, {'distance': 18}),
    (11, 26, {'distance': 19}),
    (11, 28, {'distance': 28}),
    (11, 37, {'distance': 16}),
    (11, 57, {'distance': 43}),
    (11, 83, {'distance': 50}),
    (11, 93, {'distance': 20}),
    (12, 41, {'distance': 42}),
    (12, 56, {'distance': 46}),
    (12, 66, {'distance': 25}),
    (12, 76, {'distance': 6}),
    (12, 78, {'distance': 49}),
    (13, 48, {'distance': 26}),
    (13, 55, {'distance': 16}),
    (13, 65, {'distance': 30}),
    (14, 18, {'distance': 21}),
    (14, 31, {'distance': 36}),
    (14, 60, {'distance': 20}),
    (14, 84, {'distance': 18}),
    (14, 90, {'distance': 30}),
    (15, 8, {'distance': 22}),
    (15, 18, {'distance': 38}),
    (15, 79, {'distance': 22}),
    (15, 87, {'distance': 37}),
    (15, 88, {'distance': 45}),
    (15, 91, {'distance': 49}),
    (15, 95, {'distance': 16}),
    (16, 57, {'distance': 31}),
    (16, 94, {'distance': 1}),
    (17, 74, {'distance': 12}),
    (17, 91, {'distance': 22}),
    (18, 30, {'distance': 43}),
    (18, 48, {'distance': 15}),
    (19, 21, {'distance': 33}),
    (19, 30, {'distance': 34}),
    (19, 47, {'distance': 12}),
    (19, 76, {'distance': 24}),
    (19, 85, {'distance': 42}),
    (19, 92, {'distance': 6}),
    (20, 0, {'distance': 37}),
    (20, 12, {'distance': 45}),
    (20, 14, {'distance': 29}),
    (20, 50, {'distance': 8}),
    (20, 74, {'distance': 3}),
    (20, 87, {'distance': 17}),
    (20, 94, {'distance': 26}),
    (21, 19, {'distance': 29}),
    (21, 35, {'distance': 28}),
    (21, 67, {'distance': 2}),
    (21, 91, {'distance': 17}),
    (21, 98, {'distance': 28}),
    (22, 3, {'distance': 47}),
    (22, 18, {'distance': 43}),
    (22, 21, {'distance': 16}),
    (22, 25, {'distance': 7}),
    (22, 40, {'distance': 25}),
    (22, 47, {'distance': 8}),
    (22, 49, {'distance': 38}),
    (23, 9, {'distance': 8}),
    (23, 12, {'distance': 20}),
    (23, 16, {'distance': 33}),
    (23, 33, {'distance': 9}),
    (23, 41, {'distance': 20}),
    (23, 54, {'distance': 3}),
    (23, 56, {'distance': 3}),
    (23, 61, {'distance': 10}),
    (23, 68, {'distance': 44}),
    (23, 97, {'distance': 31}),
    (24, 22, {'distance': 47}),
    (24, 28, {'distance': 41}),
    (24, 39, {'distance': 16}),
    (24, 51, {'distance': 21}),
    (24, 78, {'distance': 46}),
    (24, 82, {'distance': 17}),
    (24, 90, {'distance': 34}),
    (25, 17, {'distance': 49}),
    (25, 46, {'distance': 47}),
    (25, 54, {'distance': 35}),
    (25, 57, {'distance': 49}),
    (25, 67, {'distance': 39}),
    (25, 89, {'distance': 26}),
    (26, 4, {'distance': 1}),
    (26, 7, {'distance': 2}),
    (26, 8, {'distance': 30}),
    (26, 19, {'distance': 10}),
    (26, 85, {'distance': 36}),
    (27, 43, {'distance': 37}),
    (27, 47, {'distance': 48}),
    (27, 65, {'distance': 12}),
    (27, 85, {'distance': 18}),
    (28, 3, {'distance': 50}),
    (28, 9, {'distance': 40}),
    (28, 19, {'distance': 13}),
    (28, 29, {'distance': 28}),
    (28, 30, {'distance': 7}),
    (28, 32, {'distance': 8}),
    (28, 36, {'distance': 5}),
    (28, 55, {'distance': 27}),
    (28, 80, {'distance': 43}),
    (28, 89, {'distance': 33}),
    (28, 92, {'distance': 24}),
    (28, 99, {'distance': 43}),
    (29, 64, {'distance': 8}),
    (29, 89, {'distance': 18}),
    (30, 10, {'distance': 50}),
    (30, 18, {'distance': 33}),
    (30, 98, {'distance': 48}),
    (31, 9, {'distance': 20}),
    (31, 65, {'distance': 11}),
    (31, 98, {'distance': 42}),
    (32, 12, {'distance': 50}),
    (32, 45, {'distance': 13}),
    (32, 64, {'distance': 15}),
    (32, 65, {'distance': 9}),
    (32, 90, {'distance': 47}),
    (32, 95, {'distance': 10}),
    (33, 36, {'distance': 46}),
    (33, 52, {'distance': 23}),
    (33, 72, {'distance': 21}),
    (33, 82, {'distance': 48}),
    (33, 87, {'distance': 17}),
    (34, 68, {'distance': 1}),
    (34, 70, {'distance': 32}),
    (34, 78, {'distance': 49}),
    (35, 12, {'distance': 26}),
    (35, 32, {'distance': 17}),
    (35, 50, {'distance': 17}),
    (36, 32, {'distance': 46}),
    (36, 58, {'distance': 40}),
    (36, 68, {'distance': 41}),
    (36, 71, {'distance': 21}),
    (36, 76, {'distance': 28}),
    (36, 82, {'distance': 30}),
    (37, 17, {'distance': 3}),
    (37, 48, {'distance': 43}),
    (37, 53, {'distance': 19}),
    (37, 54, {'distance': 11}),
    (37, 72, {'distance': 8}),
    (37, 87, {'distance': 32}),
    (38, 36, {'distance': 3}),
    (38, 55, {'distance': 39}),
    (38, 58, {'distance': 44}),
    (38, 65, {'distance': 18}),
    (39, 31, {'distance': 42}),
    (39, 91, {'distance': 15}),
    (39, 94, {'distance': 12}),
    (40, 30, {'distance': 8}),
    (40, 65, {'distance': 34}),
    (40, 89, {'distance': 33}),
    (41, 17, {'distance': 46}),
    (41, 72, {'distance': 42}),
    (41, 82, {'distance': 39}),
    (41, 87, {'distance': 14}),
    (41, 91, {'distance': 2}),
    (41, 95, {'distance': 24}),
    (42, 23, {'distance': 38}),
    (42, 32, {'distance': 31}),
    (42, 50, {'distance': 38}),
    (43, 22, {'distance': 29}),
    (43, 58, {'distance': 3}),
    (43, 67, {'distance': 4}),
    (43, 68, {'distance': 43}),
    (43, 74, {'distance': 5}),
    (43, 77, {'distance': 11}),
    (43, 94, {'distance': 12}),
    (44, 16, {'distance': 30}),
    (44, 21, {'distance': 5}),
    (44, 39, {'distance': 31}),
    (44, 55, {'distance': 13}),
    (44, 70, {'distance': 13}),
    (44, 84, {'distance': 15}),
    (45, 15, {'distance': 27}),
    (45, 41, {'distance': 2}),
    (45, 49, {'distance': 17}),
    (45, 80, {'distance': 17}),
    (45, 82, {'distance': 40}),
    (46, 14, {'distance': 33}),
    (46, 22, {'distance': 49}),
    (46, 33, {'distance': 28}),
    (46, 66, {'distance': 25}),
    (46, 72, {'distance': 5}),
    (46, 85, {'distance': 19}),
    (46, 87, {'distance': 45}),
    (47, 19, {'distance': 43}),
    (48, 7, {'distance': 35}),
    (48, 35, {'distance': 12}),
    (48, 64, {'distance': 39}),
    (48, 68, {'distance': 9}),
    (48, 72, {'distance': 12}),
    (48, 87, {'distance': 33}),
    (49, 4, {'distance': 5}),
    (49, 25, {'distance': 24}),
    (49, 27, {'distance': 11}),
    (49, 82, {'distance': 6}),
    (49, 93, {'distance': 27}),
    (50, 12, {'distance': 20}),
    (50, 30, {'distance': 37}),
    (51, 15, {'distance': 22}),
    (51, 24, {'distance': 19}),
    (51, 29, {'distance': 32}),
    (51, 76, {'distance': 21}),
    (52, 10, {'distance': 28}),
    (52, 12, {'distance': 39}),
    (52, 33, {'distance': 44}),
    (52, 57, {'distance': 22}),
    (52, 63, {'distance': 15}),
    (52, 77, {'distance': 14}),
    (52, 81, {'distance': 17}),
    (52, 90, {'distance': 8}),
    (53, 15, {'distance': 22}),
    (53, 27, {'distance': 35}),
    (53, 31, {'distance': 21}),
    (53, 66, {'distance': 40}),
    (53, 70, {'distance': 26}),
    (53, 74, {'distance': 25}),
    (53, 84, {'distance': 41}),
    (54, 67, {'distance': 43}),
    (55, 17, {'distance': 6}),
    (55, 62, {'distance': 38}),
    (55, 84, {'distance': 47}),
    (55, 92, {'distance': 47}),
    (55, 97, {'distance': 9}),
    (56, 45, {'distance': 46}),
    (56, 76, {'distance': 10}),
    (56, 81, {'distance': 15}),
    (57, 11, {'distance': 26}),
    (57, 42, {'distance': 48}),
    (57, 98, {'distance': 41}),
    (58, 9, {'distance': 16}),
    (58, 11, {'distance': 38}),
    (58, 41, {'distance': 5}),
    (58, 42, {'distance': 38}),
    (58, 54, {'distance': 13}),
    (58, 57, {'distance': 25}),
    (58, 63, {'distance': 8}),
    (59, 30, {'distance': 30}),
    (59, 38, {'distance': 13}),
    (59, 46, {'distance': 2}),
    (59, 53, {'distance': 6}),
    (59, 57, {'distance': 34}),
    (59, 62, {'distance': 1}),
    (59, 70, {'distance': 45}),
    (59, 91, {'distance': 3}),
    (60, 51, {'distance': 36}),
    (60, 69, {'distance': 1}),
    (61, 28, {'distance': 15}),
    (61, 34, {'distance': 4}),
    (61, 54, {'distance': 38}),
    (61, 74, {'distance': 14}),
    (61, 77, {'distance': 20}),
    (61, 82, {'distance': 1}),
    (61, 85, {'distance': 5}),
    (62, 3, {'distance': 44}),
    (62, 22, {'distance': 26}),
    (62, 25, {'distance': 35}),
    (62, 47, {'distance': 15}),
    (62, 59, {'distance': 21}),
    (63, 15, {'distance': 50}),
    (63, 58, {'distance': 34}),
    (63, 85, {'distance': 45}),
    (64, 92, {'distance': 25}),
    (64, 95, {'distance': 41}),
    (65, 31, {'distance': 48}),
    (65, 37, {'distance': 11}),
    (65, 91, {'distance': 17}),
    (66, 12, {'distance': 38}),
    (66, 28, {'distance': 41}),
    (66, 49, {'distance': 48}),
    (67, 4, {'distance': 25}),
    (67, 12, {'distance': 7}),
    (67, 19, {'distance': 49}),
    (67, 44, {'distance': 49}),
    (67, 48, {'distance': 27}),
    (67, 51, {'distance': 8}),
    (67, 85, {'distance': 44}),
    (68, 16, {'distance': 20}),
    (68, 29, {'distance': 23}),
    (68, 32, {'distance': 40}),
    (68, 44, {'distance': 21}),
    (69, 20, {'distance': 46}),
    (69, 75, {'distance': 19}),
    (69, 82, {'distance': 41}),
    (70, 26, {'distance': 3}),
    (70, 51, {'distance': 41}),
    (70, 78, {'distance': 50}),
    (71, 2, {'distance': 47}),
    (71, 4, {'distance': 32}),
    (71, 9, {'distance': 20}),
    (71, 15, {'distance': 25}),
    (71, 20, {'distance': 25}),
    (71, 23, {'distance': 42}),
    (71, 28, {'distance': 22}),
    (71, 40, {'distance': 39}),
    (71, 77, {'distance': 41}),
    (72, 44, {'distance': 19}),
    (72, 45, {'distance': 25}),
    (72, 73, {'distance': 46}),
    (72, 97, {'distance': 23}),
    (73, 26, {'distance': 11}),
    (74, 1, {'distance': 24}),
    (74, 41, {'distance': 2}),
    (74, 70, {'distance': 21}),
    (74, 83, {'distance': 37}),
    (74, 90, {'distance': 31}),
    (75, 2, {'distance': 43}),
    (75, 63, {'distance': 14}),
    (75, 73, {'distance': 37}),
    (75, 83, {'distance': 8}),
    (76, 10, {'distance': 37}),
    (76, 18, {'distance': 30}),
    (76, 20, {'distance': 40}),
    (76, 56, {'distance': 5}),
    (76, 59, {'distance': 32}),
    (76, 73, {'distance': 18}),
    (76, 89, {'distance': 45}),
    (77, 20, {'distance': 9}),
    (77, 38, {'distance': 10}),
    (77, 49, {'distance': 41}),
    (77, 89, {'distance': 21}),
    (78, 11, {'distance': 7}),
    (78, 16, {'distance': 43}),
    (78, 40, {'distance': 16}),
    (78, 69, {'distance': 34}),
    (78, 83, {'distance': 22}),
    (78, 84, {'distance': 15}),
    (78, 91, {'distance': 38}),
    (79, 5, {'distance': 38}),
    (79, 42, {'distance': 42}),
    (79, 64, {'distance': 1}),
    (79, 91, {'distance': 19}),
    (80, 34, {'distance': 20}),
    (80, 59, {'distance': 27}),
    (80, 60, {'distance': 2}),
    (80, 73, {'distance': 25}),
    (81, 38, {'distance': 30}),
    (81, 46, {'distance': 33}),
    (81, 89, {'distance': 35}),
    (81, 95, {'distance': 35}),
    (82, 27, {'distance': 37}),
    (83, 16, {'distance': 26}),
    (83, 23, {'distance': 11}),
    (83, 33, {'distance': 23}),
    (83, 38, {'distance': 8}),
    (83, 54, {'distance': 1}),
    (83, 59, {'distance': 17}),
    (83, 60, {'distance': 8}),
    (84, 5, {'distance': 38}),
    (84, 12, {'distance': 45}),
    (84, 15, {'distance': 29}),
    (84, 45, {'distance': 50}),
    (85, 0, {'distance': 9}),
    (85, 4, {'distance': 22}),
    (85, 31, {'distance': 5}),
    (86, 5, {'distance': 34}),
    (86, 61, {'distance': 17}),
    (86, 80, {'distance': 36}),
    (86, 81, {'distance': 4}),
    (86, 83, {'distance': 35}),
    (86, 84, {'distance': 33}),
    (86, 89, {'distance': 41}),
    (87, 65, {'distance': 40}),
    (87, 70, {'distance': 4}),
    (87, 72, {'distance': 34}),
    (87, 90, {'distance': 5}),
    (88, 7, {'distance': 10}),
    (88, 13, {'distance': 15}),
    (88, 37, {'distance': 27}),
    (88, 45, {'distance': 12}),
    (88, 64, {'distance': 39}),
    (88, 90, {'distance': 15}),
    (88, 96, {'distance': 40}),
    (89, 12, {'distance': 46}),
    (89, 21, {'distance': 30}),
    (89, 22, {'distance': 42}),
    (89, 81, {'distance': 38}),
    (90, 5, {'distance': 10}),
    (90, 15, {'distance': 11}),
    (90, 40, {'distance': 19}),
    (90, 46, {'distance': 40}),
    (90, 83, {'distance': 28}),
    (90, 84, {'distance': 6}),
    (91, 0, {'distance': 16}),
    (91, 13, {'distance': 2}),
    (91, 68, {'distance': 44}),
    (91, 74, {'distance': 26}),
    (91, 75, {'distance': 18}),
    (92, 20, {'distance': 44}),
    (92, 27, {'distance': 1}),
    (92, 34, {'distance': 28}),
    (92, 68, {'distance': 15}),
    (92, 88, {'distance': 17}),
    (92, 89, {'distance': 40}),
    (93, 15, {'distance': 33}),
    (93, 20, {'distance': 49}),
    (93, 36, {'distance': 42}),
    (93, 37, {'distance': 3}),
    (93, 43, {'distance': 44}),
    (93, 55, {'distance': 39}),
    (93, 59, {'distance': 16}),
    (93, 66, {'distance': 23}),
    (93, 81, {'distance': 22}),
    (93, 88, {'distance': 42}),
    (93, 90, {'distance': 41}),
    (94, 22, {'distance': 30}),
    (94, 27, {'distance': 37}),
    (94, 33, {'distance': 31}),
    (94, 45, {'distance': 23}),
    (94, 70, {'distance': 42}),
    (94, 72, {'distance': 44}),
    (94, 96, {'distance': 45}),
    (95, 2, {'distance': 15}),
    (95, 80, {'distance': 20}),
    (95, 85, {'distance': 44}),
    (95, 89, {'distance': 33}),
    (96, 61, {'distance': 38}),
    (96, 76, {'distance': 16}),
    (96, 89, {'distance': 36}),
    (96, 94, {'distance': 31}),
    (97, 11, {'distance': 23}),
    (97, 16, {'distance': 32}),
    (97, 23, {'distance': 11}),
    (97, 28, {'distance': 41}),
    (97, 38, {'distance': 43}),
    (97, 55, {'distance': 2}),
    (97, 64, {'distance': 1}),
    (98, 0, {'distance': 42}),
    (98, 16, {'distance': 28}),
    (98, 17, {'distance': 22}),
    (98, 50, {'distance': 43}),
    (98, 67, {'distance': 13}),
    (98, 75, {'distance': 41}),
    (98, 87, {'distance': 7}),
    (98, 94, {'distance': 11}),
    (99, 4, {'distance': 28}),
    (99, 6, {'distance': 27}),
    (99, 14, {'distance': 17}),
    (99, 20, {'distance': 32}),
    (99, 26, {'distance': 30}),
    (99, 48, {'distance': 46}),
    (99, 49, {'distance': 2}),
    (99, 51, {'distance': 23}),
    (99, 54, {'distance': 34}),
    (99, 78, {'distance': 13}),
    (99, 85, {'distance': 38}),
    (99, 91, {'distance': 40}),
]
