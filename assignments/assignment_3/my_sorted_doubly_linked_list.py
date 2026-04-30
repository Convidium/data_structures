"""Algorithms and Data Structures 1 AI - Linked Lists."""

from dataclasses import dataclass
import sys
from typing import Any, Iterator, Sequence, overload, override


@dataclass
class MyListNode:
    value: int
    prev_node: "MyListNode | None" = None
    next_node: "MyListNode | None" = None

class MySortedDoublyLinkedList(Sequence[int]):
    """A base class providing a doubly linked list representation."""

    @overload
    def __init__(self) -> None:
        """Initializes a new SortedDoublyLinkedList."""
        ...

    @overload
    def __init__(self, head: MyListNode, tail: MyListNode, size: int):
        """Initializes a new SortedDoublyLinkedList using predefined `head` and `tail`.

        Used for testing.
        """
        ...

    def __init__(
        self,
        head: "MyListNode | None" = None,
        tail: "MyListNode | None" = None,
        size: int = 0,
    ) -> None:
        self._head = head
        self._tail = tail
        self._size = size

    @override
    def __len__(self) -> int:
        """Return the number of elements in the list."""
        return self._size

    @override
    def __iter__(self) -> Iterator[int]:
        node = self._head
        while node:
            yield node.value
            node = node.next_node

    @override
    def __reversed__(self) -> Iterator[int]:
        node = self._tail
        while node:
            yield node.value
            node = node.prev_node

    @overload
    def __getitem__(self, index: int) -> int:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[int]:
        ...

    @override
    def __getitem__(self, index: int | slice) -> int | Sequence[int]:
        # proper implementation of Sequence interface
        if isinstance(index, slice):
            rv = []
            for idx in range(*index.indices(len(self))):
                rv.append(self[idx])
            return rv
        if isinstance(index, int) and index < 0:
            index = len(self) - index
        return self._get_value(index)

    def _get_value(self, index: int) -> int:
        """Return the value (elem) at position "index" without removing the node.

        Args:
            index (int): 0 <= index < length of list

        Returns:
            int: Retrieved value.

        Raises:
            IndexError: If the passed index out of range.
        """
        if not isinstance(index, int) or index < 0 or index >= self._size:
            raise IndexError(f"{index} is out of range.")
        if index < (self._size/2):
            current_node = self._head
            for i in range(index):
                current_node = current_node.next_node
        else:
            current_node = self._tail
            for i in range((self._size-1) - index):
                current_node = current_node.prev_node
        return current_node.value
            

    @override
    def index(self, value: Any, start: int = 0, stop: int = sys.maxsize) -> int:
        """Return the index of the first occurrence of `value` in the list.

        Args:
            val (Any): Value to be searched.
            start (int): A number representing where to start the search.
            stop (int): A number representing where to end the search.

        Raises:
            ValueError: If the given value isn't found.
            
        Returns:
            int: Retrieved index.
        """
        if not isinstance(value, int):
            raise ValueError(f"{value} is not in list.")
        
        # To avoid any further complications, here I "normalize" 
        # `start` and `stop` values here, to be in range of (0, self._size).
        if stop >= self._size: stop = self._size-1
        if start < 0: start = 0
        
        if start < self._size/2:
            current_node = self._head
            for i in range(start):
                current_node = current_node.next_node
        else:
            current_node = self._tail
            for i in range((self._size-1) - start):
                current_node = current_node.prev_node
                
        for i in range(start, stop+1):
            if current_node.value == value:
                return i
            if current_node.value > value:
                break
            current_node = current_node.next_node
            
        raise ValueError(f"{value} is not in list.")
            

    def insert(self, val: int) -> None:
        """Add a new node containing "val" to the list, keeping the list in ascending order.

        Args:
            val (int): Value to be added.

        Raises:
            TypeError: If val is not an int.
        """
        if not isinstance(val, int):
            raise TypeError(f"{val} is not an int.")
        
        new_node = MyListNode(val)
        if self._size == 0: 
            self._head = new_node
            self._tail = new_node
            self._size += 1
            return
        
        if self._head.value > val:
            new_node.next_node = self._head
            self._head.prev_node = new_node
            self._head = new_node
            self._size += 1
            return
        
        if self._tail.value < val:
            new_node.prev_node = self._tail
            self._tail.next_node = new_node
            self._tail = new_node
            self._size += 1
            return
        
        current_node = self._head.next_node
        while current_node.value <= val:
            current_node = current_node.next_node
            
        new_node.next_node = current_node
        new_node.prev_node = current_node.prev_node
        
        current_node.prev_node.next_node = new_node
        current_node.prev_node = new_node
        self._size += 1
            

    def remove(self, val: int) -> None:
        """Remove the first occurrence of the parameter "val".

        Args:
            val (int): Value to be removed.

        Raises:
            ValueError: If `val` is not present.
        """
        if not isinstance(val, int) :
            raise ValueError(f"{val} is not in list.")
        
        if self._size == 0 or val < self._head.value or val > self._tail.value:
            raise ValueError(f"{val} is not in list.")
        
        if self._size == 1:
            self._head = None
            self._tail = None
            self._size = 0
            return
        
        if val == self._head.value:
            self._head = self._head.next_node
            self._head.prev_node = None
            self._size -= 1
            return
        if val == self._tail.value:
            self._tail = self._tail.prev_node
            self._tail.next_node = None
            self._size -= 1
            return
            
        current_node = self._head
        while current_node.value < val:
            current_node = current_node.next_node
        if current_node.value == val:
            current_node.prev_node.next_node = current_node.next_node
            current_node.next_node.prev_node = current_node.prev_node
            del current_node
            self._size -= 1
        else:
            raise ValueError(f"{val} is not in list.")
        

    def remove_all(self, val: int) -> int:
        """Remove all occurrences of the parameter "val".

        Args:
            val (int): Value to be removed.

        Returns:
            int: the number of elements removed.
        """
        if not isinstance(val, int) or self._size == 0:
            return 0
        if val < self._head.value or val > self._tail.value:
            return 0
        
        # 1. We skip through elements with value less than "val"
        current_node = self._head
        while current_node is not None and current_node.value < val:
            current_node = current_node.next_node
        
        # 2. We check if the first found value is more than "val" 
        # (Since it's a sorted list, then it would mean "val" is not present in the list) 
        if current_node is None or current_node.value > val:
            return 0
        
        # 3. So it must be the one with value "val". 
        # We set it to be the first found element
        first_node = current_node
        last_node = first_node
        amount_of_nodes = 0
         
        # 4. We go further through the list to find the last element with "val"
        # And also count their amount. 
        while current_node is not None and current_node.value == val:
            if current_node.next_node is None or current_node.next_node.value != val: 
                last_node = current_node
            amount_of_nodes += 1
            current_node = current_node.next_node
            
        # 5. Find bordering elements to block of elements with "val"
        # 6. Check if they exist, and cut the pointers            
        self._remove_multiple(first_node, last_node, amount_of_nodes)
        
        return amount_of_nodes
    
    
    def remove_duplicates(self) -> None:
        """Remove all duplicate occurrences of values from the list."""
        if self._size == 0 or self._size == 1:
            return
        current_node = self._head
        while current_node is not None and current_node.next_node is not None:
            if current_node.value == current_node.next_node.value:
                first_node = current_node.next_node
                last_node = first_node
                amount_of_nodes = 1
                
                while last_node.next_node is not None and last_node.next_node.value == current_node.value:
                    last_node = last_node.next_node
                    amount_of_nodes += 1
                self._remove_multiple(first_node, last_node, amount_of_nodes)
            else:
                current_node = current_node.next_node
        

    def _remove_multiple(self, first_node: MyListNode, last_node: MyListNode, amount_of_nodes: int):
        pre_first_node = first_node.prev_node
        post_last_node = last_node.next_node
        
        if pre_first_node == None:
            self._head = post_last_node
            first_node.prev_node = None
        else: 
            pre_first_node.next_node = post_last_node
        
        if post_last_node == None:
            self._tail = pre_first_node
            last_node.next_node = None
        else: 
            post_last_node.prev_node = pre_first_node
        self._size -= amount_of_nodes
            

    def filter_n_max(self, n: int) -> None:
        """Filter the list to only contain the "n" highest values.

        Args:
            n (int): 0 < n <= length of list

        Raises:
            TypeError: If the passed value n is not an int.
            ValueError: If the passed value n is out of range.
        """
        if not isinstance(n, int):
            raise TypeError(f"{n} is not an int.")
        if n <= 0 or n > self._size:
            raise ValueError(f"{n} is out of range.")
        
        if n == self._size: return
        
        current_node = self._tail
        
        for _ in range(n - 1):
            current_node = current_node.prev_node
            
        self._head = current_node
        self._head.prev_node = None
        self._size = n
        

    def filter_odd(self) -> None:
        """Filter the list to only contain odd values."""
        current_node = self._head
        while current_node is not None:
            next_node = current_node.next_node
            if current_node.value % 2 == 0:
                self._remove_multiple(current_node, current_node, 1)
            current_node = next_node


    def filter_even(self) -> None:
        """Filter the list to only contain even values."""
        current_node = self._head
        while current_node is not None:
            next_node = current_node.next_node
            if current_node.value % 2 != 0:
                self._remove_multiple(current_node, current_node, 1)
            current_node = next_node
