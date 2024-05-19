from unittest import TestCase
from ..priority_queue import PriorityQueue


class TestPriorityQueue(TestCase):

    def test1(self):
        items = [5, 2, 3, 1, 6]

        queue = PriorityQueue()
        for item in items:
            queue.push(item, priority=item)

        popped_items = [
            queue.pop()
            for _ in range(len(items))
        ]

        self.assertListEqual(popped_items, sorted(items))
