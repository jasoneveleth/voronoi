from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap

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
        status.addRoot(True, event._site, event)
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

    secBranch = status.addRight(oldNode, 'breakpoint', [event._site, oldNode._site], diagram.addEdge())
    leafl = status.addLeft(oldNode, 'arc', oldNode._site)
    leafm = status.addLeft(secBranch, 'arc', event._site)
    leafr = status.addRight(secBranch, 'arc', oldNode._site)
    
    oldNode._site = None

    # update edges
    oldNode._halfedge._twin = secBranch._halfedge
    secBranch._halfedge._twin = oldNode._halfedge
    
    # check for new circle events
    toLeft = status.prevLeaf(leafl)
    if leafl._site[1] >= leafm._site[1] and leafl._site[1] >= toLeft._site[1]:
        e = events.insert('circle event', leafl, toLeft._site, leafl._site, leafm._site)
        leafl._event = e
    toRight = status.nextLeaf(leafr)
    if leafr._site[1] >= leafm._site[1] and leafr._site[1] >= toRight._site[1]:
        e = events.insert('circle event', leafr, leafm._site, leafr._site, toRight._site)
        leafr._event = e

def handleCircleEvent(leaf):
    status.remove(leaf)
    nextLeaf = status.nextLeaf(leaf)
    prevLeaf = status.prevLeaf(leaf)
    p1 = leaf._parent
    p2 = p1._parent


    if p2._left == p1:
        p2._breakpoint = [p1._breakpoint[0], p2._breakpoint[1]]
        p2._left = p1._left
    else:
        p2._breakpoint = [p2._breakpoint[0], p1._breakpoint[1]]
        p2._right = p1._right

    # remove false alarm circle events
    e1 = nextLeaf._event
    events.remove(e1)
    nextLeaf._event = None
    e2 = prevLeaf._event
    events.remove(e2)
    prevLeaf._event = None

    # getting point and making vertex
    coord = leaf._event._point
    vert = diagram.addVertex(coord)

    # making edges
    edge1 = diagram.addEdge()
    edge2 = diagram.addEdge()
    edge1._twin = edge2
    edge2._twin = edge1
    edge1._origin = coord

    # it needs one incident edge
    vert._incidentEdge = edge1

    # adding origin
    oldHalf1 = p1._halfedge
    odlHalf2 = p2._halfedge
    p2._halfedge = edge1
    if oldHalf1._origin != None:
        oldHalf1._origin = coord
    else:
        oldHalf1._twin._origin = coord
    if odlHalf2._origin != None:
        odlHalf2._origin = coord
    else:
        odlHalf2._twin._origin = coord

    # adding next and prev to the edges that are leaving
    if oldHalf1._origin != coord:
        if odlHalf2._origin != coord:
            oldHalf1._next = odlHalf2._twin
            oldHalf1._twin._prev = odlHalf2

            odlHalf2._next = oldHalf1._twin
            odlHalf2._twin._prev = oldHalf1
        else:
            oldHalf1._next = odlHalf2
            oldHalf1._twin._prev = odlHalf2._twin

            odlHalf2._prev = oldHalf1
            odlHalf2._twin._next = oldHalf1._twin
    else:
        if odlHalf2._origin != coord:
            oldHalf1._prev = odlHalf2._twin
            oldHalf1._twin._next = odlHalf2

            odlHalf2._prev = oldHalf1._twin
            odlHalf2._twin._next = oldHalf1
        else:
            oldHalf1._prev = odlHalf2
            oldHalf1._twin._next = odlHalf2._twin

            odlHalf2._next = oldHalf1
            odlHalf2._twin._prev = oldHalf1._twin

    # check for circle events
    toLeft = status.prevLeaf(prevLeaf)
    if prevLeaf._site[1] >= nextLeaf._site[1] and prevLeaf._site[1] >= toLeft._site[1]:
        e = events.insert('circle event', prevLeaf, toLeft._site, prevLeaf._site, nextLeaf._site)
        prevLeaf._event = e
    toRight = status.nextLeaf(nextLeaf)
    if nextLeaf._site[1] >= prevLeaf._site[1] and nextLeaf._site[1] >= toRight._site[1]:
        e = events.insert('circle event', nextLeaf, prevLeaf._site, nextLeaf._site, toRight._site)
        nextLeaf._event = e



"""
TODO
- Cobble together the diagram
"""

"""
Possible bugs: 
- Next leaf and prev leaf need to handle when there isn't a left leaf to an internal node
- if the sites fed to the circle algorithm are colinear
- getting next child of last node
- null checking the methods of BinTree
- circle event when arc is not under the site
"""