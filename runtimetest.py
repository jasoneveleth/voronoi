from Calc import getSitePoints
from Voronoi import fortunes
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import timeit

repeats = 50
numPoints = 3000
setup = '''
from Calc import getSitePoints
from Voronoi import fortunes
from scipy.spatial import Voronoi, voronoi_plot_2d
'''
setupWithCollecting = 'gc.enable()\n' + setup
time = lambda x: timeit.Timer(x, setupWithCollecting).timeit(repeats)


mine = '''
points = getSitePoints({})
vor = Voronoi(points)
'''.format(numPoints)

theirs = '''
points = getSitePoints({})
vor = fortunes(points)
'''.format(numPoints)

tests = [mine, theirs]
print('for {} points'.format(numPoints))
for test in tests:
    t = time(test)
    print(t, 'seconds to compute', repeats, 'loops\n',
          int(100*t/repeats), 'ms per repeat')

