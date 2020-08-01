from Diagram import Diagram
import sys
import Calc
import random
import math
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection as LineColl

def makeSimple():
    points = Calc.getSitePoints(150)
    d = Diagram(points)
    print(d.getPerimeter())
    plot(d)

def plot(d):
    edges, sites, vertices = d.getPlotables()
    plt.axis([0, 1, 0, 1])
    sites = np.array(sites)
    # vertices = np.array(vertices)
    edges = LineColl(edges)
    plt.plot(sites[:,0], sites[:,1], 'ro')
    # plt.plot(vertices[:,0], vertices[:,1], 'bo')
    plt.gca().add_collection(edges)
    plt.show()

def monteCarlo(numPoints, numTrials, batchSize, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    d = Diagram(points)
    collection = [(d.getPlotables(), d.getPerimeter())]
    numTrials -= 1 # we did the first one here ^^

    print('doing trials...')
    for curr in range(numTrials):
        loadingBar(curr, numTrials)
        i = random.randrange(0, numPoints)
        minData = None
        minP = math.inf
        for _ in range(batchSize):
            points[i] = Calc.wiggle(points[i], jiggleSize)
            d._sites = points
            d.fortunes()
            p = d.getPerimeter()
            if p < minP:
                minData = d.getPlotables()
                minP = p
        collection.append((minData, minP))
    print('\ndone with trials')
    return collection

def loadingBar(curr, total):
    width = int((curr/total) * Calc.Constants.LOADING) + 1
    bar = "[" + "#" * width + " " * (Calc.Constants.LOADING - width) + "]"
    sys.stdout.write(u"\u001b[1000D" +  bar)
    sys.stdout.flush()

def gradientDescent(numPoints, numTrials, stepSize, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    d = Diagram(points)
    collection = [(d.getPlotables(), d.getPerimeter())]
    numTrials -= 1 # we did the first one here ^^

    print('doing trials...')
    for curr in range(numTrials):
        loadingBar(curr, numTrials)
        gradient = []
        p0 = collection[-1][1]
        for i,point  in enumerate(points):
            for j in range(2):
                testPoints = list(points)
                dx = jiggleSize*j
                dy = jiggleSize*(1-j)
                testPoints[i] = (point[0]+dx, point[1]+dy)
                d._sites = testPoints
                d.fortunes()
                pwiggle = d.getPerimeter()
                gradient.append((pwiggle - p0)/jiggleSize)
        for i in range(len(points)):
            points[i] = (points[i][0]+stepSize*gradient[2*i - 1],
                         points[i][1]+stepSize*gradient[2*i])
        d._sites = points
        d.fortunes()
        collection.append((d.getPlotables(), d.getPerimeter()))
            
    print('\ndone with trials')
    return collection

def newtonsMethod(numPoints, numTrials, stepSize, jiggleSize):
    pass

def plotAnimation(collection, fileNum=1):
    numFrames = len(collection)
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2, aspect='equal')
    ax1.set_xlim(0, numFrames)
    ax1.set_ylim(0, 30) # EWWWWW hard coded
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax1.set_title('gamma function')
    ax2.set_title('voronoi diagram')

    gammaLine, = ax1.plot([], [], lw=3) # comma unpacks the tuple, takes first argument
    edges = LineColl(())
    sites, = ax2.plot([], [], 'ro')
    ax2.add_collection(edges)
    gamma = []

    def animate(i):
        tempE, tempS, vertices = collection[i][0]
        edges.set_segments(tempE)
        tempS = np.array(tempS)
        sites.set_data(tempS[:,0], tempS[:,1])

        gamma.append(collection[i][1])
        x = np.arange(len(gamma))
        y = np.array(gamma)
        gammaLine.set_data(x, y)
        return gammaLine,edges,sites,

    anim = FuncAnimation(fig, animate, frames=numFrames,
                         interval=20, blit=True)
    anim.save('optimization{}.gif'.format(fileNum), writer='imagemagick')

if __name__ == "__main__":
    # makeSimple()
    numPoints = 50
    numTrials = 500
    jiggleSize = 0.2
    collection = monteCarlo(numPoints, numTrials, 10, jiggleSize)
    # collection = gradientDescent(numPoints, numTrials, jiggleSize, 0.1)
    plotAnimation(collection)
