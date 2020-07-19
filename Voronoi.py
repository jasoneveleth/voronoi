import matplotlib.pyplot as plt
import numpy as np
import Calc
from matplotlib.collections import LineCollection as LineColl
from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap
from Errors import *

class Voronoi:
    def __init__(self, points):
        self._events = Heap()
        self._tree = BinTree()
        self._edgelist = DCEL()
        for p in points:
            self._events.insert('site event', p)

        while not self._events.empty():
            event = self._events.removeMax()
            print(self._tree)
            if event._kind == 'site event':
                print('site event')
                self.handleSiteEvent(event)
            else:
                print('circle event')
                self.handleCircleEvent(event._leaf)
            print(self._tree)
            print('-----------------------------------------------------------')
        self.finishDiagram(points)
        self.plot(points)

    def handleSiteEvent(self, event):
        if self._tree.empty():
            self._tree.addRoot('arc', event._site, None)
            return
        oldNode = self._tree.findArc(event._site)
        point = Calc.getProjection(event._site, oldNode._site)

        self.removeFalseAlarm(oldNode)

        # add subtree
        oldNode._version = 'breakpoint'
        oldNode._breakpoint = [oldNode._site, event._site]
        oldNode._halfedge = self._edgelist.addEdge(point)
        self._edgelist.initSiteVector(oldNode._halfedge, oldNode._site, event._site)
        newBp = self._tree.addRight(oldNode, 'breakpoint', 
                                      [event._site, oldNode._site],
                                      oldNode._halfedge._twin)
        oldArcLeft = self._tree.addLeft(oldNode, 'arc', oldNode._site)
        newArc = self._tree.addLeft(newBp, 'arc', event._site)
        oldArcRight = self._tree.addRight(newBp, 'arc', oldNode._site)
        oldNode._site = None

        toLeft = self._tree.prevLeaf(oldArcLeft)
        if toLeft is not None:
            self.checkNewCircle(toLeft, oldArcLeft, newArc)

        toRight = self._tree.nextLeaf(oldArcRight)
        if toRight is not None:
            self.checkNewCircle(newArc, oldArcRight, toRight)
        

    def handleCircleEvent(self, leaf):
        nextLeaf = self._tree.nextLeaf(leaf)
        prevLeaf = self._tree.prevLeaf(leaf)
        nextBreakpoint = self._tree.successor(leaf)
        prevBreakpoint = self._tree.predecessor(leaf)
        self._tree.remove(leaf)
        coord = Calc.circleCenter(prevLeaf._site, leaf._site, nextLeaf._site)
        bottom = Calc.circleBottom(prevLeaf._site, leaf._site, nextLeaf._site)

        prevBreakpoint._halfedge._twin._origin = coord
        nextBreakpoint._halfedge._twin._origin = coord
        vert = self._edgelist.addVertex(coord)
        newHalf = self._edgelist.addEdge(coord)
        vert._incidentEdge = newHalf

        self._edgelist.assignAdjacency(coord, prevBreakpoint._halfedge, nextBreakpoint._halfedge)

        # readjusting tree
        if nextBreakpoint == leaf._parent:
            self._tree.replace(nextBreakpoint, nextBreakpoint._right)
            prevBreakpoint._breakpoint[1] = nextLeaf._site
            remainingBp = prevBreakpoint # or upper
        elif prevBreakpoint == leaf._parent:
            self._tree.replace(prevBreakpoint, prevBreakpoint._left)
            nextBreakpoint._breakpoint[0] = prevLeaf._site
            remainingBp = nextBreakpoint # AKA upper
        else:
            raise AssumptionError('our assumptions were wrong, our worst fear')
        remainingBp._halfedge = newHalf
        self._edgelist.initCircleVector(newHalf, remainingBp._breakpoint[0], remainingBp._breakpoint[1], bottom)

        # remove false alarm circle events
        self.removeFalseAlarm(nextLeaf)
        self.removeFalseAlarm(prevLeaf)

        # check for circle self._events
        toLeft = self._tree.prevLeaf(prevLeaf)
        if toLeft is not None:
            self.checkNewCircle(toLeft, prevLeaf, nextLeaf)

        toRight = self._tree.nextLeaf(nextLeaf)
        if toRight is not None:
            self.checkNewCircle(prevLeaf, nextLeaf, toRight)

    def removeFalseAlarm(self, leaf):
        if leaf._event != None:
            self._events.remove(leaf._event)
            leaf._event = None
    
    def checkNewCircle(self, left, center, right):
        next = self._tree.successor(center)
        prev = self._tree.predecessor(center)
        if Calc.converge(next, prev):
            e = self._events.insert('circle event', center, left._site, 
                                    center._site, right._site)
            center._event = e

    def finishDiagram(self, points):
        toRemove = set()
        for e in self._edgelist.edges():
            t = e._twin
            theyExist = (e._origin is not None) and (t._origin is not None)
            neitherExist = (e._origin is None) and (t._origin is None)
            existing = e if not (e._origin is None) else t # gives _an_ existing edge (or t if neither exist)
            if neitherExist:
                if Calc.isOutside(e._point):
                    if Calc.extend(t._point, t._vector) is None:
                        e._origin = Calc.shorten(e._point, e._vector)
                        t._origin = Calc.extend(e._point, e._vector)
                    elif Calc.extend(e._point, e._vector) is None:
                        e._origin = Calc.shorten(t._point, t._vector)
                        t._origin = Calc.extend(t._point, t._vector)
                else:
                    e._origin = Calc.extend(e._point, e._vector)
                    t._origin = Calc.extend(t._point, t._vector)
            else:
                if Calc.pointsOutward(e._origin, e._vector) or Calc.pointsOutward(t._origin, t._vector):
                    toRemove.add(e)
                    toRemove.add(t)
                elif theyExist and not Calc.isOutside(e._origin) and not Calc.isOutside(t._origin):
                    continue
                elif theyExist and (Calc.isOutside(e._origin) or Calc.isOutside(t._origin)):
                    outside = e if Calc.isOutside(e._origin) else t
                    outside._origin = Calc.extend(outside._twin._origin, outside._twin._vector)
                elif (not neitherExist) and Calc.isOutside(existing._origin):
                    if Calc.extend(existing._origin, existing._vector) is None:
                        toRemove.add(e)
                        toRemove.add(t)
                    else:
                        existing._twin._origin = Calc.extend(existing._origin, existing._vector)
                        existing._origin = Calc.shorten(existing._origin, existing._vector)
                elif (not neitherExist) and not Calc.isOutside(existing._origin):
                    existing._twin._origin = Calc.extend(existing._origin, existing._vector)

        for e in toRemove:
            self._edgelist.removeEdge(e)
        # TODO traverse the half edges to add the cell records and the pointers to and from them

    def plot(self, sites=None):
        # plot sites
        if sites is not None:
            sites = np.array(sites)
            plt.plot(sites[:,0], sites[:,1], 'ro')

        vertices = np.array([e._origin for e in self._edgelist.edges()])
        plt.plot(vertices[:,0], vertices[:,1], 'bo')

        edges = [[e._origin, e.dest()] for e in self._edgelist.edges()]
        edges = LineColl(edges)
        plt.gca().add_collection(edges)

        plt.axis([0, 1, 0, 1])
        plt.show()

