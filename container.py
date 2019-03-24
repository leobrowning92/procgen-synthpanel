import time, datetime, argparse

import numpy as np

import flat as fl

import snap

GREEN = (0, 255, 0)
RED = (255, 0, 0)


def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


class Container:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        linecolor=(100, 0, 0),
        primary_grid=(5, 5),
        grid_inset=0,
        inset=0,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inset = inset
        self.linecolor = fl.rgb(*linecolor)
        self.childcolor = (0, 0, 100)
        self.rectstyle = fl.shape().stroke(self.linecolor).width(3)
        self.children = []
        self.grid = self.make_grid(*primary_grid, grid_inset)

    # spatial functions
    def make_grid(self, nx, ny, inset=0):
        xstart = self.x + inset
        ystart = self.y + inset
        xlim = (xstart, self.x + self.width - inset)
        ylim = (ystart, self.y + self.height - inset)
        return snap.make_grid(xlim, ylim, nx, ny)

    def make_gridsnapped_point(self):
        x1 = np.random.rand() * self.width + self.x
        y1 = np.random.rand() * self.height + self.y
        return snap.snap_to_grid(self.grid, (x1, y1))

    # Drawing
    def draw_bbox(self, page, v=False):
        linestyle = fl.shape().stroke(fl.rgb(*RED)).width(1)
        page.place(linestyle.rectangle(self.x, self.y, self.width, self.height))
        if v:
            # page.place(fl.shape().fill(fl.rgb(*GREEN)).circle(self.x, self.y, 1))
            pass

    def draw_outline(self, page, v=False):
        page.place(
            self.rectstyle.rectangle(
                self.x + self.inset,
                self.y + self.inset,
                self.width - 2 * self.inset,
                self.height - 2 * self.inset,
            )
        )
        pass

    def draw(self, page, v=False):
        if v:
            self.draw_bbox(page=page, v=v)
        self.draw_outline(page=page, v=v)

        if self.children:
            for child in self.children:
                child.draw(page, v=v)

    # Child creation

    def insert_child(self, x, y, width, height, linecolor, inset=0):
        # could add check that child is actually within parent
        self.children.append(
            Container(x, y, width, height, linecolor=linecolor, inset=inset)
        )

    def random_child(self, v=False):

        startpoint = self.make_gridsnapped_point()
        while np.any(np.equal(startpoint, self.grid[-1, -1])):
            startpoint = self.make_gridsnapped_point()

        endpoint = self.make_gridsnapped_point()

        while np.any(np.greater_equal(startpoint, endpoint)):
            endpoint = self.make_gridsnapped_point()

        width = endpoint[0] - startpoint[0]
        height = endpoint[1] - startpoint[1]

        self.insert_child(*startpoint, width, height, self.childcolor, inset=self.inset)


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
            for k in range(child_containers):
                cont.random_child(v=True)
            cont.draw(page, v=v)

            # save the image
    page.image(kind="rgb").png("out.png".format(savename))
    page.image(kind="rgb").png("outputs/{}.png".format(savename))


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
