from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap
from random import random

events = Heap()
status = BinTree()
diagram = DCEL()

def makeDiagram(points):
    """takes in a list of points (lists)
    returns the doubly connected edge list"""
    for p in points:
        events.insert('site event', p)
        
    while not events.empty():
        event = events.removeMax()
        if event._kind == 'site event':
            handleSiteEvent(event)
        else:
            handleCircleEvent(event._leaf)
    # TODO the remaining internal nodes of BinTree are infinite half edges
    # TODO compute a box and attach half-infinite edges to boudning box by updating appropriately
    # TODO traverse the half edges to add the cell records and the pointers to and from them
    return diagram
    

def handleSiteEvent(event):
    if status.empty():
        status.addRoot('arc', event._site, None)
        return
    oldNode = status.findArc(event._site)

    # Remove false alarm
    if oldNode._event != None:
        events.remove(oldNode._event)
        oldNode._event = None

    # add subtree
    oldNode._version = 'breakpoint'
    oldNode._breakpoint = [oldNode._site, event._site]
    oldNode._halfedge = diagram.addEdge()

    newBreakpoint = status.addRight(oldNode, 'breakpoint', [event._site, oldNode._site], diagram.addEdge())
    oldArcLeft = status.addLeft(oldNode, 'arc', oldNode._site)
    newArc = status.addLeft(newBreakpoint, 'arc', event._site)
    oldArcRight = status.addRight(newBreakpoint, 'arc', oldNode._site)

    oldNode._site = None

    # update edges
    oldNode._halfedge._twin = newBreakpoint._halfedge
    newBreakpoint._halfedge._twin = oldNode._halfedge
    
    # check for new circle events
    if not status.isFirst(oldArcLeft):
        toLeft = status.prevLeaf(oldArcLeft)
        checkNewCircle(toLeft, oldArcLeft, newArc)

    if not status.isLast(oldArcRight):
        toRight = status.nextLeaf(oldArcRight)
        checkNewCircle(newArc, oldArcRight, toRight)
    
def checkNewCircle(left, center, right):
    if center._site[1] >= right._site[1] and center._site[1] >= left._site[1]:
        e = events.insert('circle event', center, left._site, center._site, right._site)
        center._event = e

def handleCircleEvent(leaf):
    status.remove(leaf)
    nextLeaf = status.nextLeaf(leaf)
    prevLeaf = status.prevLeaf(leaf)
    parent = leaf._parent
    grandparent = parent._parent

    # readjusting tree
    if status.isLeftChild(parent):
        grandparent._left = parent._left
        grandparent._breakpoint = [parent._breakpoint[0], grandparent._breakpoint[1]]
    else:
        grandparent._right = parent._right
        grandparent._breakpoint = [grandparent._breakpoint[0], parent._breakpoint[1]]
    
    status._size -= 1

    # remove false alarm circle events
    if nextLeaf._event != None:
        events.remove(nextLeaf._event)
        nextLeaf._event = None
    if prevLeaf._event != None:
        events.remove(prevLeaf._event)
        prevLeaf._event = None

    # getting point and making vertex
    coord = circle(prevLeaf._site, leaf._site, nextLeaf._site)
    vert = diagram.addVertex(coord)

    # making edges
    newHalf = diagram.addEdge()
    newHalf._twin = diagram.addEdge()
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

    # check for circle events
    if not status.isFirst(prevLeaf):
        toLeft = status.prevLeaf(prevLeaf)
        checkNewCircle(toLeft, prevLeaf, nextLeaf)
    if not status.isLast(nextLeaf):
        toRight = status.nextLeaf(nextLeaf)
        checkNewCircle(prevLeaf, nextLeaf, toRight)

def rand():
    return round(random()*100)/100.0

def circle(a, b, c):
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    x = (1.0/d)*((a[0]**2 + a[1]**2)*(b[1] - c[1]) + (b[0]**2 + b[1]**2)*(c[1] - a[1]) + (c[0]**2 + c[1]**2)*(a[1] - b[1]))
    y = (1.0/d)*((a[0]**2 + a[1]**2)*(c[0] - b[0]) + (b[0]**2 + b[1]**2)*(a[0] - c[0]) + (c[0]**2 + c[1]**2)*(b[0] - a[0]))
    return [x,y]

if __name__ == "__main__":
    # diagram = makeDiagram([[0.3,0.7],[0.7,0.3],[0.5,0.6]])
    # print(diagram)
    # print(status)
    points = []
    for i in range(4):
        points.append([rand(),rand()])
    print(points)
    diagram = makeDiagram(points)
    print(diagram)
    print(status)

"""
TODO
- Cobble together the diagram
"""

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- null checking the methods of BinTree
- circle event when arc is not under the site
"""