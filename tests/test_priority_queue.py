from unittest import TestCase
from route_engine.priority_queue import PriorityQueue


class TestPriorityQueue(TestCase):

    def test1(self):
        items = [5, 2, 3, 1, 6]

        queue = PriorityQueue()
        for item in items:
            queue.push(item, priority=item)

        popped_items = list()
        while queue:
            popped_items.append(queue.pop())

        self.assertListEqual(popped_items, sorted(items))
