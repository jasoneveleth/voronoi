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
            raise TypeError("yikes wrong version")

        self._left = None
        self._right = None
        if parent == None:
            self._depth = 0
        else:
            self._depth = parent._depth + 1

    def addRight(self, version, data1, data2):
        self._right = Node(self, version, data1, data2)
        return self._right

    def addLeft(self, version, data1, data2):
        self._left = Node(self, version, data1, data2)
        return self._left

    def getInfo(self):
        if self._version == 'breakpoint':
            return "breakpoint: {} halfedge: <{}>\n".format(self._breakpoint, self._halfedge)
            # return "breakpoint: {}\n".format(self._breakpoint)
        else:
            return "site: {} event: <{}>\n".format(self._site, self._event)
    
    def __str__(self, prefix='', isLast=True):
        currLine = prefix + ("`- " if isLast else "|- ") + self.getInfo()
        prefix += "   " if isLast else "|  "
        children = [child for child in [self._left, self._right] if child]
        for i,child in enumerate(children):
            last = (i == len(children) - 1)
            currLine += child.__str__(prefix, last)
        return currLine


class BinTree:
    def __init__(self):
        self._root = None
        self._size = 0
        self._height = 0

    def empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def height(self):
        return self._height

    def isLeftChild(self, node):
        if self._root == node:
            raise Exception('root is parentless')
        return node == node._parent._left

    def isRightChild(self, node):
        if self._root == node:
            raise Exception('root is parentless')
        return node == node._parent._right

    def addRoot(self, version, data1, data2):
        if self._root == None:
            self._root = Node(None, version, data1, data2)
            self._size = 1
            self._height = 1
            return self._root
        else:
            raise BinTreeRootError("oops already has root")
            return self._root
    
    def findArc(self, site):
        node = self._root
        while node._version != 'arc':
            intersection = Calc.intersect(node._breakpoint, site[1])
            if site[0] < intersection[0]:
                node = node._left
            else:
                node = node._right
        return node

    def getMin(self, node):
        if node._left == None:
            return node
        return self.getMin(node._left)
    
    def getMax(self, node):
        if node._right == None:
            return node
        return self.getMax(node._right)
            
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
    
    def remove(self, node):
        self._size -= 1
        p = node._parent # trying to remove root, or parent's null
        if p._left == node:
            p._left = None
        elif p._right == node:
            p._right = None

    def getNodes(self):
        l = []
        l = self.recurseAcc(l, self._root)
        return l

    def recurseAcc(self, l, n):
        l += [n]
        if n._left is not None:
            l = self.recurseAcc(l, n._left)
        if n._right is not None:
            l = self.recurseAcc(l, n._right)
        return l

    def diagnostic(self):
        n = self._root
        l = [n]
        visited = []
        while len(l) > 0:
            n = l.pop()
            if n in visited:
                print('not good')
                continue
            if n._left is not None:
                l += [n._left]
            if n._right is not None:
                l += [n._right]
            print()
            print('self: ' + str(n).split('\n')[0])
            print('left: ' + str(n._left).split('\n')[0])
            print('right: ' + str(n._right).split('\n')[0])
            print('parent: ' + str(n._parent).split('\n')[0])
            visited += [n]

    def replaceWithChild(self, parent, child):
        """We know from context parent's other child is None."""
        if parent == self._root:
            self._root = child
            return
        grand = parent._parent
        if self.isLeftChild(parent):
            grand._left = child
        else:
            grand._right = child
        child._parent = grand

        # parent._version = child._version
        # parent._site = child._site
        # parent._event = child._event
        # parent._breakpoint = child._breakpoint
        # parent._halfedge = child._halfedge
        # parent._left = child._left
        # parent._right = child._right
        # if parent._right is not None:
        #     parent._right._parent = parent
        # if parent._left is not None:
        #     parent._left._parent = parent
        # self._size -= 1


    def lowestLeaf(self, node):
        if node._left != None:
            return self.lowestLeaf(node._left)
        elif node._right != None:
            return self.lowestLeaf(node._right)
        else:
            return node
    
    def highestLeaf(self, node):
        if node._right != None:
            return self.highestLeaf(node._right)
        elif node._left != None:
            return self.highestLeaf(node._left)
        else:
            return node

    def nextLeaf(self, node):
        if not (node == self.getMax(self._root)):
            successor = self.successor(node)
            return self.lowestLeaf(successor._right)
        else:
            return None

    def prevLeaf(self, node):
        if not (node == self.getMin(self._root)):
            predecessor = self.predecessor(node)
            return self.highestLeaf(predecessor._left)
        else:
            return None

    def addRight(self, node, version, data1, data2=None):
        node.addRight(version, data1, data2)
        self._size += 1
        depth = node._right._depth
        if depth + 1 > self._height:
            self._height = depth + 1
        return node._right

    def addLeft(self, node, version, data1, data2=None):
        node.addLeft(version, data1, data2)
        self._size += 1
        depth = node._left._depth
        if depth + 1 > self._height:
            self._height = depth + 1
        return node._left

    def __str__(self):
        return 'BinTree: \n' + str(self._root)
