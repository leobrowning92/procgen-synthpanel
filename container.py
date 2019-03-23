import time, datetime, argparse

import numpy as np

import flat as fl

import snap

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Container:
    def __init__(self, x, y, width, height, linecolor=(100, 0, 0), primary_grid=(5, 5)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.linecolor = fl.rgb(*linecolor)
        self.childcolor = (0, 0, 100)
        self.rectstyle = fl.shape().stroke(self.linecolor).width(3)
        self.children = []
        self.grid = self.make_grid(*primary_grid)

    def make_grid(self, nx, ny):
        xlim = (self.x, self.x + self.width)
        ylim = (self.y, self.y + self.height)
        return snap.make_grid(xlim, ylim, nx, ny)

    def draw_bbox(self, page, v=False):
        page.place(self.rectstyle.rectangle(self.x, self.y, self.width, self.height))
        if v:
            page.place(
                fl.shape().stroke(fl.rgb(*GREEN)).width(1).circle(self.x, self.y, 5)
            )
        if self.children:
            for child in self.children:
                child.draw_bbox(page, v=v)

    def insert_child(self, x, y, width, height, linecolor):
        # could add check that child is actually within parent
        self.children.append(Container(x, y, width, height, linecolor=linecolor))

    def random_child(self, v=False):
        # TODO : generate child from two random points within parent, not with xyhw

        x1 = np.random.rand() * self.width + self.x
        y1 = np.random.rand() * self.height + self.y
        x2 = np.random.rand() * self.width + self.x
        y2 = np.random.rand() * self.height + self.y

        startpoint = snap.snap_to_grid(self.grid, (x1, y1))
        endpoint = snap.snap_to_grid(self.grid, (x2, y2))
        width = endpoint[0] - startpoint[0]
        height = endpoint[1] - startpoint[1]
        self.insert_child(*startpoint, width, height, self.childcolor)


def random_grid(n=2, v=False, savename="out"):
    # TODO: need to turn this in to a function so that I can call with CLI
    pagesize = 200
    grid_n = n
    grid_size = pagesize / grid_n
    doc = fl.document(pagesize, pagesize, "mm")
    page = doc.addpage()

    for i in range(grid_n):
        for j in range(grid_n):
            cont = Container(
                (i + 0.05) * grid_size,
                (j + 0.05) * grid_size,
                grid_size * 0.9,
                grid_size * 0.9,
            )
            for k in range(5):
                cont.random_child(v=True)
            cont.draw_bbox(page, v=v)

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
    parser.add_argument("-n", "--number", type=int)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args()
    random_grid(args.number, args.verbose, savename=timestamped_name())
