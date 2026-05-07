"""Algorithms and Data Structures 1 AI - Binary Search Trees."""

import contextlib
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, MutableMapping, overload, override

@dataclass
class TreeNode:
    """TreeNode helper class.

    Attributes:
        key (int): Key used for sorting the node into a BST.
        value (Any): Whatever data the node shall carry.
        right (TreeNode): Node to the right.
        left (TreeNode): Node to the left.
        parent (TreeNode): Parent node.
    """

    key: int
    value: Any
    _right: "TreeNode | None" = field(default=None, init=False, repr=False)
    _left: "TreeNode | None" = field(default=None, init=False, repr=False)
    _parent: "TreeNode | None" = field(default=None, init=False, repr=False, compare=False)

    @property
    def right(self) -> "TreeNode | None":
        """Return the right child of this node if existing."""
        return self._right
    
    @right.setter
    def right(self, value: "TreeNode | None"):
        """Set the right child of this node."""
        # NOTE: You may want to additionally update the parent field of the current child 
        # and future child accordingly and avoid ever setting 'parent' explicitly.
        self._right = value

    @property
    def left(self) -> "TreeNode | None":
        """Return the left child of this node if existing."""
        return self._left

    @left.setter
    def left(self, value: "TreeNode | None"):
        """Set the left child of this node."""
        # NOTE: You may want to additionally update the parent field of the current child 
        # and future child accordingly and avoid ever setting 'parent' explicitly.
        self._left = value

    @property
    def parent(self) -> "TreeNode | None":
        """Returns the parent of this node or 'None' if this is a root node."""
        return self._parent

    @parent.setter
    def parent(self, value: "TreeNode | None"):
        """Set the parent of this node."""
        # NOTE: *You may delete this setter* and automatically set '_parent' whenever this node
        # is being set as the left/right node of some other node.
        # This could make your life easier, ensuring that 'node.left.parent == node' all the time.
        self._parent = value
     
    def overwrite_parent(self, new_parent: "TreeNode | None"):
        """Force-set the parent of this node."""
        # This method is used in testing to ensure we can provide you a valid tree.
        self._parent = new_parent

    @property
    def depth(self) -> int:
        """Return depth of the node, i.e. the number of parents/grandparents etc.

        Returns:
            int: Depth of node
        """
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @property
    def is_external(self) -> bool:
        """Return if node is an external node (= leaf)."""
        return self.left is None and self.right is None

    @property
    def is_internal(self) -> bool:
        """Return if node is an internal node."""
        return not self.is_external



