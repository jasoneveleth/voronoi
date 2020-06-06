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
            handleCircleEvent(event)
    # TODO compute a box and attach half-infinite edges to boudning box by updating appropriately
    # TODO traverse the half edges to add the cell records and the pointers to and from them
    

def handleSiteEvent(event):
    if status.empty():
        status.addRoot(True, event._site, event)
        return
    oldNode = status.findArc(event._site)
    if oldNode._event != None: # this assumes the _event is a circle event (which is true: nodes either store circle events or halfedges)
        events.remove(oldNode._event)
        oldNode._event = None
    if oldNode._parent._right == oldNode:
        firBranch = status.addRight(oldNode._parent, 'breakpoint', [oldNode._site, event._site], diagram.addEdge())
    else:
        firBranch = status.addRight(oldNode._parent, 'breakpoint', [oldNode._site, event._site], diagram.addEdge())
    secBranch = status.addRight(firBranch, 'breakpoint', [event._site, oldNode._site], diagram.addEdge())
    firBranch._halfedge._twin = secBranch._halfedge
    secBranch._halfedge._twin = firBranch._halfedge
    leafl = status.addLeft(firBranch, 'arc', oldNode._site)
    leafm = status.addLeft(secBranch, 'arc', event._site)
    leafr = status.addRight(secBranch, 'arc', oldNode._site)
    
    # check for new circle events
    toLeft = status.prevLeaf(leafl)
    if leafl._site[1] >= leafm._site[1] and leafl._site[1] >= toLeft._site[1]:
        e = events.insert('circle event', leafl, toLeft._site, leafl._site, leafm._site)
        leafl._event = e
    toRight = status.nextLeaf(leafr)
    if leafr._site[1] >= leafm._site[1] and leafr._site[1] >= toRight._site[1]:
        e = events.insert('circle event', leafr, leafm._site, leafr._site, toRight._site)
        leafr._event = e

def handleCircleEvent(event):
    leaf = event._leaf
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

    e1 = nextLeaf._event
    events.remove(e1)
    nextLeaf._event = None
    e2 = prevLeaf._event
    events.remove(e2)
    prevLeaf._event = None

    # getting point and making vertex
    coord = event._point
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
    half1 = p1._halfedge
    half2 = p2._halfedge
    p2._halfedge = edge1
    if half1._origin != None:
        half1._origin = coord
    else:
        half1._twin._origin = coord
    if half2._origin != None:
        half2._origin = coord
    else:
        half2._twin._origin = coord

    # adding next and prev to what we know
    

    # Update the records
    # Check the new triple of consecutive arcs that has the former left neighbor of α as its middle arc to see if the two breakpoints of the triple converge.
    # If so, insert the corresponding circle event into Q. and set pointers between the new circle event in Q and the corresponding leaf of T. 
    # Do the same for the triple where the former right neighbor is the middle arc.



"""
TODO
- Next leaf and prev leaf need to handle when there isn't a left leaf to an internal node
- Handle Circle Event
- Cobble together the diagram
"""

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- getting next child of last node
- null checking the methods of BinTree
- circle event when arc is not under the site
"""