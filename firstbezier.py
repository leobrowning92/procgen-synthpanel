import numpy as np
import flat as fl

brick=fl.rgb(100,0,0)
red=fl.rgb(255,0,0)
blue=fl.rgb(0,0,255)


pagesize=100
doc = fl.document(pagesize,pagesize, 'mm')
page=doc.addpage()

circs = fl.shape().stroke(red).width(pagesize*0.01)
lines = fl.shape().stroke(brick).width(pagesize*0.02)

def bez(points):
    assert len(points)==4, "4 points for a cubic bezier!"
    cmds=[fl.command.moveto(*points[0]), fl.command.curveto(*points[1], *points[2], *points[3])]
    d1 = [fl.command.moveto(*points[0]), fl.command.lineto(*points[1])]
    d2 = [fl.command.moveto(*points[2]), fl.command.lineto(*points[3])]
    return cmds,d1,d2


for i in range(5):
    for j in range(5):
        pts=np.random.uniform(size=(4,2))
        pts[0,0]=0
        pts[-1,1]=1
        bezpts = pts*20+np.array([i,j])*20

        cmds, d1, d2=bez(bezpts)
        page.place(lines.path(cmds))

        for pt in bezpts:
            page.place(circs.circle(*pt,0.5))
        page.place(circs.stroke(blue).path(d1))
        page.place(circs.stroke(blue).path(d2))

img = page.image(kind='rgb').png('out.png')
