import matplotlib.pyplot as plt
import numpy as np
import Calc
from matplotlib.collections import LineCollection as LineColl
from functools import reduce
from BinTree import BinTree
from DCEL import DCEL
from Heap import Heap

class Diagram:
    def __init__(self, points):
        self._events = Heap()
        self._tree = BinTree()
        self._edgelist = DCEL()
        for p in points:
            self._events.insert('site', p)
        while not self._events.empty():
            event = self._events.removeMax()
            if event._kind == 'site':
                self.handleSiteEvent(event)
            else:
                self.handleCircleEvent(event._leaf)
        self.pruneEdges(points)

    def handleSiteEvent(self, event):
        if self._tree.empty():
            self._tree.addRoot({'site': event._site})
            return
        oldNode = self._tree.findArc(event._site)
        self.removeFalseAlarm(oldNode)

        # these local vars are for readability
        oldSite = oldNode.data['site']
        newSite = event._site

        # add subtree
        leftBp = self._tree.addRight(oldNode, {'bp': (oldSite, newSite)})
        rightBp = self._tree.addRight(leftBp, {'bp': (newSite, oldSite)})
        oldArcLeft = self._tree.addLeft(leftBp, {'site': oldSite})
        newArc = self._tree.addLeft(rightBp, {'site': newSite})
        oldArcRight = self._tree.addRight(rightBp, {'site': oldSite})
        self._tree.replaceWithChild(oldNode, leftBp)

        # add edge
        p = Calc.getProjection(newSite, oldSite)
        leftBp.data['edge'] = self._edgelist.addEdge(p)
        rightBp.data['edge'] = leftBp.data['edge']._twin
        self._edgelist.initSiteVector(leftBp.data['edge'], oldSite, newSite)

        self.checkNewCircle(self._tree.prevLeaf(oldArcLeft), oldArcLeft, newArc)
        self.checkNewCircle(newArc, oldArcRight, self._tree.nextLeaf(oldArcRight))

    def handleCircleEvent(self, leaf):
        # these local vars are for readability
        nextLeaf = self._tree.nextLeaf(leaf)
        prevLeaf = self._tree.prevLeaf(leaf)
        nextBp = self._tree.successor(leaf)
        prevBp = self._tree.predecessor(leaf)
        leftSite = prevLeaf.data['site']
        centerSite = leaf.data['site']
        rightSite = nextLeaf.data['site']
        coord = Calc.circleCenter(leftSite, centerSite, rightSite)

        self._tree.remove(leaf)

        prevBp.data['edge']._twin._origin = coord
        nextBp.data['edge']._twin._origin = coord
        newlyAdjacent = (leftSite, rightSite)

        # readjusting tree
        nextIsParent = (nextBp == leaf._parent)
        toRemove = nextBp if nextIsParent else prevBp
        remainingBp = prevBp if nextIsParent else nextBp
        otherChild = nextBp._right if nextIsParent else prevBp._left
        self._tree.replaceWithChild(toRemove, otherChild)
        remainingBp.data['bp'] = newlyAdjacent

        # add edge
        vert = self._edgelist.addVertex(coord)
        newHalf = self._edgelist.addEdge(coord)
        vert._incidentEdge = newHalf
        remainingBp.data['edge'] = newHalf
        bottom = Calc.circleBottom(leftSite, centerSite, rightSite)
        self._edgelist.initCircleVector(newHalf, newlyAdjacent, bottom)

        self.removeFalseAlarm(nextLeaf)
        self.removeFalseAlarm(prevLeaf)

        self.checkNewCircle(self._tree.prevLeaf(prevLeaf), prevLeaf, nextLeaf)
        self.checkNewCircle(prevLeaf, nextLeaf, self._tree.nextLeaf(nextLeaf))

    def removeFalseAlarm(self, leaf):
        if leaf.data['event'] != None:
            self._events.remove(leaf.data['event'])
            leaf.data['event'] = None

    def checkNewCircle(self, left, middle, right):
        if (left is None) or (right is None):
            return
        e1 = self._tree.successor(middle).data['edge']
        e2 = self._tree.predecessor(middle).data['edge']
        if Calc.converge(e1._point, e1._vector, e2._point, e2._vector):
            p = Calc.circleBottom(left.data['site'], middle.data['site'], right.data['site'])
            event = self._events.insert('circle', middle, p)
            middle.data['event'] = event

    def pruneEdges(self, points):
        toRemove = set()
        for e in self._edgelist.edges():
            t = e._twin
            exists = lambda x: x is not None # function which determines existence
            if not (exists(e._origin) or exists(t._origin)):
                if Calc.isOutside(e._point):
                    inward = e if (Calc.extend(t._point, t._vector) is None) else t
                    inward._origin = Calc.shorten(inward._point, inward._vector)
                    inward._twin._origin = Calc.extend(inward._point, inward._vector)
                else:
                    e._origin = Calc.shorten(e._point, e._vector)
                    t._origin = Calc.shorten(t._point, t._vector)
            else:
                if Calc.pointsOutward(e._origin, e._vector) or Calc.pointsOutward(t._origin, t._vector):
                    toRemove.add(e)
                    toRemove.add(t)
                elif exists(e._origin) and exists(t._origin):
                    for outside in filter(lambda x: Calc.isOutside(x._origin), [e,t]):
                        outside._origin = Calc.shorten(outside._origin, outside._vector)
                else: # only one exists
                    existing = e if not (e._origin is None) else t
                    existing._twin._origin = Calc.extend(existing._origin, existing._vector)
                    if Calc.isOutside(existing._origin):
                        existing._origin = Calc.shorten(existing._origin, existing._vector)
        for e in toRemove:
            self._edgelist.removeEdge(e)

    def perimeter(self):
        halfLength = lambda acc,x: acc+(Calc.dist(x._origin,x.dest())/2.0)
        return 4 + reduce(halfLength, self._edgelist.edges(), 0)

    def plot(self, sites=None):
        # plot sites
        if (sites is not None) and (len(sites) < 300):
            sites = np.array(sites)
            plt.plot(sites[:,0], sites[:,1], 'ro')

            vertices = np.array([e._origin for e in self._edgelist.edges()])
            plt.plot(vertices[:,0], vertices[:,1], 'bo')

        edges = [[e._origin, e.dest()] for e in self._edgelist.edges()]
        edges = LineColl(edges)
        plt.gca().add_collection(edges)

        plt.axis([0, 1, 0, 1])
        plt.show()

if __name__ == "__main__":
    points = Calc.getSitePoints(1014)
    diagram = Diagram(points)
    print('perimeter: ' + str(Calc.roundBetter(diagram.perimeter())))
    diagram.plot(points)

