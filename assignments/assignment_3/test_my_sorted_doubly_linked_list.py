"""Unit tests for Algorithms and Data Structures 1 AI - Linked Lists."""

import sys

import pytest
from my_sorted_doubly_linked_list import MyListNode, MySortedDoublyLinkedList


def create_list_from_array(arr: list[int]) -> MySortedDoublyLinkedList:
    """Helper function to create a linked-list from an list."""
    if len(arr) == 0:
        return MySortedDoublyLinkedList()

    head = MyListNode(arr[0])
    old_node = head
    for i in range(1, len(arr)):
        new_node = MyListNode(arr[i])
        new_node.prev_node = old_node
        old_node.next_node = new_node
        old_node = new_node
    return MySortedDoublyLinkedList(head, old_node, len(arr))


try:
    from conftest import points  # type: ignore
except ImportError:

    def points(points: float):
        return lambda function: function


# Fixtures
@pytest.fixture
def empty_dll() -> MySortedDoublyLinkedList:
    return create_list_from_array([])


@pytest.fixture
def sorted_dll() -> MySortedDoublyLinkedList:
    return create_list_from_array([1, 2, 3, 4])


@pytest.fixture
def arr_fib() -> list[int]:
    return [1, 1, 2, 3, 5, 8, 13, 21]


@pytest.fixture
def arr_even() -> list[int]:
    return [-2, -2, -2, 0, 2, 2, 4, 6, 8, 8]


@pytest.fixture
def arr_odd() -> list[int]:
    return [-1, 1, 1, 1, 3, 3, 5, 7, 9]


@points(0)
def test_python_version():
    assert sys.version_info >= (3, 13), \
        f"Python version is too low. Required >=3.13, your version: {sys.version_info.major}.{sys.version_info.minor}"


# Test cases
@points(1.0)
def test_get_value(sorted_dll: MySortedDoublyLinkedList):
    assert sorted_dll[0] == 1
    assert sorted_dll[1] == 2
    assert sorted_dll[2] == 3
    assert sorted_dll[3] == 4


@points(0.25)
def test_invalid_get_value(
    empty_dll: MySortedDoublyLinkedList, sorted_dll: MySortedDoublyLinkedList
):
    with pytest.raises(IndexError):
        empty_dll[0]
    with pytest.raises(IndexError):
        sorted_dll[-1]
    with pytest.raises(IndexError):
        sorted_dll[4]


@points(0.75)
def test_index(sorted_dll: MySortedDoublyLinkedList):
    assert sorted_dll.index(1) == 0
    assert sorted_dll.index(2) == 1
    assert sorted_dll.index(3) == 2
    assert sorted_dll.index(4) == 3


@points(0.25)
def test_invalid_index(
    empty_dll: MySortedDoublyLinkedList, sorted_dll: MySortedDoublyLinkedList
):
    with pytest.raises(ValueError):
        empty_dll.index(0)
    with pytest.raises(ValueError):
        sorted_dll.index(0)
    with pytest.raises(ValueError):
        sorted_dll.index(5)


@points(0.5)
def test_index_with_start_stop_args(arr_even: list[int]):
    l = create_list_from_array(arr_even)

    assert l.index(-2) == 0
    assert l.index(-2, 2) == 2
    assert l.index(8) == 8
    with pytest.raises(ValueError):
        l.index(8, 0, 7)

    with pytest.raises(ValueError):
        l.index(-2, 3)


@points(2.0)
def test_insert(
    empty_dll: MySortedDoublyLinkedList, sorted_dll: MySortedDoublyLinkedList
):
    empty_dll.insert(0)
    assert list(empty_dll) == [0]

    sorted_dll.insert(3)
    assert list(sorted_dll) == [1, 2, 3, 3, 4]

    sorted_dll.insert(5)
    assert list(sorted_dll) == [1, 2, 3, 3, 4, 5]

    sorted_dll.insert(0)
    assert list(sorted_dll) == [0, 1, 2, 3, 3, 4, 5]


