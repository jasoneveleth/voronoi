import matplotlib.pyplot as plt
import numpy as np
import math
from Calc import rotate
from Diagram import fortunes
from Voronoi import plot
from scipy.spatial import Voronoi, voronoi_plot_2d
a = [rotate((0.25,0.25)),
     rotate((0.25,0.75)),
     rotate((0.75,0.75)),
     rotate((0.75,0.25))]
# a = [(0.25,0.25),
#       (0.25,0.75),
#       (0.75,0.75),
#       (0.75,0.25)]
# a = [(0.25,0.5),
#      (0.75,0.5)]
# a = [(0.25,0.75),
#      (0.75,0.5),
#      (0.75,0.75)]
a = [(0.5+0.1*math.cos(2*math.pi/3),0.5+0.1*math.sin(2*math.pi/3)),(0.5+0.1*math.cos(4*math.pi/3),0.5+0.1*math.sin(4*math.pi/3)),(0.6,0.5),(0.5,0.5)]

a = [rotate((0,0.5),10),
     rotate((0,0.5),20),
     rotate((0,0.5),50),
     rotate((0,0.5),70),
     rotate((0,0.5),80),
     rotate((0,0.5),100),
     rotate((0,0.5),120),
     rotate((0,0.5),180),
     rotate((0,0.5),190),
     rotate((0,0.5),210),
     rotate((0,0.5),300),
     rotate((0,0.5),320),
     rotate((0,0.5),380),
     rotate((0,0.5),390),
     rotate((0,0.5),310),]
vor = Voronoi(np.array(a))
fig = voronoi_plot_2d(vor)
plt.show()
b = fortunes(a)
# print(b, a)
plot(b, a)

