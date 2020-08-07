from Diagram import fortunes, getPerimeter
import sys
import Calc
import random
import math
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection as LineColl

def makeSimple():
    points = Calc.getSitePoints(1050)
    edges = fortunes(points)
    print(getPerimeter(edges))
    # plot(edges, points)

def plot(edges, sites):
    plt.axis([0, 1, 0, 1])
    sites = np.array(sites)
    edges = LineColl(edges)
    plt.plot(sites[:,0], sites[:,1], 'ro')
    plt.gca().add_collection(edges)
    plt.show()

def monteCarlo(numPoints, numTrials, batchSize, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    collection = []
    print('doing trials...')

    for curr in range(numTrials):
        loadingBar(curr, numTrials)
        i = random.randrange(0, numPoints)
        minData = None
        minP = math.inf
        for _ in range(batchSize):
            points[i] = Calc.wiggle(points[i], jiggleSize)
            edges = fortunes(points)
            p = getPerimeter(edges)
            if p < minP:
                minData = (edges, list(points))
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
    # points = Calc.getSitePoints(numPoints)
    points = [(0.5+0.1*math.cos(2*math.pi/3),0.5+0.1*math.sin(2*math.pi/3)),(0.5+0.1*math.cos(4*math.pi/3),0.5+0.1*math.sin(4*math.pi/3)),(0.6,0.5),(0.5,0.5)]
    edges = fortunes(points)
    collection = [((edges, list(points)), getPerimeter(edges))]
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
                edges = fortunes(testPoints)
                pwiggle = getPerimeter(edges)
                gradient.append((pwiggle - p0)/jiggleSize)
        for i in range(len(points)):
            points[i] = (points[i][0]+stepSize*gradient[2*i - 1],
                         points[i][1]+stepSize*gradient[2*i])
        edges = fortunes(points)
        collection.append(((edges, list(points)), getPerimeter(edges)))
            
    print('\ndone with trials')
    return collection

def gradientDescentSpecialStep(numPoints, numTrials, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    edges = fortunes(points)
    collection = [((edges, list(points)), getPerimeter(edges))]
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
                edges = fortunes(testPoints)
                pwiggle = getPerimeter(edges)
                gradient.append((pwiggle - p0)/jiggleSize)
        for i in range(len(points)):
            points[i] = (points[i][0]+stepSize*gradient[2*i - 1],
                         points[i][1]+stepSize*gradient[2*i])
        edges = fortunes(points)
        collection.append(((edges, list(points)), getPerimeter(edges)))
            
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
    ax1.set_title('gamma function (perimeter)')
    ax2.set_title('voronoi diagram')

    gammaLine, = ax1.plot([], [], lw=3) # the comma unpacks the tuple
    edges = LineColl(())
    sites, = ax2.plot([], [], 'ro')
    ax2.add_collection(edges)
    gamma = []

    def animate(i):
        tempE, tempS = collection[i][0]
        edges.set_segments(tempE)
        tempS = np.array(list(tempS))
        # tempS = np.fromiter(tempS, 'float,float').reshape((len(tempS),2))
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
    numTrials = 10
    jiggleSize = 0.05
    # collection = monteCarlo(numPoints, numTrials, 10, jiggleSize)
    collection = gradientDescent(numPoints, numTrials, jiggleSize, 0.1)
    # collection = gradientDescentSpecialStep(numPoints, numTrials, 0.1)
    plotAnimation(collection)
