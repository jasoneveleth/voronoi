import voronoi.calc as Calc
from functools import reduce
from voronoi.bintree import BinTree
from voronoi.edgelist import DCEL
from voronoi.heap import Heap

def fortunes(sites):
    heap = Heap()
    tree = BinTree()
    edgelist = DCEL()
    for p in sites:
        heap.insert('site', p)
    first, second = heap.bigPeek()
    if first._key == second._key:
        specialCode(tree, heap, edgelist)
    while not heap.empty():
        event = heap.removeMax()
        if event._kind == 'site':
            handleSiteEvent(event, tree, heap, edgelist)
        else:
            handleCircleEvent(event._leaf, tree, heap, edgelist)
    return pruneEdges(edgelist)

def newfortunes(sites):
    '''makes faces'''
    heap = Heap()
    tree = BinTree()
    edgelist = DCEL()
    for p in sites:
        heap.insert('site', p)
    first, second = heap.bigPeek()
    if first._key == second._key:
        specialCode(tree, heap, edgelist)
    while not heap.empty():
        event = heap.removeMax()
        if event._kind == 'site':
            handleSiteEvent(event, tree, heap, edgelist)
        else:
            handleCircleEvent(event._leaf, tree, heap, edgelist)
    edges = buildFacesPruneEdges(edgelist)
    getFaces(edgelist)
    for f in edgelist.faces():
        print()
        print(f)
    return edges

def performantPerimeter(sites):
    heap = Heap()
    tree = BinTree()
    edgelist = DCEL()
    for p in sites:
        heap.insert('site', p)
    while not heap.empty():
        event = heap.removeMax()
        if event._kind == 'site':
            handleSiteEvent(event, tree, heap, edgelist)
        else:
            handleCircleEvent(event._leaf, tree, heap, edgelist)
    return pruneEdgeReturnPerimeter(edgelist.edges())

def handleSiteEvent(event, tree, heap, edgelist):
    if tree.empty():
        tree.addRoot({'site': event._site})
        return
    oldNode = tree.findArc(event._site)
    removeFalseAlarm(oldNode, heap)

    # these local vars are for readability
    oldSite = oldNode.data['site']
    newSite = event._site

    # add subtree
    leftBp = tree.addRight(oldNode, {'bp': (oldSite, newSite)})
    rightBp = tree.addRight(leftBp, {'bp': (newSite, oldSite)})
    oldArcLeft = tree.addLeft(leftBp, {'site': oldSite})
    newArc = tree.addLeft(rightBp, {'site': newSite})
    oldArcRight = tree.addRight(rightBp, {'site': oldSite})
    tree.replaceWithChild(oldNode, leftBp)

    # add edge
    p = Calc.getProjection(newSite, oldSite)
    leftBp.data['edge'] = edgelist.addEdge(p)
    rightBp.data['edge'] = leftBp.data['edge']._twin
    edgelist.initSiteVector(leftBp.data['edge'], oldSite, newSite)

    checkNewCircle(tree.prevLeaf(oldArcLeft), oldArcLeft, newArc, tree, heap)
    checkNewCircle(newArc, oldArcRight, tree.nextLeaf(oldArcRight), tree, heap)

def handleCircleEvent(leaf, tree, heap, edgelist):
    # these local vars are for readability
    nextLeaf = tree.nextLeaf(leaf)
    prevLeaf = tree.prevLeaf(leaf)
    nextBp = tree.successor(leaf)
    prevBp = tree.predecessor(leaf)
    leftSite = prevLeaf.data['site']
    centerSite = leaf.data['site']
    rightSite = nextLeaf.data['site']
    coord = Calc.circleCenter(leftSite, centerSite, rightSite)

    tree.remove(leaf)

    prevBp.data['edge']._twin._origin = coord
    nextBp.data['edge']._twin._origin = coord
    newlyAdjacent = (leftSite, rightSite)

    # readjusting tree
    nextIsParent = (nextBp == leaf._parent)
    toRemove = nextBp if nextIsParent else prevBp
    remainingBp = prevBp if nextIsParent else nextBp
    otherChild = nextBp._right if nextIsParent else prevBp._left
    tree.replaceWithChild(toRemove, otherChild)
    remainingBp.data['bp'] = newlyAdjacent

    # add edge
    newHalf = edgelist.addEdge(coord)
    remainingBp.data['edge'] = newHalf
    bottom = Calc.circleBottom(leftSite, centerSite, rightSite)
    edgelist.initCircleVector(newHalf, newlyAdjacent, bottom)

    removeFalseAlarm(nextLeaf, heap)
    removeFalseAlarm(prevLeaf, heap)

    checkNewCircle(tree.prevLeaf(prevLeaf), prevLeaf, nextLeaf, tree, heap)
    checkNewCircle(prevLeaf, nextLeaf, tree.nextLeaf(nextLeaf), tree, heap)

