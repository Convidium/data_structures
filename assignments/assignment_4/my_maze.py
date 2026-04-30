"""Algorithms and Data Structures 1 AI - Maze Solving."""
# Using constants might make this more readable.
from typing import override

START = "S"
EXIT = "X"
VISITED = "."
OBSTACLE = "#"
PATH = " "


class MyMaze:
    """Maze object, used for demonstrating recursive algorithms."""

    def __init__(self, maze_str: str):
        """Initialize Maze.

        Args:
            maze_str (str): Maze represented by a string, 
                where rows are separated by newlines (\n).
        """
        # We internally treat this as a list[list[str]], as it makes indexing easier.
        self._maze = list(list(row) for row in maze_str.splitlines())
        self._height = len(self._maze)
        self._width = len(self._maze[0])
        self._exits: list[tuple[int, int]] = []
        self._max_recursion_depth = 0
        
        self._directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self._initial_pos: tuple[int, int] = ()

    def find_exits(self, start_row: int, start_col: int, depth: int = 0):
        """Find and save all exits into `self._exits` using recursion, save
        the maximum recursion depth into `self._max_recursion_depth` and mark the maze.

        An exit is an accessible from an empty cell on the outer rims of the maze.

        You can assume that the starting point is in an empty cell and not on the outer rim.

        Args:
            start_row (int): row to start from. 0 represents the topmost cell.
            start_col (int): column to start from; 0 represents the leftmost cell.
            depth (int): Depth of current iteration.
        """
        if depth > self._max_recursion_depth:
            self._max_recursion_depth = depth
            
        if not (0 <= start_row < self._height and 0 <= start_col < self._width):
            return
        
        if self._initial_pos == ():
            self._initial_pos = (start_row, start_col)
            self._maze[start_row][start_col] = START
            
        current_pos = self._maze[start_row][start_col]
        
        if current_pos == OBSTACLE or current_pos == VISITED or current_pos == EXIT:
            return
        
        if start_row == 0 or start_col == 0 or start_row == self._height-1 or start_col == self._width-1:
            self._exits.append((start_row, start_col))
            self._maze[start_row][start_col] = EXIT
        elif current_pos != START:
            self._maze[start_row][start_col] = VISITED
        
        for diff_row, diff_col in self._directions:
            self.find_exits(start_row + diff_row, start_col + diff_col, depth + 1)
        return
        

    @property
    def exits(self) -> "list[tuple[int, int]]":
        """List of tuples of (row, col)-coordinates of currently found exits."""
        return self._exits

    @property
    def max_recursion_depth(self) -> int:
        """Return the maximum recursion depth after executing find_exits()."""
        return self._max_recursion_depth

    @override
    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self._maze)
