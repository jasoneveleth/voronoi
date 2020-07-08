from math import ceil
import Calc

class Event:
    def __init__(self, index, kind, data, p1=None, p2=None, p3=None):
        self._kind = kind
        self._index = index
        if self._kind == 'site event':
            self._site = data
        elif self._kind == 'circle event':
            self._leaf = data
            self._point = Calc.circleBottom(p1, p2, p3)
        else:
            print("yoinks, non-event")
    
    def key(self):
        if self._kind == 'site event':
            return self._site[1]
        if self._kind == 'circle event':
            return self._point[1]

    def __str__(self):
        if self._kind == 'site event':
            return "kind: '{}' site: {}".format(self._kind, self._site)
        else:
            return "kind: '{}' leaf: {} point: {}".format(self._kind, self._leaf, self._point)

class Heap:
    def __init__(self):
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
        while (self.size() > 2 * event._index + 1) and (event.key() < self.maxChild(event).key()):
            self.swap(event, self.maxChild(event))

    def upheap(self, event):
        while event._index > 0 and event.key() > self.parent(event).key():
            self.swap(event, self.parent(event))

    def parent(self, event):
        return self._array[int(ceil(event._index/2.0) - 1)]
    
    def maxChild(self, event):
        if (self.size() <= 2 * event._index + 2
            or self._array[2 * event._index + 1].key() > self._array[2 * event._index + 2].key()):
            return self._array[2 * event._index + 1]
        return self._array[2 * event._index + 2]

    def size(self):
        return len(self._array)
    
    def __str__(self):
        if len(self._array) == 0:
            return 'Heap:\nempty\n'
        string = 'Heap:\n'
        for i in self._array:
            string += str(i) + '\n'
        return string
