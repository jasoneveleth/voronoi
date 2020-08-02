import Calc

class Event:
    def __init__(self, index, kind, data, p=None):
        self._kind = kind
        self._index = index
        if self._kind == 'site':
            self._site = data
            self._key = self._site[1]
        elif self._kind == 'circle':
            self._leaf = data
            self._point = p
            self._key = self._point[1]
        else:
            raise TypeError("non-event")

    def __str__(self):
        if self._kind == 'site':
            return "kind: {} site: {}".format(self._kind, self._site)
        else:
            # return "kind: '{}' leaf: {} point: {}".format(self._kind, self._leaf, self._point)
            return "kind: {} point: {}".format(self._kind, self._point)

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

    def insert(self, kind, data, p=None):
        event = Event(self.size(), kind, data, p)
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
        while self.hasLeft(event._index):
            maxChild = self.maxChild(event._index)
            if event._key < self._array[maxChild]._key:
                self.swap(event, self._array[maxChild])
            else:
                break

    def upheap(self, event):
        while event._index > 0 and event._key > self._array[self.parent(event._index)]._key:
            self.swap(event, self._array[self.parent(event._index)])

    def hasLeft(self, key):
        return self.size() > 2*key + 1

    def hasRight(self, key):
        return self.size() > 2*key + 2

    def left(self, index):
        return 2*index + 1

    def right(self, index):
        return 2*index + 2

    def parent(self, index):
        return (index-1)//2
    
    def maxChild(self, index):
        if (not self.hasRight(index)
            or self._array[self.left(index)]._key > self._array[self.right(index)]._key):
            return self.left(index)
        return self.right(index)

    def size(self):
        return len(self._array)
    
    def __str__(self):
        if len(self._array) == 0:
            return 'Heap:\nempty\n'
        string = 'Heap:\n'
        for i in self._array:
            string += str(i) + '\n'
        return string
