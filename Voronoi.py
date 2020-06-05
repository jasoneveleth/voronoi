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


        


def handleCircleEvent(leaf):
    pass


"""
TODO
- Handle Site Event
- Handle Circle Event
- Cobble together the diagram
"""

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear
- getting next child of last node
- null checking the methods of BinTree
"""