import numpy as np
import flat as fl
from flat.command import curveto, moveto, quadto, closepath, lineto
from flat.path import elevated
from flat.shape import placedshape, shape


def bez(points):
    assert len(points) == 4, "4 points for a cubic bezier!"
    cmds = [moveto(*points[0]), curveto(*points[1], *points[2], *points[3])]
    d1 = [moveto(*points[0]), lineto(*points[1])]
    d2 = [moveto(*points[2]), lineto(*points[3])]
    return cmds, d1, d2


def rrect(x, y, height, width, radius):
    if radius * 2 > height:
        radius = height / 2
    elif radius * 2 > width:
        radius = width / 2
    start = np.array([x, y])
    cmds = [
        moveto(*(start + [radius, 0])),
        lineto(*(start + [width - radius, 0])),
        quadto(*(start + [width, 0]), *(start + [width, radius])),
        lineto(*(start + [width, height - radius])),
        quadto(*(start + [width, height]), *(start + [width - radius, height])),
        lineto(*(start + [radius, height])),
        quadto(*(start + [0, height]), *(start + [0, height - radius])),
        lineto(*(start + [0, radius])),
        quadto(*start, *(start + [radius, 0])),
        closepath,
    ]
    return cmds


class RoundRect(object):
    __slots__ = "style", "x", "y", "width", "height", "radius", "cmds"

    def __init__(self, style, x, y, width, height, radius):
        self.style = style
        self.x, self.y = x, y
        self.width, self.height = width, height
        if (radius * 2) > height:
            self.radius = height / 2
        elif (radius * 2) > width:
            self.radius = width / 2
        else:
            self.radius = radius

        self.cmds = self.commands()

    def commands(self):
        x, y = self.x, self.y
        w, h = self.width, self.height
        r = self.radius
        start = np.array([x, y])
        commands = [
            moveto(*(start + [r, 0])),
            lineto(*(start + [w - r, 0])),
            quadto(*(start + [w, 0]), *(start + [w, r])),
            lineto(*(start + [w, h - r])),
            quadto(*(start + [w, h]), *(start + [w - r, h])),
            lineto(*(start + [r, h])),
            quadto(*(start + [0, h]), *(start + [0, h - r])),
            lineto(*(start + [0, r])),
            quadto(*start, *(start + [r, 0])),
            closepath,
        ]

        return commands

    def pdf(self, k, x, y):
        fragments = [c.pdf(k, x, y) for c in elevated(self.cmds)]
        fragments.append(self.style.pdfpaint())
        return b" ".join(fragments)

    def svg(self, k, x, y):
        return b'<path d="%s" %s />' % (
            b" ".join(c.svg(k, x, y) for c in self.cmds),
            self.style.svg(),
        )

    def placed(self, k):
        return placedshape(self, k)


def rrect(self, x, y, width, height, radius):
    return RoundRect(self.style, x, y, width, height, radius)


shape.rrect = rrect


if __name__ == "__main__":
    # curveto()
    brick = fl.rgb(100, 0, 0)
    RED = fl.rgb(255, 0, 0)
    BLUE = fl.rgb(0, 0, 255)
    GREEN = fl.rgb(0, 255, 0)

    pagesize = 200
    doc = fl.document(pagesize, pagesize, "mm")
    page = doc.addpage()

    circs = fl.shape().stroke(RED).width(pagesize * 0.01)
    lines = fl.shape().stroke(brick).width(pagesize * 0.02)
    filled = fl.shape().stroke(brick).width(pagesize * 0.02).fill(RED)
    debugline = fl.shape().stroke(GREEN).width(pagesize * 0.02)
    debugpoint = fl.shape().stroke(BLUE).width(pagesize * 0.005)

    corners = np.empty((4, 2))
    corners[0] = [10, 10]
    corners[1] = [190, 10]
    corners[2] = [10, 190]
    corners[3] = [190, 190]
    width = 180
    height = 180

    for point in corners:
        page.place(debugline.circle(*point, 5))

    page.place(debugline.rectangle(*corners[0], *(corners[3] - corners[0])))
    page.place(filled.rrect(10, 10, 180, 180, 20))

    img = page.image(kind="rgb").png("out.png")
