from typing import List, Any, Callable, Tuple


class Vector(tuple):
    """Stores position info. Can do basic math. Usage: `Vector([4, 7])`.

    Because this rides on top of `tuple` calls for doing instantiation,
    you'll want to call it with an iterable . If you call it with positional
    args, it will just break. [If we really want this API, it's doable, but
    it requires understanding how to work with __new__, not just __init__.]
    Examples:
        + Vector([4, 7])
        + Vector([1, -2, 3, -4, 5, -6, 7])
        ---BAD---> Vector(4, 7)  <---WILL NOT WORK---

        Math Example:
        Vector([4, 7]) + Vector([6, 3]) - (10 * Vector([1, -1]))
            produces ===> Vector([0, 20])

    Intent is to have a way to record position, but also able to combine them.
    Basically behaves the same as vectors from precalculus math class.
    Can be arbitrary dimension, not just 2d.
    Supports addition, subtraction, and **scalar** multiplication (can multiply
    a Vector by a number, but can't multiply two Vectors). Most importantly,
    it handles equality, hashing, and dictionary lookups as expected, since
    that's what it's most likely to be used for.

    There's some safety stuff in here -- we verify that lengths are the same
    before adding, for example -- but it's not foolproof. For instance, you
    could create a Vector from a string and it would merrily go on its way
    because it's just a thin layer on top of `tuple`. I don't think it's worth
    it to try to add a whole bunch more safety around verifying that the
    incoming values are numbers, but I could be wrong.
    """

    def __repr__(self):
        """Returns an actual `eval`-uable string, e.g: Vector([1, 2, 3])"""
        # Approach kinda hacky, couldn't figure out a proper way to get values
        # of tuple and make it look like a list, so just actually `list` it.
        return f"Vector({list(self)})"

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Vectors can only add with other Vectors")
        if len(self) != len(other):
            raise ValueError("Can not add Vectors of different lengths")
        return Vector([val[0] + val[1] for val in zip(self, other)])

    def __radd__(self, other):
        """Takes over `other + self` direction. Ensure Vector primacy!"""
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Vectors can only subtract with other Vectors")
        if len(self) != len(other):
            raise ValueError("Can not subtract Vectors of different lengths")
        return Vector([val[0] - val[1] for val in zip(self, other)])

    def __rsub__(self, other):
        """Takes over `other - self` direction. Ensure Vector primacy!

        This is a bit confusing. If `x` and `y` are both vectors and
        you want to evaluate `x - y`, in theory you should be able to do
        `x.__sub__(y)` OR `y.__rsub__(x)` and get whatever `x - y` ought to
        come out as. However, because __sub__ is implemented and both are
        Vectors, Python would never call out to __rsub__ in that case.
        Thus, __rsub__ would only get used if `x` was not actually a Vector,
        but we just want an exception to get raised when `x` and `y` are not
        both Vectors, so that's why this whole thing exists. I'm very, very
        confident that the NotImplementedError will never happen, but that
        sure will be interesting if it does!

        Yeah, it's a bit silly. We could implement a `reverse` bool on __sub__
        to handle this, but that's extra logic that would literally never get
        used, so this seemed better. ¯\_(ツ)_/¯"""
        if not isinstance(other, Vector):
            raise TypeError("Vectors can only subtract with other Vectors")
        else:
            raise NotImplementedError("This code should never run. Whoops.")

    def __mul__(self, other):
        """SCALAR multiplication. We do not implement anything else."""
        return Vector([other * val for val in self])

    def __rmul__(self, other):
        """Still just SCALAR multiplication. Handles the other * self side."""
        return self.__mul__(other)


GRID_DELTAS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get_neighbors(
    grid: List[list],
    row: int,
    col: int,
    distance: int = 1,
    gimme_indices: bool = False,
    diagonals: bool = False,
) -> List[Any]:
    neighbors = []
    length = len(grid)
    width = len(grid[0])
    for i in range(max(0, row - distance), min(row + distance + 1, length)):
        for j in range(max(0, col - distance), min(col + distance + 1, width)):
            if i != row or j != col:
                if diagonals or (i == row or j == col):
                    neighbors.append(
                        (grid[i][j], (i, j))
                    ) if gimme_indices else neighbors.append(grid[i][j])
    return neighbors


def get_visible_neighbors(
    grid: List[list],
    row: int,
    col: int,
    distance: int,
    skip_signal: Callable,
    gimme_indices: bool = False,
) -> List[Any]:
    neighbors = []
    length = len(grid)
    width = len(grid[0])
    for row_dir in range(-distance, distance + 1):
        for col_dir in range(-distance, distance + 1):
            if row_dir != 0 or col_dir != 0:
                current_row = row + row_dir
                current_col = col + col_dir
                while 0 <= current_row < length and 0 <= current_col < width:
                    # if grid[current_row][current_col] != skip_signal:
                    if not skip_signal(grid[current_row][current_col]):
                        neighbors.append(
                            (current_row, current_col)
                        ) if gimme_indices else neighbors.append(
                            grid[current_row][current_col]
                        )
                        break
                    current_row += row_dir
                    current_col += col_dir
    return neighbors


def get_manhattan_dist(tuple_a: Tuple[int, int], tuple_b: Tuple[int, int]) -> int:
    return (abs(tuple_b[0] - tuple_a[0])) + abs((tuple_b[1] - tuple_a[1]))
