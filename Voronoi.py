import matplotlib.pyplot as plt
import numpy as np
import Calc
from matplotlib.collections import LineCollection as LineColl
from functools import reduce
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
            if event._kind == 'site event':
                self.handleSiteEvent(event)
            else:
                self.handleCircleEvent(event._leaf)
        self.finishDiagram(points)
        # TODO traverse the half edges to add the cell records and the pointers to and from them

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
        self._edgelist.assignAdjacency(coord, prevBreakpoint._halfedge, nextBreakpoint._halfedge)
        vert = self._edgelist.addVertex(coord)
        newHalf = self._edgelist.addEdge(coord)
        vert._incidentEdge = newHalf

        # readjusting tree
        if nextBreakpoint == leaf._parent:
            self._tree.replaceWithChild(nextBreakpoint, nextBreakpoint._right)
            prevBreakpoint._breakpoint[1] = nextLeaf._site
            remainingBp = prevBreakpoint
        elif prevBreakpoint == leaf._parent:
            self._tree.replaceWithChild(prevBreakpoint, prevBreakpoint._left)
            nextBreakpoint._breakpoint[0] = prevLeaf._site
            remainingBp = nextBreakpoint
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
            exists = lambda x: x is not None
            if not (exists(e._origin) or exists(t._origin)):
                if Calc.isOutside(e._point):
                    inward = e if (Calc.extend(t._point, t._vector) is None) else t # note that e if ...t... else t (not e if ...e...)
                    inward._origin = Calc.shorten(inward._point, inward._vector)
                    inward._twin._origin = Calc.extend(inward._point, inward._vector)
                else:
                    e._origin = Calc.shorten(e._point, e._vector)
                    t._origin = Calc.shorten(t._point, t._vector)
            else:
                if Calc.pointsOutward(e._origin, e._vector) or Calc.pointsOutward(t._origin, t._vector):
                    toRemove.add(e)
                    toRemove.add(t)
                elif exists(e._origin) and exists(t._origin):
                    for outside in filter(lambda x: Calc.isOutside(x._origin), [e,t]):
                        outside._origin = Calc.shorten(outside._origin, outside._vector) # change to shorten on non-twin??
                else: # only one exists
                    existing = e if not (e._origin is None) else t # gives _an_ existing edge (or t if neither exist)
                    existing._twin._origin = Calc.extend(existing._origin, existing._vector)
                    if Calc.isOutside(existing._origin):
                        existing._origin = Calc.shorten(existing._origin, existing._vector)
        for e in toRemove:
            self._edgelist.removeEdge(e)

    def perimeter(self):
        halfLength = lambda acc,x: acc+(Calc.dist(x._origin,x.dest())/2.0)
        return 4 + reduce(halfLength, self._edgelist.edges(), 0)

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
    points = Calc.getSitePoints(172)
    # points = [[0.11, 0.94], [0.12, 0.62], [0.12, 0.42], [0.71, 0.38], [0.29, 0.48], [0.51, 0.73], [0.54, 0.03], [0.66, 0.66], [0.9, 0.61], [0.19, 0.85], [0.78, 0.97], [0.9, 0.15], [0.75, 0.87], [0.96, 0.9], [0.79, 0.13], [0.49, 0.29], [0.18, 0.5], [0.13, 0.37], [0.62, 0.21], [0.17, 0.89], [0.98, 0.43], [0.8, 0.7], [0.93, 0.59], [0.21, 0.64], [0.77, 0.92], [0.38, 0.01], [0.21, 0.36], [0.34, 0.23], [0.71, 0.78], [0.95, 0.08], [0.87, 0.91], [0.85, 0.34], [0.61, 0.69]]

    print(points)
    diagram = Voronoi(points)
    print('perimeter: ' + str(Calc.roundBetter(diagram.perimeter())))
    diagram.plot(points)

"""Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- null checking the methods of BinTree
- circle event when arc is not under the site
"""