if __name__ == "__main__":
    # points = [[0.19, 0.68], [0.46, 0.09], [0.95, 0.89]]
    # points = [[0.86, 0.37], [0.38, 0.21], [0.1, 0.51], [0.81, 0.68]]
    # points = [[0.13, 0.29], [0.57, 0.47], [0.05, 0.62]]
    # points = [[0.88, 0.26], [0.26, 0.12], [0.67, 0.43]]
    # points = [[0.51, 0.92], [0.62, 0.82], [0.21, 0.98]]
    # points = [[0.34, 0.52], [0.4, 0.05], [0.4, 0.7]]
    # points = [[0.69, 0.49], [0.5, 0.11], [0.75, 0.7]]
    # points = [[1.0, 0.2], [0.61, 0.86], [0.8, 0.4], [0.95, 0.54]]
    # points = [[0.25, 0.59], [0.61, 0.44], [0.73, 0.2], [0.32, 0.47], [0.99, 0.46], [0.59, 0.87], [0.32, 0.76]]
    points = [[0.83, 0.36], [0.27, 0.25], [0.23, 0.41], [0.18, 0.42]]
    points = [[0.5, 0.93], [0.51, 0.05], [0.42, 0.57], [0.93, 0.86]]
    points = [[0.85, 0.51], [0.97, 0.99], [0.22, 0.21], [0.07, 0.1]]
    points = [[0.99, 0.7], [0.53, 0.4], [0.5, 0.1], [0.29, 0.96]]
    points = Calc.getPoints(4)

    print(points)
    diagram = Voronoi(points)
    # print(diagram._edgelist)

"""Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- null checking the methods of BinTree
- circle event when arc is not under the site
"""
