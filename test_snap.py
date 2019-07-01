import pytest
import numpy as np
from snap import Grid


@pytest.fixture
def dummy_grid():
    g = Grid([0, 0], [1, 1], 6, 5)
    return g


def test_grid_dtypes(dummy_grid):
    g = dummy_grid
    assert type(g.grid_points == np.array)
    assert type(g.center_points == np.array)


def test_grid_shape(dummy_grid):
    g = dummy_grid
    assert g.grid_points.shape == (6, 5, 2)
    assert g.center_points.shape == (5, 4, 2)


def test_grid_values(dummy_grid):
    g = dummy_grid
    assert np.all(g.grid_points[0, 0] == np.array([0, 0]))
    assert np.all(g.grid_points[1, 1] == np.array([1 / 5, 1 / 4]))


def test_random_gridpoint(dummy_grid):
    g = dummy_grid
    np.random.seed(123)
    assert np.random.rand() == 0.6964691855978616  # sanity check
    assert [g.random_index(g.nx, g.ny) for i in range(3)] == [(2, 4), (2, 1), (3, 2)]
    p = g.random_point()
    print(p[0], p == np.array([3/5,  0.25]))
    # print(np.array([g.get_random_point() for i in range(3)]))
    assert np.all(np.array([g.random_index(g.nx, g.ny) for i in range(100)]).max(0) == [5, 4])

    assert np.all(np.array([g.random_point() for i in range(100)]).max(0) == np.array([1, 1]))


def test_random_rect(dummy_grid):
    g = dummy_grid
    for i in range(100):
        p1, p2 = g.random_rect()
