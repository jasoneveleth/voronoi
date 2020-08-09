import Calc

class BinTreeOrganizationError(Exception):
    def __init__(self, message):
        self.message = message

class BinTreeRootError(Exception):
    def __init__(self, message):
        self.message = message


class Node:
    def __init__(self, parent, data):
        self._parent = parent
        self.data = data
        self._left = None
        self._right = None
        self._depth = 0 if (parent is None) else parent._depth + 1
        for attr in ['site', 'event', 'bp', 'edge']:
            if not (attr in self.data):
                self.data[attr] = None

    def addRight(self, data):
        self._right = Node(self, data)
        return self._right

    def addLeft(self, data):
        self._left = Node(self, data)
        return self._left

    def getInfo(self):
        if self.data['site'] is None:
            return "breakpoint: {} halfedge: <{}>\n".format(self.data['bp'], self.data['edge'])
        else:
            return "site: {} event: <{}>\n".format(self.data['site'], self.data['event'])

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
            raise BinTreeRootError('root is parentless')
        return node == node._parent._left

    def isRightChild(self, node):
        if self._root == node:
            raise BinTreeRootError('root is parentless')
        return node == node._parent._right

    def addRoot(self, value):
        if self._root == None:
            self._root = Node(None, value)
            self._size = 1
            self._height = 1
            return self._root
        else:
            raise BinTreeRootError("oops already has root")
            return self._root

    def findArc(self, site):
        node = self._root
        while node.data['site'] is None:
            intersection = Calc.intersect(node.data['bp'], site[1])
            if site[0] < intersection[0]:
                node = node._left
            else:
                node = node._right
        return node

    def getMin(self, node):
        while not node._left is None:
            node = node._left
        return node

    def getMax(self, node):
        while not node._right is None:
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
        p = node._parent
        if p is not None:
            if p._left == node:
                p._left = None
            elif p._right == node:
                p._right = None

    def diagnostic(self):
        n = self._root
        l = [n]
        visited = []
        string = ''
        while len(l) > 0:
            n = l.pop()
            if n in visited:
                raise BinTreeOrganizationError('not good')
            if n._left is not None:
                l += [n._left]
            if n._right is not None:
                l += [n._right]
            string += '\n'
            string += 'self: ' + str(n).split('\n')[0][3:] + '\n'
            string += 'left: ' + str(n._left).split('\n')[0][3:] + '\n'
            string += 'right: ' + str(n._right).split('\n')[0][3:] + '\n'
            string += 'parent: ' + str(n._parent).split('\n')[0][3:] + '\n'
            visited += [n]
        return string

    def replaceWithChild(self, parent, child):
        """We know from context parent's other child is None."""
        self._size -= 1
        if parent == self._root:
            self._root = child
            return
        grand = parent._parent
        if self.isLeftChild(parent):
            grand._left = child
        else:
            grand._right = child
        child._parent = grand

    def lowestLeaf(self, node):
        while True:
            if not node._left is None:
                node = node._left
            elif not (node._right is None):
                node = node._right
            else:
                return node

    def highestLeaf(self, node):
        while True:
            if not (node._right is None):
                node = node._right
            elif not (node._left is None):
                node = node._left
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

    def addRight(self, parent, data):
        parent.addRight(data)
        self._size += 1
        depth = parent._right._depth
        if depth + 1 > self._height:
            self._height = depth + 1
        return parent._right

    def addLeft(self, parent, data):
        parent.addLeft(data)
        self._size += 1
        depth = parent._left._depth
        if depth + 1 > self._height:
            self._height = depth + 1
        return parent._left

    def __str__(self):
        return 'BinTree: \n' + str(self._root)
