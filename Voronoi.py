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
    node = status.findArc(event._site)
    if node._event != None and node._event._kind == 'circle event':
        events.remove(node._event)
        node._event = None
    parent = node._parent
    if parent._left == node:
        firBranch = status.addRight(parent, 'breakpoint', [node._site, event._site], diagram.addEdge())
        secBranch = status.addRight(firBranch, 'breakpoint', [event._site, node._site], diagram.addEdge())
        firBranch._halfedge._twin = secBranch._halfedge
        secBranch._halfedge._twin = firBranch._halfedge
        leafl = status.addLeft(firBranch, 'arc', node._site)
        leafm = status.addLeft(secBranch, 'arc', event._site)
        leafr = status.addRight(secBranch, 'arc', node._site)
        


def handleCircleEvent(leaf):
    pass


"""
TODO
- Successor for BinTree
- figure out events for leaf nodes in handlesiteevent
- Handle Site Event
- Handle Circle Event
- Cobble together the diagram
"""

"""
Possible bugs: 
- if the sites fed to the circle algorithm are colinear

Unlikely
- circle lowest point algorithm doesn't work
"""