@points(0.25)
def test_invalid_insert(sorted_dll: MySortedDoublyLinkedList):
    with pytest.raises(TypeError):
        sorted_dll.insert(2.5)  # type: ignore
    with pytest.raises(TypeError):
        sorted_dll.insert("a")  # type: ignore


@points(2.0)
def test_remove(sorted_dll: MySortedDoublyLinkedList):
    sorted_dll.remove(3)
    assert list(sorted_dll) == [1, 2, 4]
    assert len(sorted_dll) == 3
    sorted_dll.remove(4)
    assert list(sorted_dll) == [1, 2]
    assert len(sorted_dll) == 2
    sorted_dll.remove(1)
    assert list(sorted_dll) == [2]
    assert len(sorted_dll) == 1


@points(0.25)
def test_remove_invalid_value(
    empty_dll: MySortedDoublyLinkedList, sorted_dll: MySortedDoublyLinkedList
):
    with pytest.raises(ValueError):
        empty_dll.remove(0)
    with pytest.raises(ValueError):
        sorted_dll.remove(5)
    with pytest.raises(ValueError):
        sorted_dll.remove(2.5)  # type: ignore
    with pytest.raises(ValueError):
        sorted_dll.remove("a")  # type: ignore
    assert list(sorted_dll) == [1, 2, 3, 4]
    assert len(sorted_dll) == 4


@points(2.0)
def test_remove_all(arr_even: list[int]):
    sorted_dll = create_list_from_array(arr_even)
    assert sorted_dll.remove_all(2) == 2
    assert list(sorted_dll) == [-2, -2, -2, 0, 4, 6, 8, 8]
    assert len(sorted_dll) == 8

    assert sorted_dll.remove_all(8) == 2
    assert list(sorted_dll) == [-2, -2, -2, 0, 4, 6]
    assert len(sorted_dll) == 6

    assert sorted_dll.remove_all(-2) == 3
    assert list(sorted_dll) == [0, 4, 6]
    assert len(sorted_dll) == 3

    assert sorted_dll.remove_all(4) == 1
    assert list(sorted_dll) == [0, 6]
    assert len(sorted_dll) == 2


@points(0.5)
def test_no_remove_all(
    empty_dll: MySortedDoublyLinkedList, sorted_dll: MySortedDoublyLinkedList
):
    assert empty_dll.remove_all(0) == 0
    assert sorted_dll.remove_all(5) == 0
    assert list(sorted_dll) == [1, 2, 3, 4]

    assert sorted_dll.remove_all(2.5) == 0  # type: ignore
    assert sorted_dll.remove_all("a") == 0  # type: ignore
    assert len(sorted_dll) == 4


@points(2.0)
def test_remove_duplicates(
    empty_dll: MySortedDoublyLinkedList,
    sorted_dll: MySortedDoublyLinkedList,
    arr_fib: list[int],
    arr_even: list[int],
    arr_odd: list[int],
):
    empty_dll.remove_duplicates()
    assert list(empty_dll) == []

    sorted_dll.remove_duplicates()
    assert list(sorted_dll) == [1, 2, 3, 4]

    sorted_dll = create_list_from_array(arr_fib)
    sorted_dll.remove_duplicates()
    assert list(sorted_dll) == [1, 2, 3, 5, 8, 13, 21]

    sorted_dll = create_list_from_array(arr_even)
    sorted_dll.remove_duplicates()
    assert list(sorted_dll) == [
        -2,
        0,
        2,
        4,
        6,
        8,
    ]
    assert len(sorted_dll) == 6
    sorted_dll = create_list_from_array(arr_odd)
    sorted_dll.remove_duplicates()
    assert list(sorted_dll) == [
        -1,
        1,
        3,
        5,
        7,
        9,
    ]
    assert len(sorted_dll) == 6