class BinarySearchTree(MutableMapping[int, Any]):
    """Binary-Search-Tree implemented for didactic reasons."""

    @overload
    def __init__(self):
        """Initialize BinarySearchTree."""
        ...

    @overload
    def __init__(self, root: "TreeNode", size: int):
        """Initializes a BinarySearchTree already filled with data.

        Used for testing.

        Args:
            root (TreeNode): Root of the BST.
            size (int): Size of the BST.
        """
        ...

    def __init__(self, root: "TreeNode | None" = None, size: "int | None" = None):
        """Initializes a BinarySearchTree."""
        self._root = root
        self._size = size or 0


    def insert(self, key: int, value: Any) -> TreeNode:
        """Insert a new node into BST.

        Args:
            key (int): Key which is used for placing the value into the tree.
            value (Any): Value to insert.

        Raises:
            TypeError: If key is not an integer.
            KeyError: If key is already present in the tree.
        
        Returns:
            TreeNode: The newly inserted node.
        """
        if not isinstance(key, int): raise TypeError
        new_node = TreeNode(key=key, value=value)
        
        if self.root is None: 
            self._root = new_node
            self._size += 1
            return new_node
        
        current_node = self.root
        while current_node is not None:
            if current_node.key == key: raise KeyError
            
            if current_node.key > key:
                if current_node.left is None:
                    current_node.left = new_node
                    new_node.parent = current_node
                    self._size += 1
                    return new_node
                else:
                    current_node = current_node.left       
            elif current_node.key < key:
                if current_node.right is None:
                    current_node.right = new_node
                    new_node.parent = current_node
                    self._size += 1
                    return new_node
                else:
                    current_node = current_node.right
        

    def find(self, key: int) -> TreeNode:
        """Return node with given key.

        Raises:
            TypeError: If `key` is not an integer.
            KeyError: If `key` is not present in the tree.
        """
        if not isinstance(key, int): raise TypeError
        
        current = self.root
        while current is not None:
            if current.key == key:
                return current
            elif key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
        raise KeyError
    
    def try_find(self, key: int) -> TreeNode | None:
        """Returns the node with the given key or None if that node doesn't exist.

        Raises:
            TypeError: If key is not an integer.
        """
        with contextlib.suppress(KeyError):
            return self.find(key)
        return None
    

    @property
    def size(self) -> int:
        """Return the number of nodes contained in the tree."""
        return self._size
    

    # This is what is called when you do `len(tree)`
    @override
    def __len__(self) -> int:
        """Returns the number of nodes contained in the tree."""
        return self.size


    # This is what gets called when you call e.g. `tree[5]`
    @override
    def __getitem__(self, key: int) -> Any:
        """Return value of node with given key.

        Args:
            key (int): Key to look for.

        Raises:
            TypeError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            Any: The value of the node with the given key.
        """
        return self.find(key).value
    
    @override
    def __contains__(self, key: object) -> bool:
        """Return whether a node with the given key is in this tress."""
        if not isinstance(key, int):
            return False
        return self.try_find(key) is not None

    @override
    def __setitem__(self, key: int, value: Any) -> None:
        """Sets the value of the node with the given key or inserts a new node."""
        node = self.try_find(key)
        if node is None:
            self.insert(key, value)
        else:
            node.value = value
    
    @override
    def __delitem__(self, key: int) -> None:
        """Removes node with the given key, maintaining BST-properties."""
        self.remove(key)

    def remove(self, key: int) -> None:
        """Remove node with given key, maintaining BST-properties.

        Args:
            key (int): Key of node which should be deleted.

        Raises:
            TypeError: If key is not an integer.
            KeyError: If key is not present in the tree.
        """
        # * HINT:
        # * find node
        # * node has 0 children? => remove node by detaching from parent
        # * node has 1 child?    => attach child to parent (instead of the node)
        # * node has 2 children?
        # * => find inorder-successor of node (how to do that?)
        # * => swap/replace node with inorder successor (maybe add a function for that)
        # * => after that our node has guaranteed at most one child (why that?)
        ...
        # TODO
        found_node = self.find(key)
        
        if found_node.left is None and found_node.right is None:
            if found_node.parent is None:
                self._root = None
            elif found_node.parent.left == found_node:
                found_node.parent.left = None
            else:
                found_node.parent.right = None
        
        elif found_node.right is None:
            if found_node.parent is None:
                self._root = found_node.left
            elif found_node.parent.left == found_node:
               found_node.parent.left = found_node.left
            else:
                found_node.parent.right = found_node.left
                
            if found_node.left:
                found_node.left.parent = found_node.parent
            
        elif found_node.left is None:
            if found_node.parent is None:
                self._root = found_node.right
            elif found_node.parent.left == found_node:
                found_node.parent.left = found_node.right
            else:
                found_node.parent.right = found_node.right
            if found_node.right:
                found_node.right.parent = found_node.parent
        else:
            inorder_successor = self.return_min_key_in_tree(found_node.right)
            
            if inorder_successor.parent != found_node:
                inorder_successor.parent.left = inorder_successor.right
                if inorder_successor.right:
                    inorder_successor.right.parent = inorder_successor.parent
                inorder_successor.right = found_node.right
                inorder_successor.right.parent = inorder_successor
              
            if found_node.parent is None:
                self._root = inorder_successor
                inorder_successor.parent = None
            elif found_node.parent.left == found_node:
                inorder_successor.parent = found_node.parent
                found_node.parent.left = inorder_successor
            elif found_node.parent.right == found_node:
                inorder_successor.parent = found_node.parent
                found_node.parent.right = inorder_successor
                
            inorder_successor.left = found_node.left
            inorder_successor.left.parent = inorder_successor
            
            found_node.parent = None
            found_node.left = None
            found_node.right = None
        self._size -= 1
                
            

    def inorder(self) -> Iterable[TreeNode]:
        """Returns an iterable yielding the nodes in inorder."""
        inorder_list: list[TreeNode] = []
        queue: list[TreeNode] = []
        
        current_node = self.root
        while current_node is not None or len(queue) > 0:
            while current_node is not None:
                queue.append(current_node) # add node to queue, like a waitlist
                current_node = current_node.left # pick the next node
                
            # after we found the first node that is None, we knwo it's the leftmost one.
            
            current_node = queue.pop() # we extract that last found leftmost node
            inorder_list.append(current_node) # add it to list
            
            current_node = current_node.right # and choose the right node as the new current node
        return inorder_list

    def preorder(self) -> Iterable[TreeNode]:
        """Returns an iterable yielding the nodes in preorder."""
        preorder_list: list[TreeNode] = []
        queue: list[TreeNode] = []
        
        current_node = self.root
        while current_node is not None or len(queue) > 0:
            while current_node is not None:
                preorder_list.append(current_node) # if node exists, add it to list
                
                if current_node.right is not None: # check the right child, if exists
                    queue.append(current_node.right) # if so - add the right child to queue to be checked afterwards
                current_node = current_node.left # set the left child as new current node
            
            if len(queue) > 0:
                current_node = queue.pop() # roll back to the last found right node
        return preorder_list
    
    def postorder(self) -> Iterable[TreeNode]:
        """Returns an iterable yielding the nodes in postorder."""
        if self.root is None: return []
        postorder_list: list[TreeNode] = []
        queue: list[TreeNode] = [self.root] 
        
        while len(queue) > 0:
            current_node = queue.pop() # we get the last node in a queue
            postorder_list.append(current_node) # this last node is added to the list
            
            if current_node.left is not None: # check if left child exists
                queue.append(current_node.left) # if so - add it
            if current_node.right is not None: # check if right child exists
                queue.append(current_node.right) # if so - add it
                
            # in the result we get that the queue is filled with the children first, and then their parent. 
            # The children are filled left first, then right.
            # In reverse, this ensures priority for the child nodes to be proccesed, only then the parent. 
        return postorder_list[::-1]

    # this allows for e.g. `for key in tree` and is required for a mutable mapping
    @override
    def __iter__(self) -> Iterator[int]:
        return iter(node.key for node in self.preorder())

    def is_valid(self) -> bool:
        """Return if the tree fulfills BST-criteria."""
        # for tree to be valid, each parent node has to be larger than all of the left subtree node keys,
        # and smaller than the right node all of the right subtree node keys
        
        if self.root is None: return True
        
        queue: list[TreeNode] = [(self.root, float('-inf'), float('inf'))]
        while len(queue) > 0:
            current_node, min_val, max_val = queue.pop()
            
            if not (min_val < current_node.key < max_val):
                return False
            
            if current_node.right:
                queue.append((current_node.right, current_node.key, max_val))
                
            if current_node.left:
                queue.append((current_node.left, min_val, current_node.key))
        return True

    def return_min_key(self) -> "TreeNode | None":
        """Return the node with the smallest key (None if tree is empty)."""
        return self.return_min_key_in_tree(self.root)
    
    # I make here my custom method that takes as an input the starting node to search from
    def return_min_key_in_tree(self, node: TreeNode) -> "TreeNode | None":
        if node is None: return None
        
        current_node = node
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def return_max_key(self) -> "TreeNode | None":
        """Return the node with the largest key (None if tree is empty)."""
        if self.root is None: return None
        
        current_node = self.root
        while current_node.right is not None:
            current_node = current_node.right
        return current_node

    @staticmethod
    def count_comparisons(for_list: "list[int]", key: int) -> "tuple[int, int]":
        """Count how many comparisons are needed to find a specific key in a list vs bst.

        Creates a Binary Search tree, inserts all values from `for_list` and then checks
        how many comparisons are needed to find `key` vs how many comparisons are required when
        just going through the list one element after another. 

        `for_list` must not contain duplicates.

        Args:
            for_list (list[int]): The list to check against and build a BST from.
            key (int): The key to find.

        Returns:
            tuple[int, int]:
                0: The number of comparisons walking through the list.
                1: The number of comparisons used in the bst.
        """
        list_comparisons = 0
        for item in for_list:
            list_comparisons += 1
            if item == key:
                break
        
        tree = BinarySearchTree()
        for x in for_list:
            tree.insert(x, None)
            
        bst_comparisons = 0
        current_node = tree.root
        
        while current_node is not None:
            bst_comparisons += 1
            if key == current_node.key:
                break
            
            bst_comparisons += 1
            if key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
                
        return (list_comparisons, bst_comparisons)

    @property
    def root(self) -> "TreeNode | None":
        """Returns the root of the Binary Search Tree."""
        return self._root

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self.inorder())})"

    # You can of course add your own methods and/or functions!
    # (A method is within a class, a function outside of it.)

