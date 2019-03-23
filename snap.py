import numpy as np


def make_grid(xlim, ylim, nx, ny):
    # Making a 2d grid array
    xrange = np.linspace(*xlim, nx)
    yrange = np.linspace(*ylim, ny)

    xgrid, ygrid = np.meshgrid(xrange, yrange)

    fullgrid = np.stack((xgrid, ygrid), axis=2)
    return fullgrid


def snap_to_grid(grid, point):

    dists = np.linalg.norm((grid - point), axis=2)

    gridpoint = np.unravel_index(dists.argmin(), dists.shape)
    return grid[gridpoint]


if __name__ == "__main__":

    testgrid = make_grid((0, 1), (0, 1), 5, 5)
    testpoint = (0.1, 0.2)

    print(snap_to_grid(testgrid, testpoint))