@points(1.5)
def test_filter_n_max(
    sorted_dll: MySortedDoublyLinkedList,
    arr_fib: list[int],
    arr_even: list[int],
    arr_odd: list[int],
):
    sorted_dll.filter_n_max(4)
    assert list(sorted_dll) == [1, 2, 3, 4]
    assert len(sorted_dll) == 4
    sorted_dll.filter_n_max(3)
    assert list(sorted_dll) == [2, 3, 4]
    assert len(sorted_dll) == 3
    sorted_dll.filter_n_max(2)
    assert list(sorted_dll) == [3, 4]
    assert len(sorted_dll) == 2
    sorted_dll.filter_n_max(1)
    assert list(sorted_dll) == [4]
    assert len(sorted_dll) == 1
    sorted_dll = create_list_from_array(arr_fib)
    sorted_dll.filter_n_max(8)
    assert list(sorted_dll) == [
        1,
        1,
        2,
        3,
        5,
        8,
        13,
        21,
    ]
    assert len(sorted_dll) == 8
    sorted_dll = create_list_from_array(arr_even)
    sorted_dll.filter_n_max(2)
    assert list(sorted_dll) == [8, 8]
    assert len(sorted_dll) == 2
    sorted_dll = create_list_from_array(arr_odd)
    sorted_dll.filter_n_max(1)
    assert list(sorted_dll) == [9]
    assert len(sorted_dll) == 1


@points(0.25)
def test_invalid_filter_n_max(
    empty_dll: MySortedDoublyLinkedList, sorted_dll: MySortedDoublyLinkedList
):
    with pytest.raises(ValueError):
        empty_dll.filter_n_max(1)
    with pytest.raises(ValueError):
        sorted_dll.filter_n_max(0)
    with pytest.raises(ValueError):
        sorted_dll.filter_n_max(5)
    with pytest.raises(TypeError):
        sorted_dll.filter_n_max(2.5)  # type: ignore
    with pytest.raises(TypeError):
        sorted_dll.filter_n_max("a")  # type: ignore


@points(1.25)
def test_filter_odd(
    empty_dll: MySortedDoublyLinkedList,
    sorted_dll: MySortedDoublyLinkedList,
    arr_fib: list[int],
    arr_even: list[int],
    arr_odd: list[int],
):
    empty_dll.filter_odd()
    assert list(empty_dll) == []
    assert len(empty_dll) == 0

    sorted_dll.filter_odd()
    assert list(sorted_dll) == [1, 3]
    assert len(sorted_dll) == 2
    
    sorted_dll = create_list_from_array(arr_fib)
    sorted_dll.filter_odd()
    assert list(sorted_dll) == [1, 1, 3, 5, 13, 21]
    assert len(sorted_dll) == 6

    sorted_dll = create_list_from_array(arr_even)
    sorted_dll.filter_odd()
    assert list(sorted_dll) == []
    assert len(sorted_dll) == 0

    sorted_dll = create_list_from_array(arr_odd)
    sorted_dll.filter_odd()
    assert list(sorted_dll) == arr_odd
    assert len(sorted_dll) == len(arr_odd)

@points(1.25)
def test_filter_even(
    empty_dll: MySortedDoublyLinkedList,
    sorted_dll: MySortedDoublyLinkedList,
    arr_fib: list[int],
    arr_even: list[int],
    arr_odd: list[int],
):
    empty_dll.filter_even()
    assert list(empty_dll) == []
    assert len(empty_dll) == 0

    sorted_dll.filter_even()
    assert list(sorted_dll) == [2, 4]
    assert len(sorted_dll) == 2
    
    sorted_dll = create_list_from_array(arr_fib)
    sorted_dll.filter_even()
    assert list(sorted_dll) == [2, 8]
    assert len(sorted_dll) == 2

    sorted_dll = create_list_from_array(arr_odd)
    sorted_dll.filter_even()
    assert list(sorted_dll) == []
    assert len(sorted_dll) == 0

    sorted_dll = create_list_from_array(arr_even)
    sorted_dll.filter_even()
    assert list(sorted_dll) == arr_even
    assert len(sorted_dll) == len(arr_even)

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
