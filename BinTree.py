class Node:
    def __init__(self, parent, version, data1, data2):
        self._parent = parent
        self._version = version
        if version == 'arc':
            self._site = data1
            self._event = data2
            self._breakpoint = None
            self._halfedge = None
        elif version == 'breakpoint':
            self._breakpoint = data1
            self._halfedge = data2
            self._site = None
            self._event = None
        else:
            print("yikes wrong version")

        self._left = None
        self._right = None
        if parent == None:
            self._depth = 0
        else:
            self._depth = parent.depth() + 1

    def depth(self):
        return self._depth

    def addRight(self, version, data1, data2):
        self._right = Node(self, version, data1, data2)
        return self._right

    def addLeft(self, version, data1, data2):
        self._left = Node(self, version, data1, data2)
        return self._left

class BinTree:
    def __init__(self):
        self._root = None
        self._size = 0
        self._height = 0

    def root(self):
        return self._root
    
    def empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def height(self):
        return self._height

    def addRoot(self, version, data1, data2):
        if self._root == None:
            self._root = Node(None, version, data1, data2)
            self._size = 1
            self._height = 1
            return self._root
        else:
            print("oops already has root")
            return self._root
    
    def isRoot(self, node):
        return node == self._root

    def findArc(self, site):
        node = self.root()
        while node._version != 'arc':
            bp = node._breakpoint
            intersection = self.intersect(bp, site[1])

            if len(intersection) == 1:
                x = intersection[0][0]
            elif bp[0][0] <= bp[1][0]:
                x =  min(intersection[0][0], intersection[1][0])
            else:
                x = max(intersection[0][0], intersection[1][0])

            if site[0] < x:
                node = node._left
            else:
                node = node._right

        return node


    def intersect(self, bp, l):
        p1 = bp[0]
        p2 = bp[1]

        a = 1.0/(2*(p1[1] - l)) - 1.0/(2*(p2[1] - l))
        b = float(p2[0])/(p2[1] - l) - float(p1[0])/(p1[1] - l)
        c = float(p1[0]**2 + p1[1]**2 - l**2)/(2*(p1[1]-l)) - float(p2[0]**2 + p2[1]**2 - l**2)/(2*(p2[1] - l))
        
        if a == 0:
            x1 = - c/b
            y1 = 1.0/(2*(p1[1] - l))*(x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2)
            return [[x1,y1]]

        x1 = (- b + (b**2 - 4*a*c)**0.5)/(2*a)
        y1 = 1.0/(2*(p1[1] - l))*(x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2)
        x2 = (- b - (b**2 - 4*a*c)**0.5)/(2*a)
        y2 = 1.0/(2*(p1[1] - l))*(x2**2 - 2*p1[0]*x2 + p1[0]**2 + p1[1]**2 - l**2)
        return [[x1,y1],[x2,y2]]

    def addRight(self, node, version, data1, data2):
        node.addRight(version, data1, data2)
        self._size += 1
        depth = node.right().depth()
        if depth + 1 > self._height:
            self._height = depth + 1
        return node.right()

    def addLeft(self, node, version, data1, data2):
        node.addLeft(version, data1, data2)
        self._size += 1
        depth = node.left().depth()
        if depth + 1 > self._height:
            self._height = depth + 1
        return node.left()
    
    def isExternal(self, node):
        return node.right() == None and node.left() == None