def specialCode(tree, heap, edgelist):
    first = heap.removeMax()
    second = heap.removeMax()
    root = tree.addRoot({'bp': (first._site, second._site)})
    tree.addLeft(root, {'site': first._site})
    tree.addRight(root, {'site': second._site})

    # add edge
    p = ((first._site[0] + second._site[0]) / 2.0,9999999999999) # could be wrong to use infinity
    root.data['edge'] = edgelist.addEdge(p)
    edgelist.initSiteVector(root.data['edge'], first._site, second._site)

def removeFalseAlarm(leaf, heap):
    if leaf.data['event'] != None:
        heap.remove(leaf.data['event'])
        leaf.data['event'] = None

def checkNewCircle(left, middle, right, tree, heap):
    if (left is None) or (right is None):
        return
    e1 = tree.successor(middle).data['edge']
    e2 = tree.predecessor(middle).data['edge']
    if Calc.converge(e1._point, e1._vector, e2._point, e2._vector):
        p = Calc.circleBottom(left.data['site'], middle.data['site'], right.data['site'])
        event = heap.insert('circle', middle, p)
        middle.data['event'] = event

def pruneEdgeReturnPerimeter(setofEdges):
    """takes set of incomplete halfedge objects,
        returns set of pairs of tuples"""
    perimeter = 0
    exists = lambda x: x is not None # function which determines existence
    for e in setofEdges:
        t = e._twin
        if (not exists(e._origin)) and (not exists(t._origin)):
            if Calc.isOutside(e._point):
                inward = e if (Calc.extend(t._point, t._vector) is None) else t
                inward._origin = Calc.shorten(inward._point, inward._vector)
                inward._twin._origin = Calc.extend(inward._point, inward._vector)
            else:
                e._origin = Calc.shorten(e._point, e._vector)
                t._origin = Calc.shorten(t._point, t._vector)
        else:
            if Calc.pointsOutward(e._origin, e._vector) or Calc.pointsOutward(t._origin, t._vector):
                continue
            elif exists(e._origin) and exists(t._origin):
                for outside in filter(lambda x: Calc.isOutside(x._origin), [e,t]):
                    outside._origin = Calc.shorten(outside._origin, outside._vector)
            else: # only one exists
                existing = e if not (e._origin is None) else t
                existing._twin._origin = Calc.extend(existing._origin, existing._vector)
                if Calc.isOutside(existing._origin):
                    existing._origin = Calc.shorten(existing._origin, existing._vector)
        perimeter += Calc.dist(t._origin, e._origin)
    return 4 + (perimeter/2)

def buildFacesPruneEdges(edgelist):
    setofEdges = edgelist.edges()
    """takes set of incomplete halfedge objects,
        returns set of pairs of tuples"""
    newEdges = set()
    exists = lambda x: x is not None # function which determines existence
    pointsOnBoundary = []
    for e in setofEdges:
        t = e._twin
        if (not exists(e._origin)) and (not exists(t._origin)):
            if Calc.isOutside(e._point):
                inward = e if (Calc.extend(t._point, t._vector) is None) else t
                inward._origin = Calc.shorten(inward._point, inward._vector)
                inward._twin._origin = Calc.extend(inward._point, inward._vector)
                pointsOnBoundary.append(inward._origin)
                pointsOnBoundary.append(inward._twin._origin)
            else:
                e._origin = Calc.shorten(e._point, e._vector)
                t._origin = Calc.shorten(t._point, t._vector)
                pointsOnBoundary.append(e._origin)
                pointsOnBoundary.append(t._origin)
        else:
            if Calc.pointsOutward(e._origin, e._vector) or Calc.pointsOutward(t._origin, t._vector):
                continue
            elif exists(e._origin) and exists(t._origin):
                for outside in filter(lambda x: Calc.isOutside(x._origin), [e,t]):
                    outside._origin = Calc.shorten(outside._origin, outside._vector)
                    pointsOnBoundary.append(outside._origin)
            else: # only one exists
                existing = e if not (e._origin is None) else t
                existing._twin._origin = Calc.extend(existing._origin, existing._vector)
                if Calc.isOutside(existing._origin):
                    existing._origin = Calc.shorten(existing._origin, existing._vector)
                    pointsOnBoundary.append(existing._origin)
                    pointsOnBoundary.append(existing._twin._origin)
        if not (t._origin, e._origin) in newEdges:
            newEdges.add((e._origin,t._origin))
    # ADDING BOUNDARY EDGES {{{{{{{
    x0 = []
    x1 = []
    y0 = []
    y1 = []
    for p in pointsOnBoundary:
        if p[0] == 0:
            x0.append(p)
        elif p[0] == 1:
            x1.append(p)
        elif p[1] == 0:
            y0.append(p)
        elif p[1] == 1:
            y1.append(p)
        else:
            raise TypeError(f'{p} not on boundary')
    x0 = sorted(x0,key=lambda x: (-x[1]))
    y0 = sorted(y0,key=lambda x: (x[0]))
    x1 = sorted(x1,key=lambda x: (x[1]))
    y1 = sorted(y1,key=lambda x: (-x[0]))
    pointsOnBoundary = y0 + x1 + y1 + x0
    total = len(pointsOnBoundary)
    for i,p in enumerate(pointsOnBoundary):
        e = edgelist.addEdge(p)
        e._origin = p
        # the modulus is so it wraps back to 0
        e._twin._origin = pointsOnBoundary[(i+1)%total]
    # }}}}}}}
    return newEdges

