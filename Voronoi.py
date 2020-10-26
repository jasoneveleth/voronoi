#!/usr/local/bin/python3.8
from voronoi.algorithm import fortunes, getPerimeter, performantPerimeter, newfortunes
import multiprocessing as mp
import voronoi.calc as Calc
import getch
import os
import shutil
import glob
import sys
import random
import math
from functools import reduce
from matplotlib.animation import FuncAnimation
from collections import defaultdict
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection as LineColl
from scipy.spatial import Voronoi, voronoi_plot_2d

def makeSimple(numPoints):
    points = Calc.getSitePoints(numPoints)
    edges = fortunes(points)
    print('perimeter:',getPerimeter(edges))
    plot(edges, points)

def testing(numPoints):
    points = Calc.getSitePoints(numPoints)
    edges = newfortunes(points)
    print('perimeter:',getPerimeter(edges))
    plot(edges, points)

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
    width = math.ceil((Calc.Constants.LOADING * curr)/total)
    percent = str(round((curr/total)*1000)/10)
    bar = "[" + "#" * width + " " * (Calc.Constants.LOADING - width) + "]" + " " + percent + "%"
    sys.stdout.write(u"\u001b[1000D" +  bar)
    sys.stdout.flush()

def bounce(v, dv):
    w = Calc.sumVectors(v, dv)
    if not Calc.isOutside(w):
        return w
    t = 1
    while not Calc.isOutside(Calc.sumVectors(v, Calc.scale(t, dv))):
        point = Calc.shorten(v, dv)
        t = t - Calc.getTime(Calc.subtract(point, v), dv)
        if point[1] == 0 or point[1] == 1:
            dv = (dv[0], -dv[1])
        else:
            dv = (-dv[0], dv[1])
        v = Calc.sumVectors(point, Calc.scale(t, dv))
    return v

def sticky(v, dv):
    w = Calc.sumVectors(v, dv)
    if not Calc.isOutside(w):
        return w
    return Calc.shorten(v, dv)

def lib_asteriods(v, dv):
    w = v + dv
    if Calc.isOutside(w):
        return w
    return w % 1

def asteroids(v, dv):
    w = Calc.sumVectors(v, dv)
    if not Calc.isOutside(w):
        return w
    return (w[0] % 1, w[1] % 1)

