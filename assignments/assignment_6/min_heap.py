"""Algorithms and Data Structures 1 AI - Queue and Heaps."""

from typing import Collection, Iterator, override


class MinHeap(Collection[int]):
    """A priority queue implementation using a min heap."""

    def __init__(self, raw_heap: list[int] | None = None):
        """Initializes a new min heap, with an optional heap array to use as a basis.

        Args:
            raw_heap (list[int] | None): A already populated heap or None. Used for testing.
        """
        self._heap: list[int] = raw_heap or []

    @property
    def container(self) -> "list[int]":
        """Returns the underlying storage container used in the heap."""
        return self._heap


    def is_empty(self) -> bool:
        """True if the min heap is empty, False otherwise."""
        if len(self._heap) == 0: return True
        return False

    def push(self, val: int) -> None:
        """Inserts the given value into the min heap."""
        self._heap.append(val)
        self._heapify_up(len(self._heap)-1)

    def peek(self) -> int:
        """Returns the minimum element of the heap without removing it.
        
        Raises:
            RuntimeError: if the heap is empty.
        """
        if self.is_empty(): raise RuntimeError
        return self._heap[0]

    def pop(self) -> int:
        """Removes the minimum element of the heap and returns it.

        Raises:
            RuntimeError: if the heap is empty.
        """
        if self.is_empty(): raise RuntimeError
        root_element = self._heap[0]
        self._heap[0] = self._heap[len(self._heap)-1]
        self._heap.pop()
        self._heapify_down(0)
        return root_element
    
    def _heapify_up(self, index: int) -> None:
        parent_index = int((index-1)/2)
        if index > 0 and self._heap[parent_index] > self._heap[index]:
            self._heap[index], self._heap[parent_index] = self._heap[parent_index], self._heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index: int) -> None:
        current = index
        left_child_index = 2*index + 1
        right_child_index = 2*index + 2
        heap_Length = len(self._heap)

        if left_child_index < heap_Length and  self._heap[left_child_index] < self._heap[current]:
            current = left_child_index
        
        if right_child_index < heap_Length and  self._heap[right_child_index] < self._heap[current]:
            current = right_child_index

        if current != index:
            self._heap[index], self._heap[current] = self._heap[current], self._heap[index]
            self._heapify_down(current)

    
    @override
    def __len__(self) -> int:
        """The number of elements in the min heap."""
        return len(self._heap)
    
    @override
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.container})"
    
    @override
    def __contains__(self, x: object) -> bool:
        return x in self._heap
    
    @override
    def __iter__(self) -> Iterator[int]:
        return iter(self._heap)
