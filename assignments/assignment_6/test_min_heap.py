"""Unit tests fo Algorithms and Data Structures 1 AI - Queue and heaps."""
import random
import sys

import pytest

from min_heap import MinHeap

try:
    from conftest import points  # type: ignore
except ImportError:

    def points(points: float):
        return lambda function: function


@points(0)
def test_python_version():
    assert sys.version_info >= (3, 13), \
        f"Python version is too low. Required >=3.13, your version: {sys.version_info.major}.{sys.version_info.minor}"


@points(0.5)
def test_heap_insert_with_one_element():
    heap = MinHeap()
    heap.push(0)
    assert heap.container == [0]

@points(0.75)
def test_heap_insert_without_upheap():
    heap = MinHeap()
    for i in [0, 1, 2]:
        heap.push(i)
    assert heap.container == [0, 1, 2]

@points(0.75)
def test_heap_insert_with_upheap_of_middle_element():
    heap = MinHeap()
    for i in [1, 0, 2]:
        heap.push(i)
    assert heap.container == [0, 1, 2]

@points(0.75)
def test_heap_insert_with_upheap_of_last_element():
    heap = MinHeap()
    for i in [1, 2, 0]:
        heap.push(i)
    assert heap.container == [0, 2, 1]

@points(1)
def test_heap_insert_with_multiple_upheap():
    heap = MinHeap()
    for i in [5, 4, 3, 2, 1, 0]:
        heap.push(i)
    assert heap.container == [0, 2, 1, 5, 3, 4]

@points(0.75)
def test_heap_insert_complex():
    heap = MinHeap()
    for item, expected_order in (
        (3, [3]),
        (7, [3, 7]),
        (2, [2, 7, 3]),
        (5, [2, 5, 3, 7]),
        (1, [1, 2, 3, 7, 5]),
        (0, [0, 2, 1, 7, 5, 3]),
        (6, [0, 2, 1, 7, 5, 3, 6]),
        (4, [0, 2, 1, 4, 5, 3, 6, 7]),
        (9, [0, 2, 1, 4, 5, 3, 6, 7, 9]),
        (8, [0, 2, 1, 4, 5, 3, 6, 7, 9, 8])
    ):
        heap.push(item)
        assert heap.container == expected_order

@points(0.5)
def test_heap_big_insert():
    heap = MinHeap()
    vals = list(range(128))
    random.Random(42).shuffle(vals)
    for i in vals:
        heap.push(i)
    assert heap.container == [
        0, 1, 2, 8, 5, 16, 3, 10, 9, 18, 12, 22, 21,
        6, 4, 28, 24, 39, 15, 38, 19, 43, 20, 42, 25,
        23, 27, 7, 32, 14, 13, 60, 63, 46, 34, 59,
        58, 33, 44, 45, 48, 74, 49, 47, 84, 41, 66,
        57, 53, 80, 36, 71, 64, 29, 40, 54, 11, 69,
        67, 26, 17, 35, 31, 98, 107, 117, 101, 92,
        73, 95, 37, 123, 81, 96, 68, 104, 50, 105,
        72, 82, 51, 61, 109, 119, 88, 111, 108, 93,
        76, 112, 99, 78, 56, 124, 113, 102, 122, 100,
        115, 89, 83, 91, 52, 85, 110, 77, 70, 97, 30,
        116, 126, 118, 106, 121, 75, 87, 114, 120,
        86, 79, 125, 55, 127, 90, 62, 94, 65, 103
    ]

@points(0.5)
def test_heap_is_empty():
    heap = MinHeap()
    assert heap.is_empty() is True

    heap.push(1)
    assert heap.is_empty() is False
    heap.pop()
    assert heap.is_empty() is True

@points(1)
def test_heap_get_min():
    heap = MinHeap([0])
    assert heap.peek() == 0

@points(1)
def test_heap_get_min_with_multiple_elements():
    heap = MinHeap([0, 1, 2, 3, 4])
    assert heap.peek() == 0

@points(0.5)
def test_heap_get_min_empty_heap():
    heap = MinHeap()
    with pytest.raises(RuntimeError):
        heap.peek()

@points(1)
def test_heap_pop_last_element():
    heap = MinHeap([0])
    assert heap.pop() == 0
    assert heap.container == []
    with pytest.raises(RuntimeError):
        heap.pop()

@points(1)
def test_heap_pop_without_downheap():
    heap = MinHeap([0, 2, 1])
    assert heap.pop() == 0
    assert heap.container == [1, 2]
    assert heap.pop() == 1
    assert heap.container == [2]

@points(1)
def test_heap_pop_with_downheap():
    heap = MinHeap([0, 1, 2, 3, 4])
    assert heap.pop() == 0
    assert heap.container == [1, 3, 2, 4]
    assert heap.pop() == 1
    assert heap.container == [2, 3, 4]
    assert heap.pop() == 2
    assert heap.container == [3, 4]
    assert heap.pop() == 3
    assert heap.container == [4]

@points(1)
def test_heap_size_with_insert_and_remove():
    heap = MinHeap()
    assert len(heap) == 0
    heap.push(2)
    assert len(heap) == 1
    heap.push(2)
    assert len(heap) == 2
    heap.pop()
    assert len(heap) == 1
    heap.pop()
    assert len(heap) == 0


if __name__ == "__main__":
    try:
        import pytest_timeout

        pytest_timeout_installed = True
        del sys.modules["pytest_timeout"]
    except ModuleNotFoundError:
        print(
            "Consider installing pytest-timeout to execute all tests even if some test hangs."
        )
        pytest_timeout_installed = False

    if pytest_timeout_installed:
        pytest.main([__file__, "-rA", "--timeout=2"])
    else:
        pytest.main([__file__, "-rA"])