def generate(l, i, jiggleSize):
    l = list(l)
    l[i//2] = (l[i//2][0] + jiggleSize*((i+1)%2), l[i//2][1] + jiggleSize*(i%2))
    return l

def performantGradientDescent(numPoints, numTrials, stepSize, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    edges = fortunes(points)
    collection = [((edges, list(points)), getPerimeter(edges))]
    numTrials -= 1 # we did the first one here ^^
    print('doing trials...')
    for curr in range(numTrials):
        loadingBar(curr, numTrials)
        p0 = collection[-1][1]
        with mp.Pool(None) as p:
            possibilities = [generate(points, p, jiggleSize) for p in range(numPoints*2)]
            gradient = p.map(performantPerimeter, possibilities)
        for i,g in enumerate(gradient):
            gradient[i] = (g - p0)/jiggleSize
        for i in range(len(points)):
            points[i] = asteroids(points[i],Calc.scale(stepSize, [gradient[2*i], gradient[2*i + 1]]))
            # points[i] = asteroids(points[i],Calc.scale(-stepSize, gradient[i]))
        edges = fortunes(points)
        collection.append(((edges, list(points)), getPerimeter(edges)))
    loadingBar(numTrials, numTrials)
    print('\ndone with trials')
    return collection

def gradientDescent(numPoints, numTrials, stepSize, jiggleSize):
    points = Calc.getSitePoints(numPoints)
    edges = fortunes(points)
    collection = [((edges, list(points)), getPerimeter(edges))]
    numTrials -= 1 # we did the first one here ^^
    print('doing trials...')
    for curr in range(numTrials):
        loadingBar(curr, numTrials)
        gradient = [[0,0] for _ in range(numPoints)]
        p0 = collection[-1][1]
        for i,point in enumerate(points):
            # x
            points[i] = (point[0]+jiggleSize, point[1])
            gradient[i][0] = (getPerimeter(fortunes(points)) - p0)/jiggleSize
            points[i] = point
            # y
            points[i] = (point[0], point[1]+jiggleSize)
            gradient[i][1] = (getPerimeter(fortunes(points)) - p0)/jiggleSize
            points[i] = point
        for i in range(len(points)):
            points[i] = asteroids(points[i],Calc.scale(-stepSize, gradient[i]))
        edges = fortunes(points)
        collection.append(((edges, list(points)), getPerimeter(edges)))
    loadingBar(numTrials, numTrials)
    print('\ndone with trials')
    return collection

def lib_gradientDescent(numPoints, numTrials, stepSize, jiggleSize):
    points = np.array([[random.random(), random.random()] for _ in range(numPoints)])
    vor = Voronoi(np.copy(points))
    collection = [(vor, calcPerimeter(vor))]
    numTrials -= 1 # we did the first one here ^^
    print('doing trials...')

    for curr in range(numTrials):
        loadingBar(curr, numTrials)
        gradient = np.zeros((numPoints,2))
        p0 = collection[-1][1]
        for i,point in enumerate(points):
            # x
            testPoints = np.copy(points)
            testPoints[i][0] += jiggleSize
            gradient[i][0] = (calcPerimeter(Voronoi(testPoints))-p0)/jiggleSize
            # y
            testPoints = np.copy(points)
            testPoints[i][1] += jiggleSize
            gradient[i][1] = (calcPerimeter(Voronoi(testPoints))-p0)/jiggleSize
        points += (-stepSize) * gradient
        vor = Voronoi(np.copy(points))
        collection.append((vor, calcPerimeter(vor)))
    loadingBar(numTrials, numTrials)
    print('\ndone with trials')
    return collection

# https://stackoverflow.com/questions/40427022/polygon-perimeter
def calcPerimeter(vor, diameter=2):
    centroid = vor.points.mean(axis=0)

    # Mapping from (input point index, Voronoi point index) to list of
    # unit vectors in the directions of the infinite ridges starting
    # at the Voronoi point and neighbouring the input point.
    ridge_direction = defaultdict(list)
    for (p, q), rv in zip(vor.ridge_points, vor.ridge_vertices):
        u, v = sorted(rv)
        if u == -1:
            # Infinite ridge starting at ridge point with index v,
            # equidistant from input points with indexes p and q.
            t = vor.points[q] - vor.points[p] # tangent
            n = np.array([-t[1], t[0]]) / np.linalg.norm(t) # normal
            midpoint = vor.points[[p, q]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - centroid, n)) * n
            ridge_direction[p, v].append(direction)
            ridge_direction[q, v].append(direction)

    listOfPolygons = []
    for i, r in enumerate(vor.point_region):
        region = vor.regions[r]
        if -1 not in region:
            # Finite region.
            listOfPolygons.append(Polygon(vor.vertices[region]))
            continue
        # Infinite region.
        inf = region.index(-1)              # Index of vertex at infinity.
        j = region[(inf - 1) % len(region)] # Index of previous vertex.
        k = region[(inf + 1) % len(region)] # Index of next vertex.
        if j == k:
            # Region has one Voronoi vertex with two ridges.
            dir_j, dir_k = ridge_direction[i, j]
        else:
            # Region has two Voronoi vertices, each with one ridge.
            dir_j, = ridge_direction[i, j]
            dir_k, = ridge_direction[i, k]

        # Length of ridges needed for the extra edge to lie at least
        # 'diameter' away from all Voronoi vertices.
        length = 2 * diameter / np.linalg.norm(dir_j + dir_k)

        # Polygon consists of finite part plus an extra edge.
        finite_part = vor.vertices[region[inf + 1:] + region[:inf]]
        extra_edge = [vor.vertices[j] + dir_j * length,
                      vor.vertices[k] + dir_k * length]
        listOfPolygons.append(Polygon(np.concatenate((finite_part, extra_edge))))
    return reduce(lambda acc,x: acc+x.length, listOfPolygons, 0)

def lib_visualize(collection, fileNum=''):
    os.mkdir('temp')
    for i, (vor, perimeter) in enumerate(collection):
        fig = voronoi_plot_2d(vor)
        plt.xlim([0, 1]), plt.ylim([0, 1])
        plt.savefig(f"temp/{i}.png")
        plt.close(fig)
    fileList = glob.glob('temp/*.png')
    list.sort(fileList, key=lambda x: int(x.split('/')[-1].split('.')[0]))
    with open('temp/image_list.txt', 'w') as file:
        for item in fileList:
            file.write(f"{item}\n")
    os.system(f"convert @temp/image_list.txt visuals/temp{fileNum}.gif")
    shutil.rmtree('temp')

def plotAnimation(collection, fileNum=''):
    numFrames = len(collection)
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2, aspect='equal')
    perimeters = []
    for e in collection:
        perimeters.append(e[1])
    ax1.set_xlim(0, numFrames)
    ax1.set_ylim(0, 4*max(perimeters)/3) # EWWWWW hard coded
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
    anim.save(f'visuals/temp{fileNum}.gif', writer='imagemagick')

if __name__ == "__main__":
    numPoints = 50
    numTrials = 10
    stepSize = 0.001
    jiggleSize = 0.001
    print(f"""
points: {numPoints}, trials: {numTrials}, change: {stepSize}, jiggle: {jiggleSize}
input desired simulation:
\t0: make simple diagram
\t1: gradient descent (then plot)
\t2: scipy gradient descent (then plot)
\t3: monte carlo (then plot)
\t4: performant gradient descent (then plot)""")
    sys.stdout.write('(0/1/2/3/4) ')
    sys.stdout.flush()
    char = getch.getche()
    print('\n\n')
    if char == '1':
        collection = gradientDescent(numPoints, numTrials, stepSize, jiggleSize)
        plotAnimation(collection)
    elif char == '2':
        collection = lib_gradientDescent(numPoints, numTrials, stepSize, jiggleSize)
        lib_visualize(collection)
    elif char == '3':
        collection = monteCarlo(numPoints, numTrials, 10, jiggleSize)
        plotAnimation(collection)
    elif char == '4':
        collection = performantGradientDescent(numPoints, numTrials, stepSize, jiggleSize)
        plotAnimation(collection)
    elif char == '5':
        testing(numPoints)
    else:
        makeSimple(numPoints)
