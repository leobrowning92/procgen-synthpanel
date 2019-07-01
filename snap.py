import numpy as np
import flat as fl



class Grid(object):
    def __init__(self, startpoint, endpoint, nx, ny):
        self.start = np.array(startpoint)
        self.end = np.array(endpoint)
        self.nx = nx
        self.ny = ny
        self.grid_points = self.make_grid(self.start, self.end, nx, ny)
        self.center_points = self.make_grid_centers(self.grid_points)

        self.point=0

    def make_grid(self, start, end, nx, ny):
        # Making a 2d grid array
        self.xrange = np.linspace(start[0], end[0], nx)
        self.yrange = np.linspace(start[1], end[1], ny)

        xgrid, ygrid = np.meshgrid(self.yrange, self.xrange)

        fullgrid = np.stack((ygrid, xgrid), axis=2)
        return fullgrid

    def make_grid_centers(self, grid):
        gridspacing = np.divide(
            (self.start - self.end), [(self.nx - 1) * 2, (self.ny - 1) * 2]
        )
        start = self.start - gridspacing
        end = self.end + gridspacing

        return self.make_grid(start, end, self.nx - 1, self.ny - 1)

    def snap_to_grid(self, point):

        dists = np.linalg.norm((self.grid_points - point), axis=2)

        gridpoint = np.unravel_index(dists.argmin(), dists.shape)
        return self.grid_points[gridpoint]

    def random_index(self, xmax, ymax):
        i = np.random.choice(np.arange(0, xmax))
        j = np.random.choice(np.arange(0, ymax))
        return i, j

    def random_point(self):
        point = self.grid_points[self.random_index(self.nx, self.ny)]
        return point

    def random_center(self):
        return self.center_points[self.random_index(self.nx - 1, self.ny - 1)]

    def random_rect(self):
        ci, cj = self.random_index(self.nx - 1, self.ny - 1)
        return self.grid_points[ci,cj], self.grid_points[ci+1,cj+1]

    def __iter__(self,point):
        return iter(np.reshape(self.grid, (self.nx*self.ny,2)))

    def __next__(self):
        return (self.point)



    def draw_grids(self, page):
        RED = fl.rgb(255, 0, 0)
        BLUE = fl.rgb(0, 0, 255)
        primary_grid = fl.shape().stroke(RED).width(page.height * 0.001)
        secondary_grid = fl.shape().stroke(BLUE).width(page.height * 0.001)

        for ix, iy in np.ndindex(self.grid_points.shape[:-1]):
            page.place(primary_grid.circle(*self.grid_points[ix, iy], 1))

        for ix, iy in np.ndindex(self.center_points.shape[:-1]):
            page.place(secondary_grid.circle(*self.center_points[ix, iy], 1))


if __name__ == "__main__":
    pagesize = 200
    doc = fl.document(pagesize, pagesize, "mm")
    page = doc.addpage()

    grid = Grid([10, 10], [190, 190], 5, 5)
    grid.draw_grids(page)

    img = page.image(kind="rgb").png("out.png")

    print(grid.grid_points[0, 0], grid.center_points[0, 0])

    # TODO make a grid class for the grid_points and center_points
    # that can be used with `point in grid` syntax
    # probably means it has to be an iterator, but can check
