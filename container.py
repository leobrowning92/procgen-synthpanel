import numpy as np
import flat as fl


class Container:
    def __init__(self, x, y, width, height, linecolor=(100, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.linecolor = fl.rgb(*linecolor)
        self.childcolor = (0, 0, 100)
        self.rectstyle = fl.shape().stroke(self.linecolor).width(3)
        self.children = []

    def draw(self, page):
        page.place(self.rectstyle.rectangle(self.x, self.y, self.width, self.height))
        if self.children:
            for child in self.children:
                child.draw(page)

    def insert_child(self, x, y, width, height, linecolor):
        # could add check that child is actually within parent
        self.children.append(Container(x, y, width, height, linecolor=linecolor))

    def random_child(self):
        self.insert_child(
            np.random.rand() * self.width + self.x,
            np.random.rand() * self.height + self.y,
            np.random.rand() * self.width,
            np.random.rand() * self.height,
            self.childcolor,
        )


pagesize = 200
grid_n = 5
grid_size = pagesize / grid_n
doc = fl.document(pagesize, pagesize, "mm")
page = doc.addpage()


for i in range(5):
    for j in range(5):
        cont = Container(
            (i + 0.05) * grid_size,
            (j + 0.1) * grid_size,
            grid_size * 0.9,
            grid_size * 0.8,
        )
        cont.random_child()
        cont.draw(page)


img = page.image(kind="rgb").png("container.png")