def pruneEdges(setofEdges):
    """takes set of incomplete halfedge objects,
        returns set of pairs of tuples"""
    newEdges = set()
    exists = lambda x: x is not None # function which determines existence
    for e in setofEdges:
        t = e._twin
        if (not exists(e._origin)) and (not exists(t._origin)):
            if Calc.isOutside(e._point):
                inward = e if (Calc.extend(t._point, t._vector) is None) else t
                inward._origin = Calc.shorten(inward._point, inward._vector)
                inward._twin._origin = Calc.extend(inward._point, inward._vector)
            else:
                e._origin = Calc.shorten(e._point, e._vector)
                t._origin = Calc.shorten(t._point, t._vector)
        else:
            if Calc.pointsOutward(e._origin, e._vector) or Calc.pointsOutward(t._origin, t._vector):
                continue
            elif exists(e._origin) and exists(t._origin):
                for outside in filter(lambda x: Calc.isOutside(x._origin), [e,t]):
                    outside._origin = Calc.shorten(outside._origin, outside._vector)
            else: # only one exists
                existing = e if not (e._origin is None) else t
                existing._twin._origin = Calc.extend(existing._origin, existing._vector)
                if Calc.isOutside(existing._origin):
                    existing._origin = Calc.shorten(existing._origin, existing._vector)
        if not (t._origin, e._origin) in newEdges:
            newEdges.add((e._origin,t._origin))
    return newEdges

def getFaces(edgelist):
    visited = set()
    edges = list(edgelist.edges())
    total = len(edges)
    while len(visited) < total:
        # find edges
        i = 0
        e = edges[0]
        while e in visited:
            i += 1
            e = edges[i]
        face = edgelist.addFace()
        face.addEdge(e)
        # find two edges (at h's destination)
        dest = e.dest()
        outgoing = []
        print('LOOKING FOR:', e.dest())
        print()
        print('STARTING')
        print()
        for f in edges:
            print(f)
            if f._origin == dest:
                print('^^^^ chosen')
                outgoing.append(f)
        # calculate angles
        # take left edge
        normalizedE = Calc.subtract(e._origin, e.dest())
        normalizedVectors = list(map(outgoing, lambda x: Calc.subtract(x._origin, x.dest())))
        maxAngle = -99999
        index = None
        for i,nvect in enumerate(normalizedVectors):
            if Calc.angleBetween(normalizedE, nvect) > maxAngle:
                index = i
                maxAngle = Calc.angleBetween(normalizedE, nvect)
        if Calc.angleBetween(normalizedVector0, normalizedVector1) > Calc.angleBetween(normalizedVector0, normalizedVector2):
            face.addEdge(v1)
            nextEdge = v1
        else:
            face.addEdge(v2)
            nextEdge = v2
        # update visited set
        visited.add(e)
        visited.add(v2)

def getPerimeter(edges):
    fullLength = lambda acc,x: acc+Calc.dist(x[0],x[1])
    return 4 + reduce(fullLength, edges, 0)
