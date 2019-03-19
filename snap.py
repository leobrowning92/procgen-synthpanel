import bisect
import numpy as np
def snap(myGrid, myValue):
    ix = bisect.bisect_right(myGrid, myValue)


grid = np.array([[1, 1], [1, 2], [2, 1], [2, 2]])

point=[1.2,1.9]


dists=np.linalg.norm(grid-point,axis=1)


