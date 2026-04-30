"""Unit tests fo Algorithms and Data Structures 1 AI - Maze Solving."""

import random
import textwrap
import sys
from typing import NamedTuple, Self

import pytest
from my_maze import MyMaze

try:
    from conftest import points  # type: ignore
except ImportError:

    def points(points: float):
        return lambda function: function

def _check_exits_for_maze(maze_idx: int):
    solution = MAZES[maze_idx]
    student = MyMaze(solution.maze_initial)
    student.find_exits(*solution.start)

    assert len(solution.exits) == len(student.exits), \
        f"Student solution:\n{str(student)}\nExpected solution:\n{solution.maze_solved}"
    assert solution.exits == set(student.exits), \
        f"Student solution:\n{str(student)}\nExpected solution:\n{solution.maze_solved}"


def _check_recursion_depth_for_maze(maze_idx: int):
    # check that max_recursion_depth is being set
    depth = random.randint(1, 1000)  # use random to avoid fitting just for this depth
    student = MyMaze("""   \n   \n   """)
    student.find_exits(0, 0, depth=depth)
    assert student.max_recursion_depth >= depth, "Max recursion depth is not being set."

    solution = MAZES[maze_idx]
    student = MyMaze(solution.maze_initial)
    student.find_exits(*solution.start)

    assert solution.max_recursion_depth is not None, (
        f"Error in testfile: Maze {maze_idx}: "
        "Checking for recursion depth while no desired recursion depth was defined."
    )

    assert student.max_recursion_depth <= solution.max_recursion_depth


def _check_maze_map(maze_idx: int):
    solution = MAZES[maze_idx]
    student = MyMaze(solution.maze_initial)
    student.find_exits(*solution.start)

    assert str(student) == solution.maze_solved, \
        f"Student solution:\n{str(student)}\n\nExpected solution:\n{solution.maze_solved}"


@points(0)
def test_python_version():
    assert sys.version_info >= (3, 13), \
        f"Python version is too low. Required >=3.13, your version: {sys.version_info.major}.{sys.version_info.minor}"


@points(0.5)
def test_one_exit():
    _check_exits_for_maze(0)


@points(0.5)
def test_two_exits():
    _check_exits_for_maze(3)


@points(0.5)
def test_min_maze_with_exit():
    _check_exits_for_maze(1)


@points(0.5)
def test_split_maze_with_two_exits():
    _check_exits_for_maze(5)


@points(0.5)
def test_split_maze_without_exit():
    _check_exits_for_maze(6)


@points(0.5)
def test_big_maze_one_exit():
    _check_exits_for_maze(7)


@points(0.5)
def test_min_maze_with_four_exits():
    _check_exits_for_maze(4)


@points(0.5)
def test_min_maze_without_exit():
    _check_exits_for_maze(2)


@points(0.5)
def test_diagonal_movement_with_exit():
    _check_exits_for_maze(8)


@points(0.5)
def test_max_rec_depth1():
    _check_recursion_depth_for_maze(2)


@points(1.0)
def test_max_rec_depth2():
    _check_recursion_depth_for_maze(7)


@points(1.0)
def test_max_rec_depth3():
    _check_recursion_depth_for_maze(9)


@points(1.0)
def test_maze_map_one_exit():
    _check_maze_map(7)


@points(1.0)
def test_maze_map_multiple_exits():
    _check_maze_map(10)


@points(1.0)
def test_maze_map_diagonal():
    _check_maze_map(8)


START = "S"
EXIT = "X"
VISITED = "."
OBSTACLE = "#"
PATH = " "


class MazeSolution(NamedTuple):
    """Helper struct storing the solution and its initial conditions for a maze."""

    maze_initial: str
    maze_solved: str
    start: tuple[int, int]
    exits: set[tuple[int, int]]
    max_recursion_depth: int | None

    @classmethod
    def create_from(cls, raw_maze_sol: tuple[str, int | None]) -> Self:
        """Creates a MazeSolution from an element of MAZES."""
        maze_solved = textwrap.dedent(raw_maze_sol[0]).strip()
        maze_initial = maze_solved
        for marker in (START, EXIT, VISITED):
            maze_initial = maze_initial.replace(marker, PATH)

        start = None
        exits = set()

        for i, row in enumerate(maze_solved.splitlines()):
            for j, marker in enumerate(row):
                if marker == START:
                    start = (i, j)
                elif marker == EXIT:
                    exits.add((i, j))
                elif marker not in [VISITED, OBSTACLE, PATH]:
                    assert (
                        False
                    ), f"Error in testfile: Testcase has invalid character: {marker}"

        assert start is not None, "Error in testfile: Testcase has no start."
        return cls(maze_initial, maze_solved, start, exits, raw_maze_sol[1])
    
    @classmethod
    def create_from_list(cls, raw_mazes: list[tuple[str, int | None]]) -> list[Self]:
        return [cls.create_from(maze) for maze in raw_mazes]



MAZES: list[MazeSolution] = MazeSolution.create_from_list([
    (
        """
        ######
        #S...#
        ##.#.#
        #..#.#
        #.##.#
        ####X#
        """,
        None,
    ),
    (
        """
        ###
        XS#
        ###
        """,
        None,
    ),
    (
        """
        ###
        #S#
        ###
        """,
        1,
    ),
    (
        """
        ######
        #S...#
        ##.#.#
        #..#.X
        #.##.#
        ####X#
        """,
        None,
    ),
    (
        """
        #X#
        XSX
        #X#
        """,
        None,
    ),
    (
        """
        ######
        #  #.#
        ## #.#
        #  #.X
        # ##S#
        ####X#
        """,
        None,
    ),
    (
        """
        ######
        #..# #
        ##.# #
        #.S#  
        #.## #
        #### #
        """,
        None,
    ),
    (
        """
        ###############
        #......#......#
        ###.#.######..#
        #...#.#######.#
        #.###.........#
        #...#######...#
        ###.#.........#
        X...#.######..#
        #####......##.#
        #####.######..#
        #.........##..#
        #.##########.##
        #..........#.##
        #...##...S...##
        ###############
        """,
        97,
    ),
    (
        """
        ######
        #S.#.#
        ##.#.#
        #..#.X
        #.#..#
        ####X#
        """,
        None,
    ),
    (
        """
        ###############
        #S............#
        #############.#
        #.............#
        #.#############
        #.............#
        #############.#
        #.............#
        #.#############
        #.............#
        #############.#
        #############.#
        #############.#
        #.............#
        ###############
        """,
        85,
    ),
    (
        """
        ##X###
        #S...#
        ##.#.#
        #..#.X
        X.##.#
        ####X#
        """,
        None,
    ),
])

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
