class Node:
    def __init__(self, parent, version, data1, data2):
        self._parent = parent
        self._version = version
        if version == 'arc':
            self._site = data1 # ex. [0,0]
            self._event = data2 # ex. Event()
            self._breakpoint = None # ex. [[0,0],[0,0]]
            self._halfedge = None # ex. diagram.addEdge()
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
    
    def getX(self):
        if self._version == 'arc':
            return self._site[0]
        else:
            return 'breakpoint'
        
    def fullprint(self, prefix='', isLast=True):
        currLine = prefix
        if isLast:
            currLine += "`- *" + self._version + "* "
            prefix += "   "
        else:
            currLine += "|- *" + self._version + "* "
            prefix += "|  "
        if self._version == 'breakpoint':
            currLine += "breakpoint: " + str(self._breakpoint) + " halfedge: '" + str(self._halfedge) + "'\n"
        else:
            currLine += "site: {}\n".format(str(self._site))
        if self._left != None:
            if self._right != None:
                return currLine + self._left.fullprint(prefix, False) + self._right.fullprint(prefix, True)
            else:
                return currLine + self._left.fullprint(prefix, True)
        elif self._right != None:
            return currLine + self._right.fullprint(prefix, True)
        return currLine

    def __str__(self):
        return self.fullprint()


class BinTree:
    def __init__(self):
        self._root = None
        self._size = 0
        self._height = 0
        self._last = None
        self._first = None

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
            self._first = self._root
            self._last = self._root
            return self._root
        else:
            print("oops already has root")
            return self._root
    
    def isRoot(self, node):
        return node == self._root

    def findArc(self, site):
        node = self.root()
        while node._version != 'arc':
            intersection = self.intersect(node._breakpoint, site[1])

            if site[0] < intersection[0]:
                node = node._left
            else:
                node = node._right

        return node
    
    def isRightChild(self, node):
        if node._parent != None:
            if node._parent._right == node:
                return True
        return False

    def isLeftChild(self, node):
        if node._parent != None:
            if node._parent._left == node:
                return True
        return False

    def successor(self, node):
        if node._right == None:
            child = node
            node = node._parent
            while not (node._parent == None):
                if node._left == child:
                    return node
                child = node
                node = node._parent
            return node
        else:
            return self.getMin(node._right)
    
    def getMin(self, node):
        if node == None:
            node = self.root()
        while not (node == None):
            node = node._left
        return node._parent
    
    def getMax(self, node):
        if node == None:
            node = self.root()
        while not (node == None):
            if node._right == None:
                return node
            node = node._right
        return node
            
    def predessesor(self, node):
        if node._left == None:
            child = node
            node = node._parent
            while not (node == None):
                if node._right == child:
                    return node
                child = node
                node = node._parent
            return node
        else:
            return self.getMax(node._left)
        
    def nextLeaf(self, node):
        successor = self.successor(node)
        if successor:
            return self.lowestLeaf(successor._right)
        else:
            return None
    
    def lowestLeaf(self, node):
        if node._left != None:
            return self.lowestLeaf(node._left)
        elif node._right != None:
            return self.lowestLeaf(node._right)
        else:
            return node

    def prevLeaf(self, node):
        predessesor = self.predessesor(node)
        if predessesor:
            return self.highestLeaf(predessesor._left)
        else:
            return None
    
    def highestLeaf(self, node):
        if node._right != None:
            return self.highestLeaf(node._right)
        if node._left != None:
            return self.highestLeaf(node._left)
        else:
            return node

    def remove(self, node):
        if node == self.root():
            print('trying to remove root')
            return
        p = node._parent
        if p._left == node:
            p._left = None
        else:
            p._right = None
        if node == self._first:
            self.resetFirst()
        elif node == self._last:
            self.resetLast()
        self._size -= 1


    def intersect(self, bp, l):
        p1 = bp[0]
        p2 = bp[1]

        a = 1.0/(2*(p1[1] - l)) - 1.0/(2*(p2[1] - l))
        b = float(p2[0])/(p2[1] - l) - float(p1[0])/(p1[1] - l)
        c = float(p1[0]**2 + p1[1]**2 - l**2)/(2*(p1[1]-l)) - float(p2[0]**2 + p2[1]**2 - l**2)/(2*(p2[1] - l))
        
        if a == 0:
            x1 = - c/b
            y1 = 1.0/(2*(p1[1] - l))*(x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2)
            return [x1,y1]

        x1 = (- b + (b**2 - 4*a*c)**0.5)/(2*a)
        y1 = 1.0/(2*(p1[1] - l))*(x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2)
        x2 = (- b - (b**2 - 4*a*c)**0.5)/(2*a)
        y2 = 1.0/(2*(p1[1] - l))*(x2**2 - 2*p1[0]*x2 + p1[0]**2 + p1[1]**2 - l**2)
        if x1 > x2:
            larger = [x1, y2]
            smaller = [x2,y2]
        else:
            larger = [x2, y2]
            smaller = [x1, y2]

        if bp[0][0] > bp[1][0]:
            return larger
        else:
            return smaller

    def addRight(self, node, version, data1, data2=None):
        node.addRight(version, data1, data2)
        self._size += 1
        depth = node._right.depth()
        if depth + 1 > self._height:
            self._height = depth + 1
        if version == 'arc':
            self.resetLast()
        return node._right

    def addLeft(self, node, version, data1, data2=None):
        node.addLeft(version, data1, data2)
        self._size += 1
        depth = node._left.depth()
        if depth + 1 > self._height:
            self._height = depth + 1
        if version == 'arc':
            self.resetFirst()
        return node._left
    
    def isExternal(self, node):
        return node._right == None and node._left == None
    
    def isLast(self, node):
        return self._last == node

    def isFirst(self, node):
        return self._first == node
    
    def __str__(self):
        return 'BinTree: \n' + str(self.root())

    def resetFirst(self):
        node = self.root()
        while node._left != None:
            node = node._left
        self._first = node
        if node._version != 'arc':
            print('the tree has a breakpoint first')

    def resetLast(self):
        node = self.root()
        while node._right != None:
            node = node._right
        self._last = node
        if node._version != 'arc':
            print('the tree has a breakpoint last')
