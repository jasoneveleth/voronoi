from math import ceil
import Calc

class Event:
    def __init__(self, index, kind, data, p1=None, p2=None, p3=None):
        self._kind = kind
        self._index = index
        if self._kind == 'site':
            self._site = data
        elif self._kind == 'circle':
            self._leaf = data
            self._point = Calc.circleBottom(p1, p2, p3)
        else:
            raise TypeError("yoinks, non-event")

    def key(self):
        if self._kind == 'site':
            return self._site[1]
        if self._kind == 'circle':
            return self._point[1]

    def __str__(self):
        if self._kind == 'site':
            return "kind: {} site: {}".format(self._kind, self._site)
        else:
            # return "kind: '{}' leaf: {} point: {}".format(self._kind, self._leaf, self._point)
            return "kind: {} point: {}".format(self._kind, self._point)

class Heap:
    def __init__(self):
        self.clear()
     
    def clear(self):
        self._array = []

    def removeMax(self):
        last = self._array[-1]
        maximum = self._array[0]
        self.swap(last, maximum)
        self._array.pop() # removes last element
        self.downheap(last)
        return maximum
    
    def empty(self):
        return self.size() == 0

    def remove(self, event):
        if self.size() > 0:
            last = self._array[-1]
            self.swap(event, last)
            self._array.pop() # removes last element
            self.upheap(last)
            self.downheap(last)

    def insert(self, kind, data, p1=None, p2=None, p3=None):
        event = Event(self.size(), kind, data, p1, p2, p3)
        self._array.append(event)
        self.upheap(event)
        self.downheap(event)
        return event
    
    def swap(self, e1, e2):
        self._array[e1._index] = e2
        self._array[e2._index] = e1
        temp = e1._index
        e1._index = e2._index
        e2._index = temp

    def downheap(self, event):
        while (self.hasLeft(event._index)) and (event.key() < self.maxChild(event).key()):
            self.swap(event, self.maxChild(event))

    def upheap(self, event):
        while event._index > 0 and event.key() > self.parent(event).key():
            self.swap(event, self.parent(event))

    def hasLeft(self, key):
        return self.size() > 2*key + 1

    def hasRight(self, key):
        return self.size() > 2*key + 2

    def left(self, key):
        return self._array[2*key + 1]

    def right(self, key):
        return self._array[2*key + 2]

    def parent(self, event):
        return self._array[int(ceil(event._index/2.0) - 1)]
    
    def maxChild(self, event):
        if (not self.hasRight(event._index)
            or self.left(event._index).key() > self.right(event._index).key()):
            return self.left(event._index)
        return self.right(event._index)

    def size(self):
        return len(self._array)
    
    def __str__(self):
        if len(self._array) == 0:
            return 'Heap:\nempty\n'
        string = 'Heap:\n'
        for i in self._array:
            string += str(i) + '\n'
        return string
