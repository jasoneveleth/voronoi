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
    p1 = leaf._parent
    p2 = leaf._parent
    p1._breakpoint = None # TODO
    p2._breakpoint = None # TODO
    # Update the tuples representing the breakpoints at the internal nodes.

    e1 = status.nextLeaf(leaf)._event
    events.remove(e1)
    status.nextLeaf(leaf)._event = None
    e2 = status.prevLeaf(leaf)._event
    events.remove(e2)
    status.prevLeaf(leaf)._event = None

    event._point = 
    # Add the center of the circle causing the event as a vertex record to the doubly-connected edge list D storing the Voronoi diagram under construc- tion
    # Create two half-edge records corresponding to the new breakpoint of the beach line. Set the pointers between them appropriately.
    # Attach the three new records to the half-edge records that end at the vertex
    # Check the new triple of consecutive arcs that has the former left neighbor of α as its middle arc to see if the two breakpoints of the triple converge.
    # If so, insert the corresponding circle event into Q. and set pointers between the new circle event in Q and the corresponding leaf of T. 
    # Do the same for the triple where the former right neighbor is the middle arc.



"""
TODO
- Handle Circle Event
- Cobble together the diagram
"""

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- getting next child of last node
- null checking the methods of BinTree
"""