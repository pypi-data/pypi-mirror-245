import pytest
from advoco.tools.grid import get_manhattan_dist, Vector


#################### get_manhattan_dist ####################
@pytest.mark.parametrize(
    "tuple_a,tuple_b,expected",
    [
        ((0, 0), (0, 0), 0),
        ((0, 0), (1, 1), 2),
        ((0, 0), (-1, -1), 2),
        ((0, 0), (5, -5), 10),
        (
            (5234701378045132, -1234701378045132),
            (-5234701378045132, 4234701378045132),
            15938805512180528,
        ),
    ],
)
def test_manhattan_dist(tuple_a, tuple_b, expected):
    assert get_manhattan_dist(tuple_a, tuple_b) == expected


#################### Vector ####################
def test_different_vectors_do_not_equal():
    assert Vector([0]) != Vector([1])


@pytest.mark.parametrize(
    "vector_a_inp,vector_b_inp,expected_sum_inp",
    [
        # Small numbers
        ([1, 2], [4, 10], [5, 12]),
        # Negatives
        ([-5, 3], [2, -13], [-3, -10]),
        # Big numbers
        (
            [111111111111111111111111111111, 222222222222222222222222222222],
            [222222222222222222222222222222, 555555555555555555555555555555],
            [333333333333333333333333333333, 777777777777777777777777777777],
        ),
        # Dimensions > 2 (if we can do 2d and 10d, we can probably do n-d)
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        ),
    ],
)
def test_vectors_add_together(vector_a_inp, vector_b_inp, expected_sum_inp):
    x = Vector(vector_a_inp)
    y = Vector(vector_b_inp)
    expected_sum = Vector(expected_sum_inp)
    assert x + y == expected_sum


@pytest.mark.parametrize(
    "vector_a_inp,vector_b_inp,expected_diff_inp",
    [
        # Small numbers
        ([5, 3], [1, 3], [4, 0]),
        # Negatives
        ([-5, 3], [2, -13], [-7, 16]),
        # Big numbers
        (
            [111111111111111111111111111111, 222222222222222222222222222222],
            [222222222222222222222222222222, 555555555555555555555555555555],
            [-111111111111111111111111111111, -333333333333333333333333333333],
        ),
        # Dimensions > 2 (if we can do 2d and 10d, we can probably do n-d)
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
        ),
    ],
)
def test_vectors_subtract(vector_a_inp, vector_b_inp, expected_diff_inp):
    x = Vector(vector_a_inp)
    y = Vector(vector_b_inp)
    expected_diff = Vector(expected_diff_inp)
    assert x - y == expected_diff


def test_vectors_subtract_both_directions():
    """Ensure that `x - y` is evaluated differently than `y - x`.
    Background: __rsub__ and magic methods can get confusing, got worried
    that `y - x` was flipping subtraction order. Turned out to not be true,
    but it was only by testing that I fully understood things."""
    x = Vector([5, 3])
    y = Vector([4, -7])
    expected_x_diff_y = Vector([1, 10])
    assert x - y == expected_x_diff_y
    expected_y_diff_x = Vector([-1, -10])
    assert y - x == expected_y_diff_x


def test_add_subtract_with_non_vector_raise():
    vec_2d = Vector([1, 2])
    tuple_2d = (3, 4)
    # Need to ensure + in BOTH directions causes exception!
    with pytest.raises(TypeError):
        vec_2d + tuple_2d
    with pytest.raises(TypeError):
        tuple_2d + vec_2d
    # Need to ensure - in BOTH directions causes exception!
    with pytest.raises(TypeError):
        vec_2d - tuple_2d
    with pytest.raises(TypeError):
        tuple_2d - vec_2d


def test_vectors_of_different_lengths_raise():
    vec_2d = Vector([1, 2])
    vec_3d = Vector([1, 2, 3])
    with pytest.raises(ValueError):
        vec_2d + vec_3d
    with pytest.raises(ValueError):
        vec_2d - vec_3d


@pytest.mark.parametrize(
    "scalar,vector_inp,expected_product_inp",
    [
        # Small numbers
        (-2, [-3, 5], [6, -10]),
        # Big numbers
        (
            200000000000000000000,
            [111111111111111111111111111111, 222222222222222222222222222222],
            [
                22222222222222222222222222222200000000000000000000,
                44444444444444444444444444444400000000000000000000,
            ],
        ),
        # Dimensions > 2 (if we can do 2d and 10d, we can probably do n-d)
        (
            3,
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [30, 33, 36, 39, 42, 45, 48, 51, 54, 57],
        ),
    ],
)
def test_vectors_left_scalar_multiply(scalar, vector_inp, expected_product_inp):
    x = Vector(vector_inp)
    expected_product = Vector(expected_product_inp)
    assert scalar * x == expected_product


@pytest.mark.parametrize(
    "scalar,vector_inp,expected_product_inp",
    [
        # Small numbers
        (-2, [-3, 5], [6, -10]),
        # Big numbers
        (
            200000000000000000000,
            [111111111111111111111111111111, 222222222222222222222222222222],
            [
                22222222222222222222222222222200000000000000000000,
                44444444444444444444444444444400000000000000000000,
            ],
        ),
        # Dimensions > 2 (if we can do 2d and 10d, we can probably do n-d)
        (
            3,
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [30, 33, 36, 39, 42, 45, 48, 51, 54, 57],
        ),
    ],
)
def test_vectors_right_scalar_multiply(scalar, vector_inp, expected_product_inp):
    x = Vector(vector_inp)
    expected_product = Vector(expected_product_inp)
    assert x * scalar == expected_product


def test_equal_vectors_hash_identically():
    x_primus = Vector([2, 7])
    x_secundus = Vector([2, 7])
    assert hash(x_primus) == hash(x_secundus)

    zero_vector = Vector([0, 0])
    assert hash(x_primus - x_secundus) == hash(zero_vector)

    # While we're thinking about hashing, verify dictionary access works too
    d = {}
    VALUE = "working as expected"
    d[x_primus] = VALUE
    assert d[x_secundus] == VALUE
    assert d[x_primus] == d[x_secundus]
    OTHER_VALUE = "still working as expected"
    d[zero_vector] = OTHER_VALUE
    assert d[x_primus - x_secundus] == OTHER_VALUE
