import Calc

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
            currLine += "breakpoint: {} halfedge: '{}'\n".format(self._breakpoint, self._halfedge)
        else:
            currLine += "site: {}\n".format(self._site)
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
        print()
        print(' . . . searching')
        print('site: {}'.format(site))
        while node._version != 'arc':
            intersection = Calc.intersect(node._breakpoint, site[1])
            print('intersection: {}'.format(intersection))
            if site[0] < intersection[0]:
                node = node._left
            else:
                node = node._right
        print('found node: {}'.format(node))
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
            
    def predecessor(self, node):
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
        if not self.isLast(node):
            successor = self.successor(node)
            return self.lowestLeaf(successor._right)
        else:
            return None

    def replace(self, old, new):
        self.remove(new)
        old._site = new._site
        old._event = new._event
        old._breakpoint = new._breakpoint
        old._halfedge = new._halfedge
        old._left = new._left
        old._right = new._right
        
    def lowestLeaf(self, node):
        if node._left != None:
            return self.lowestLeaf(node._left)
        elif node._right != None:
            return self.lowestLeaf(node._right)
        else:
            return node

    def prevLeaf(self, node):
        if not self.isFirst(node):
            predecessor = self.predecessor(node)
            return self.highestLeaf(predecessor._left)
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
