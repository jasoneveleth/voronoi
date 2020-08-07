import numpy as np
import math
from Calc import rotate
from Diagram import fortunes
from Voronoi import plot

a = [rotate((0.25,0.25)),
     rotate((0.25,0.75)),
     rotate((0.75,0.75)),
     rotate((0.75,0.25))]
a = [(0.25,0.25),
      (0.25,0.75),
      (0.75,0.75),
      (0.75,0.25)]

b = fortunes(a)
print(b, a)
plot(b, a)

