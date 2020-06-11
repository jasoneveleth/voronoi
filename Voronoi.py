from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap
from random import random

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
        # TODO the remaining internal nodes of BinTree are infinite half edges
        # TODO compute a box and attach half-infinite edges to boudning box by updating appropriately
        # TODO traverse the half edges to add the cell records and the pointers to and from them
        

    def handleSiteEvent(self, event):
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
        oldNode._halfedge = self._edgelist.addEdge()

        newBreakpoint = self._status.addRight(oldNode, 'breakpoint', [event._site, oldNode._site], self._edgelist.addEdge())
        oldArcLeft = self._status.addLeft(oldNode, 'arc', oldNode._site)
        newArc = self._status.addLeft(newBreakpoint, 'arc', event._site)
        oldArcRight = self._status.addRight(newBreakpoint, 'arc', oldNode._site)

        oldNode._site = None

        # update edges
        oldNode._halfedge._twin = newBreakpoint._halfedge
        newBreakpoint._halfedge._twin = oldNode._halfedge
        
        # check for new circle self._events
        if not self._status.isFirst(oldArcLeft):
            toLeft = self._status.prevLeaf(oldArcLeft)
            self.checkNewCircle(toLeft, oldArcLeft, newArc)

        if not self._status.isLast(oldArcRight):
            toRight = self._status.nextLeaf(oldArcRight)
            self.checkNewCircle(newArc, oldArcRight, toRight)
        

    def handleCircleEvent(self, leaf):
        self._status.remove(leaf)
        nextLeaf = self._status.nextLeaf(leaf)
        prevLeaf = self._status.prevLeaf(leaf)
        parent = leaf._parent
        grandparent = parent._parent

        # readjusting tree
        if self._status.isLeftChild(parent):
            grandparent._left = parent._left
            grandparent._breakpoint = [parent._breakpoint[0], grandparent._breakpoint[1]]
        else:
            grandparent._right = parent._right
            grandparent._breakpoint = [grandparent._breakpoint[0], parent._breakpoint[1]]
        
        self._status._size -= 1

        # remove false alarm circle self._events
        if nextLeaf._event != None:
            self._events.remove(nextLeaf._event)
            nextLeaf._event = None
        if prevLeaf._event != None:
            self._events.remove(prevLeaf._event)
            prevLeaf._event = None

        print(self._status)

        # getting point and making vertex
        coord = self.circleCenter(prevLeaf._site, leaf._site, nextLeaf._site)
        vert = self._edgelist.addVertex(coord)

        # making edges
        newHalf = self._edgelist.addEdge()
        newHalf._twin = self._edgelist.addEdge()
        newHalf._twin._twin = newHalf
        newHalf._origin = coord

        # it needs one incident edge
        vert._incidentEdge = newHalf

        # adding origin
        oldHalfParent = parent._halfedge
        oldHalfGrand = grandparent._halfedge
        grandparent._halfedge = newHalf
        if oldHalfParent._origin != None:
            oldHalfParent._origin = coord
        else:
            oldHalfParent._twin._origin = coord

        if oldHalfGrand._origin != None:
            oldHalfGrand._origin = coord
        else:
            oldHalfGrand._twin._origin = coord

        # adding next and prev to the edges that are leaving
        if oldHalfParent._origin != coord:
            if oldHalfGrand._origin != coord:
                oldHalfParent._next = oldHalfGrand._twin
                oldHalfParent._twin._prev = oldHalfGrand
                oldHalfGrand._next = oldHalfParent._twin
                oldHalfGrand._twin._prev = oldHalfParent
            else:
                oldHalfParent._next = oldHalfGrand
                oldHalfParent._twin._prev = oldHalfGrand._twin
                oldHalfGrand._prev = oldHalfParent
                oldHalfGrand._twin._next = oldHalfParent._twin
        else:
            if oldHalfGrand._origin != coord:
                oldHalfParent._prev = oldHalfGrand._twin
                oldHalfParent._twin._next = oldHalfGrand
                oldHalfGrand._prev = oldHalfParent._twin
                oldHalfGrand._twin._next = oldHalfParent
            else:
                oldHalfParent._prev = oldHalfGrand
                oldHalfParent._twin._next = oldHalfGrand._twin
                oldHalfGrand._next = oldHalfParent
                oldHalfGrand._twin._prev = oldHalfParent._twin

        # check for circle self._events
        if not self._status.isFirst(prevLeaf):
            toLeft = self._status.prevLeaf(prevLeaf)
            self.checkNewCircle(toLeft, prevLeaf, nextLeaf)
        if not self._status.isLast(nextLeaf):
            toRight = self._status.nextLeaf(nextLeaf)
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
    for _ in range(n):
        points.append([rand(),rand()])
    print(points)
    diagram = Voronoi(points)
    print(diagram._edgelist)
    print(diagram._status)

if __name__ == "__main__":
    # self._edgelist = makeself._edgelist([[0.3,0.7],[0.7,0.3]])
    # print(self._edgelist)
    # print(self._status)
    diagram = Voronoi([[0.2,0.4],[0.4,0.8],[0.7,0.3]])
    print(diagram._edgelist)
    print(diagram._status)
    # testNumPoints(4)


"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- null checking the methods of BinTree
- circle event when arc is not under the site
"""