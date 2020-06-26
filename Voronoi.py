from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap
from random import random
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

    def finishDiagram(self, points):
        for e in self._edgelist.edges():
            if e._origin is None:
                e._origin = [e._point[0] + e._vector[0], e._point[1] + e._vector[1]]

        # TODO the remaining internal nodes of BinTree are infinite half edges
        # TODO compute a box and attach half-infinite edges to boudning box by updating appropriately
        # TODO traverse the half edges to add the cell records and the pointers to and from them

        # HANDLE WHEN THE LEFTOVER HALFEDGE IS A FULL LINE WITH JUST THE NORMAL INTERSECTION

    def handleSiteEvent(self, event):
        print('handle site event {}'.format(self._status))
        if self._status.empty():
            self._status.addRoot('arc', event._site, None)
            return
        oldNode = self._status.findArc(event._site)

        # Remove false alarm
        if oldNode._event != None:
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
        
        # check for new circle events
        if not self._status.isFirst(oldArcLeft):
            toLeft = self._status.prevLeaf(oldArcLeft)
            self.checkNewCircle(toLeft, oldArcLeft, newArc)

        if not self._status.isLast(oldArcRight):
            toRight = self._status.nextLeaf(oldArcRight)
            self.checkNewCircle(newArc, oldArcRight, toRight)
        

    def handleCircleEvent(self, leaf):
        print('handle circle event {}'.format(str(self._status)))
        nextLeaf = self._status.nextLeaf(leaf)
        prevLeaf = self._status.prevLeaf(leaf)
        nextBreakpoint = self._status.successor(leaf)
        prevBreakpoint = self._status.predecessor(leaf)
        self._status.remove(leaf)

        # readjusting tree
        print('stuff')
        print(nextLeaf._parent)
        print(prevLeaf._parent)
        print(leaf._parent)
        if nextLeaf._parent == leaf._parent:
            self._status.replace(nextBreakpoint, nextLeaf)
            prevBreakpoint._breakpoint[1] = nextLeaf._site
        elif prevLeaf._parent == leaf._parent:
            self._status.replace(prevBreakpoint, prevLeaf)
            nextBreakpoint._breakpoint[1] = prevLeaf._site
        else:
            print('our assumptions were wrong, our worst fear')
            
        # remove false alarm circle self._events
        if nextLeaf._event != None:
            self._events.remove(nextLeaf._event)
            nextLeaf._event = None
        if prevLeaf._event != None:
            self._events.remove(prevLeaf._event)
            prevLeaf._event = None

        print(prevLeaf._site, leaf._site, nextLeaf._site)
        # getting point and making vertex
        coord = self.circleCenter(prevLeaf._site, leaf._site, nextLeaf._site)
        vert = self._edgelist.addVertex(coord)

        # making new edge
        newHalf = self._edgelist.addEdge(coord, prevLeaf._site, nextLeaf._site)
        newHalf._origin = coord

        # it needs one incident edge
        vert._incidentEdge = newHalf

        # adding origin
        oldLeftEdge = prevBreakpoint._halfedge
        oldRightEdge = nextBreakpoint._halfedge
        if nextBreakpoint._version is not 'arc':
            nextBreakpoint._halfedge = newHalf
        else:
            prevBreakpoint._halfedge = newHalf

        if oldLeftEdge._origin is None:
            oldLeftEdge._origin = coord
        else:
            oldLeftEdge._twin._origin = coord

        if oldRightEdge._origin is None:
            oldRightEdge._origin = coord
        else:
            oldRightEdge._twin._origin = coord

        # assign next and previous
        self._edgelist.assignAdjacency(coord, prevBreakpoint, nextBreakpoint)

        # check for circle self._events
        if not self._status.isFirst(prevLeaf):
            toLeft = self._status.prevLeaf(prevLeaf)
            if toLeft is not None:
                self.checkNewCircle(toLeft, prevLeaf, nextLeaf)
        if not self._status.isLast(nextLeaf):
            toRight = self._status.nextLeaf(nextLeaf)
            if toRight is not None:
                self.checkNewCircle(prevLeaf, nextLeaf, toRight)

    def checkNewCircle(self, left, center, right):
        if center._site[1] >= right._site[1] and center._site[1] >= left._site[1]:
            e = self._events.insert('circle event', center, left._site, center._site, right._site)
            center._event = e

    def circleCenter(self, a, b, c):
        print('a: ' + str(a) + ' b: ' + str(b) + ' c: ' + str(c))
        d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
        x = (1.0/d)*((a[0]**2 + a[1]**2)*(b[1] - c[1]) + (b[0]**2 + b[1]**2)*(c[1] - a[1]) + (c[0]**2 + c[1]**2)*(a[1] - b[1]))
        y = (1.0/d)*((a[0]**2 + a[1]**2)*(c[0] - b[0]) + (b[0]**2 + b[1]**2)*(a[0] - c[0]) + (c[0]**2 + c[1]**2)*(b[0] - a[0]))
        return [x,y]

def rand():
    return round(random()*100)/100.0

def testNumPoints(n):
    points = []
    yvalues = []
    for _ in range(n):
        a = rand()
        while a in yvalues:
            a = rand()
        yvalues.append(a)
        points.append([rand(),a])
    print(points)
    diagram = Voronoi(points)
    # print("diagram has been made!!!!!!!")
    # print(diagram._edgelist)
    # print(diagram._status)

if __name__ == "__main__":
    diagram = Voronoi([[0.3,0.7],[0.7,0.3]])
    print(diagram._edgelist)
    print(diagram._status)
    # print('HERE IS DIVISION')
    # diagram = Voronoi([[0.2,0.4],[0.4,0.8],[0.7,0.3]])
    # print(diagram._edgelist)
    # print(diagram._status)
    # diagram = Voronoi([[0.86, 0.37], [0.38, 0.21], [0.1, 0.51], [0.81, 0.68]])
    # print(diagram._edgelist)
    # print(diagram._status)
    # testNumPoints(4)

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- null checking the methods of BinTree
- circle event when arc is not under the site
"""
