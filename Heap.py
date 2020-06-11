from math import ceil

class Event:
    def __init__(self, index, kind, data, p1=None, p2=None, p3=None):
        self._kind = kind
        self._index = index
        if self._kind == 'site event':
            self._site = data
        elif self._kind == 'circle event':
            self._leaf = data
            self._point = self.circum(p1, p2, p3)
        else:
            print("yoinks, non-event")
    
    def key(self):
        if self._kind == 'site event':
            return self._site[1]
        if self._kind == 'circle event':
            return self._point[1]

    def circum(self, a, b, c):
        d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
        x = (1.0/d)*((a[0]**2 + a[1]**2)*(b[1] - c[1]) + (b[0]**2 + b[1]**2)*(c[1] - a[1]) + (c[0]**2 + c[1]**2)*(a[1] - b[1]))
        y = (1.0/d)*((a[0]**2 + a[1]**2)*(c[0] - b[0]) + (b[0]**2 + b[1]**2)*(a[0] - c[0]) + (c[0]**2 + c[1]**2)*(b[0] - a[0]))
        r = ((a[0]-x)**2 + (a[1]-y)**2)**0.5
        return [x,y-r]
    
    def __str__(self):
        if self._kind == 'site event':
            return "kind: '" + str(self._kind) + "', site: " + str(self._site)
        else:
            return "kind: '" + str(self._kind) + "', leaf: " + str(self._leaf) + ", point: " + str(self._point)

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
        while self.size() > 2 * event._index + 1 and event.key() < self.maxChild(event).key():
            self.swap(event, self.maxChild(event))

    def upheap(self, event):
        while event._index > 0 and event.key() > self.parent(event).key():
            self.swap(event, self.parent(event))

    def parent(self, event):
        return self._array[ceil(event._index/2.0) - 1]
    
    def maxChild(self, event):
        if self.size() <= 2 * event._index + 2:
            return self._array[2 * event._index + 1]
        if self._array[2 * event._index + 1].key() > self._array[2 * event._index + 2].key():
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