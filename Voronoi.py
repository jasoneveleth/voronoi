import matplotlib.pyplot as plt
import numpy as np
import Calc
from matplotlib.collections import LineCollection as LineColl
from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap
from functools import reduce

class Voronoi:
    def __init__(self, points):
        """takes in a list of points (lists)
        returns the doubly connected edge list"""
        self._events = Heap()
        self._status = BinTree()
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
        self.plot(points)

    def finishDiagram(self, points):
        for e in self._edgelist.edges():
            if e._origin is None:
                e._origin = [e._point[0] + e._vector[0], e._point[1] + e._vector[1]]
                self._edgelist.addVertex(e._origin)
        # TODO traverse the half edges to add the cell records and the pointers to and from them
    
    def plot(self, sites=None):
        # plot sites
        if sites is not None:
            sites = np.array(sites)
            plt.plot(sites[:,0], sites[:,1], 'ro')

        vertices = np.array([e._origin for e in self._edgelist.edges()])
        plt.plot(vertices[:,0], vertices[:,1], 'bo')

        edges = LineColl([[e._origin, e.dest()] for e in self._edgelist.edges()])
        plt.gca().add_collection(edges)

        plt.axis([0, 1, 0, 1])
        plt.show()

    def handleSiteEvent(self, event):
        print('handle site event {}'.format(self._status))
        if self._status.empty():
            self._status.addRoot('arc', event._site, None)
            return
        oldNode = self._status.findArc(event._site)

        # Remove false alarm
        if oldNode._event != None:
            print('removed event for: {}'.format(str(oldNode)))
            self._events.remove(oldNode._event)
            oldNode._event = None

        # add subtree
        oldNode._version = 'breakpoint'
        oldNode._breakpoint = [oldNode._site, event._site]
        point = [event._site[0], (1.0/(2*(oldNode._site[1] - event._site[1]))) * (event._site[0] - oldNode._site[0])**2 + (oldNode._site[1] + event._site[1])/2.0]
        oldNode._halfedge = self._edgelist.addEdge(point, oldNode._site, event._site)

        newBreakpoint = self._status.addRight(oldNode, 'breakpoint', [event._site, oldNode._site], oldNode._halfedge._twin)
        oldArcLeft = self._status.addLeft(oldNode, 'arc', oldNode._site)
        newArc = self._status.addLeft(newBreakpoint, 'arc', event._site)
        oldArcRight = self._status.addRight(newBreakpoint, 'arc', oldNode._site)

        oldNode._site = None

        # update edges
        oldNode._halfedge._twin = newBreakpoint._halfedge
        newBreakpoint._halfedge._twin = oldNode._halfedge
        
        print(self._status)
        # check for new circle events
        toLeft = self._status.prevLeaf(oldArcLeft)
        if toLeft is not None:
            self.checkNewCircle(toLeft, oldArcLeft, newArc)

        toRight = self._status.nextLeaf(oldArcRight)
        if toRight is not None:
            self.checkNewCircle(newArc, oldArcRight, toRight)
        
        print('----------------------------------------------------------------------')

    def handleCircleEvent(self, leaf):
        print('handle circle event {}'.format(str(self._status)))
        nextLeaf = self._status.nextLeaf(leaf)
        prevLeaf = self._status.prevLeaf(leaf)
        nextBreakpoint = self._status.successor(leaf)
        prevBreakpoint = self._status.predecessor(leaf)
        self._status.remove(leaf)

        # readjusting tree
        if nextBreakpoint == leaf._parent:
            self._status.replace(nextBreakpoint, nextBreakpoint._right)
            prevBreakpoint._breakpoint[1] = nextLeaf._site
            newBreakpoint = prevBreakpoint
        elif prevBreakpoint == leaf._parent:
            self._status.replace(prevBreakpoint, prevBreakpoint._left)
            nextBreakpoint._breakpoint[1] = prevLeaf._site
            newBreakpoint = nextBreakpoint
        else:
            print('our assumptions were wrong, our worst fear')
            
        # remove false alarm circle self._events
        if nextLeaf._event != None:
            print('removed event for: {}'.format(str(nextLeaf)))
            self._events.remove(nextLeaf._event)
            nextLeaf._event = None
        if prevLeaf._event != None:
            print('removed event for: {}'.format(str(prevLeaf)))
            self._events.remove(prevLeaf._event)
            prevLeaf._event = None

        print('a: ' + str(prevLeaf._site) + ' b: ' + str(leaf._site) + ' c: ' + str(nextLeaf._site))
        coord = Calc.circleCenter(prevLeaf._site, leaf._site, nextLeaf._site)

        # making new edge
        newHalf = self._edgelist.addEdge(coord, prevLeaf._site, nextLeaf._site)
        newHalf._origin = coord

        # add vertex and incident edge
        vert = self._edgelist.addVertex(coord)
        vert._incidentEdge = newHalf

        oldLeftEdge = prevBreakpoint._halfedge
        oldRightEdge = nextBreakpoint._halfedge
        newBreakpoint._halfedge = newHalf

        self._edgelist.addOrigin(oldLeftEdge, coord)
        self._edgelist.addOrigin(oldRightEdge, coord)

        # assign next and previous
        self._edgelist.assignAdjacency(coord, prevBreakpoint._halfedge, nextBreakpoint._halfedge)

        # check for circle self._events
        toLeft = self._status.prevLeaf(prevLeaf)
        if toLeft is not None:
            self.checkNewCircle(toLeft, prevLeaf, nextLeaf)

        toRight = self._status.nextLeaf(nextLeaf)
        if toRight is not None:
            self.checkNewCircle(prevLeaf, nextLeaf, toRight)
        print('----------------------------------------------------------------------')

    def checkNewCircle(self, left, center, right):
        print('{}, {}, {}'.format(str(left), str(center), str(right)))
        if center._site[1] >= right._site[1] and center._site[1] >= left._site[1]:
            e = self._events.insert('circle event', center, left._site, center._site, right._site)
            center._event = e
            print('added an event for: {}'.format(str(center)))

if __name__ == "__main__":
    # points = [[0.3,0.7],[0.7,0.3]]
    # points = [[0.19, 0.68], [0.46, 0.09], [0.95, 0.89]]
    # points = [[0.86, 0.37], [0.38, 0.21], [0.1, 0.51], [0.81, 0.68]]
    points = Calc.testNumPoints(3)

    diagram = Voronoi(points)
    print(diagram._edgelist)

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- null checking the methods of BinTree
- circle event when arc is not under the site
"""
