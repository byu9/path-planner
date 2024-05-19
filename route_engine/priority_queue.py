from heapq import heapify, heappush, heappop


# A priority queue is just a sorted list although addition and removal are
# implemented more efficiently using the Heap Algorithm.
#
# Python standard libraries provide two implementations of a priority queue in
# the "heapq" package and the "queue.PriorityQueue" class. The latter is
# intended for multithreading. Here we need a data structure to contain some
# items, so we use "heapq" and develop a more convenient wrapper around it.


class PriorityQueue:
    __slots__ = (
        '_heap',
    )

    def __init__(self):
        self._heap = list()
        heapify(self._heap)

    def push(self, item, priority):
        """
        Inserts an item on to the queue while maintaining priority order.
        :param item: Item to insert
        :param priority: Priority associated with the item. Must support
        comparison and the lower the value the higher the priority.
        """
        heappush(self._heap, (priority, item))

    def pop(self):
        """
        Removes the item with the highest priority (smallest priority value)
        from the queue.
        :return: The item with the smallest priority value.
        """
        priority, item = heappop(self._heap)
        return item
