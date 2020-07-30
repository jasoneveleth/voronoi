from Diagram import Diagram
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

def randomOptimization(numPoints, numTrials, batchSize, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    d = Diagram(points)
    collection = [(d.getPlotables(), d.getPerimeter())]

    for _ in range(numTrials):
        i = random.randrange(0, numPoints)
        print(i)
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
    return collection

def plotAnimation(collection, fileNum, numPoints):
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2, aspect='equal')
    ax1.set_xlim(0, numPoints)
    ax1.set_ylim(0, 30) # EWWWWW hard coded
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    line, = ax1.plot([], [], lw=3) # comma unpacks the tuple, taking first argument
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
        line.set_data(x, y)
        return line,edges,sites,

    anim = FuncAnimation(fig, animate, frames=201,
                         interval=20, blit=True)
    anim.save('optimization{}.gif'.format(fileNum), writer='imagemagick')

if __name__ == "__main__":
    # makeSimple()
    collection = randomOptimization(50, 200, 10, 0.02)
    plotAnimation(collection, 1, 201)

