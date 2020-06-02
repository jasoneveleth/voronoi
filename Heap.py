from math import ceil

class Event:
    def __init__(self, kind, data, p1=None, p2=None, p3=None):
        self._kind = kind
        self._index = None
        if self._kind == 'site event':
            self._site = data
        elif self._kind == 'circle event':
            self._leaf = data
            self._point = self.circle(p1, p2, p3)
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
    
    def circle(self, p1, p2, p3):
        # reordering
        if p1[0] > p2[0]:
            temp = p1
            p1 = p2
            p2 = temp
        if p1[0] > p3[0]:
            temp = p1
            p1 = p3
            p3 = temp
        
        # finding the lowest point of the circle
        m1x = float(p1[0] + p2[0])/2.0
        m1y = float(p1[1] + p2[1])/2.0
        if p2[0] - p1[0] != 0 and p2[1] - p1[1] != 0:
            s1 = float(p2[1] - p1[1])/float(p2[0] - p1[0])
            cy = None
            cx = None
        else:
            s1 = None
            if p2[0] - p1[0] == 0:
                cy = m1y
                cx = None
            else:
                cx = m1x
                cy = None

        m2x = float(p1[0] + p3[0])/2.0
        m2y = float(p1[1] + p3[1])/2.0
        if p3[0] - p1[0] != 0 and p3[1] - p1[1] != 0:
            s2 = float(p3[1] - p1[1])/float(p3[0] - p1[0])
        else:
            s2 = None
            if p3[0] - p1[0] == 0:
                cy = m2y
            else:
                cx = m2x
        
        if cy != None and cx != None:
            r = ((p1[0]-cx)**2 + (p1[1]-cy)**2)**0.5
            return [cx, cy-r]
        if cy == None and cx == None:
            cx = float(m2y - m1y + m2x/s2 - m1x/s1)/(1/s2 - 1/s1)
            cy = m2y - (1/s2)*(cx-m2x)
        elif cy != None:
            if s1 == None:
                cx = m2x - s2*(cy - m2y)
            if s2 == None:
                cx = m1x - s1*(cy - m1y)
        elif cx != None:
            if s1 == None:
                cy = (m2x - cx)/(s2) + m2y
            if s2 == None:
                cy = (m1x - cx)/s1 + m1y

        # print('x = ' + str(cx))
        # print('y = ' + str(cy))
        r = ((p1[0]-cx)**2 + (p1[1]-cy)**2)**0.5
        # print('r = ' + str(r))
        return [cx, cy-r]

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
        last = self._array[-1]
        self.swap(event, last)
        self._array.pop() # removes last element
        self.upheap(last)
        self.downheap(last)

    def insert(self, kind, data, p1=None, p2=None, p3=None):
        event = Event(kind, data, p1=None, p2=None, p3=None)
        event._index = self.size()
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