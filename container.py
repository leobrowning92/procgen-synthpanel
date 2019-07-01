import time, datetime, argparse

import numpy as np

import flat as fl
from flat.shape import shape


import snap
import roundrect

shape.rrect = roundrect.rrect


GREEN = (0, 255, 0)
RED = (255, 0, 0)


def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))


class Container:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        radius=2,
        line_color=(100, 0, 0),
        primary_grid_spacing=(5, 5),
        grid_inset=0,
        inset=0,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.corners = self.make_corners()
        self.inset = inset
        self.line_color = fl.rgb(*line_color)
        self.child_color = (0, 0, 100)
        self.rect_style = fl.shape().stroke(self.line_color).width(3)
        self.children = []
        self.grid = snap.Grid((x,y),(x+width,y+height),*primary_grid_spacing)

    # spatial functions
    def make_corners(self):
        corners = np.empty((4, 2))
        corners[0] = [self.x, self.y]
        corners[1] = [self.x + self.width, self.y]
        corners[2] = [self.x, self.y + self.height]
        corners[3] = [self.x + self.width, self.y + self.height]
        return corners

    def make_grid(self, nx, ny, inset=0):
        # TODO: make sure that this is non-breaking before adding back in
        xstart = self.x + inset
        ystart = self.y + inset
        xlim = (xstart, self.x + self.width - inset)
        ylim = (ystart, self.y + self.height - inset)
        return snap.Grid(xlim, ylim, nx, ny)

    def get_random_gridpoint(self):
        x1 = np.random.rand() * self.width + self.x
        y1 = np.random.rand() * self.height + self.y
        return self.grid.snap_to_grid((x1, y1))

    def contains(self, point):
        inx = self.x < point[0] < self.width + self.x
        iny = self.y < point[1] < self.height + self.y
        if inx and iny:
            return True
        else:
            return False

    def collides_with(self, other):
        return np.any([self.contains(c) for c in other.corners])

    def plays_nice_with_other_children(self, other):
        if len(self.children) == 0:
            return True
        else:
            return np.any([child.collides_with(other) for child in self.children])

    # Drawing
    def draw_bbox(self, page, v=False):
        linestyle = fl.shape().stroke(fl.rgb(*RED)).width(1)
        page.place(linestyle.rectangle(self.x, self.y, self.width, self.height))
        if v:
            # page.place(fl.shape().fill(fl.rgb(*GREEN)).circle(self.x, self.y, 1))
            pass

    def draw_outline(self, page, v=False):
        page.place(
            self.rect_style.rrect(
                self.x + self.inset,
                self.y + self.inset,
                self.width - 2 * self.inset,
                self.height - 2 * self.inset,
                self.radius,
            )
        )
        pass

    def draw(self, page, v=False):
        if v:
            self.draw_bbox(page=page, v=v)
            self.grid.draw_grids(page=page)
        self.draw_outline(page=page, v=v)

        if self.children:
            for child in self.children:
                child.draw(page, v=v)

    def random_child(self, v=False):

        # startpoint = self.grid.random_point()

        # while np.any(np.equal(startpoint, self.grid[-1, -1])):
        #     print(f"{startpoint} bad, retrying")
        #     print(self.grid[-1, -1])
        #     startpoint = self.make_gridsnapped_point()

        # endpoint = self.grid.random_point()
        startpoint, endpoint = self.grid.random_rect()
        # while np.any(np.greater_equal(startpoint, endpoint)):
        #     endpoint = self.make_gridsnapped_point()

        width = endpoint[0] - startpoint[0]
        height = endpoint[1] - startpoint[1]

        return Container(
            *startpoint, width, height, line_color=self.child_color, inset=self.inset
        )

    def add_random_child(self):
        child = self.random_child()
        # while not (self.plays_nice_with_other_children(child)):
        #     child = self.random_child()
        self.children.append(child)


def random_grid(n=2, child_containers=1, v=False, savename="out"):
    # TODO: need to turn this in to a function so that I can call with CLI
    pagesize = 200
    grid_n = n
    grid_size = pagesize / grid_n
    doc = fl.document(pagesize, pagesize, "mm")
    page = doc.addpage()

    for i in range(grid_n):
        for j in range(grid_n):
            cont = Container(
                i * grid_size,
                j * grid_size,
                grid_size,
                grid_size,
                grid_inset=2,
                inset=1,
            )
            if child_containers:
                for k in range(child_containers):
                    cont.add_random_child()
            cont.draw(page, v=v)

            # save the image
    page.image(kind="rgb").png("out.png".format(savename))
    page.image(kind="rgb").png("outputs/procgen-synthpanel_{}.png".format(savename))


def timestamped_name():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d_%H:%M:%f")
    return st


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="\
                                            Plotter function for this folder",
    )
    parser.add_argument("-n", "--number", type=int, default=5)
    parser.add_argument("-c", "--children", type=int, default=1)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args()
    random_grid(
        args.number,
        child_containers=args.children,
        v=args.verbose,
        savename=timestamped_name(),
    )
