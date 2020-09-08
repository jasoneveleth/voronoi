import voronoi.calc as Calc

class Vertex:
    def __init__(self, coordinates):
        self._coordinates = coordinates
        self._incidentEdge = None

    def __str__(self):
        return 'coordinates: ' + str(self._coordinates)

class Face:
    def __init__(self):
        self._edges = []

    def addEdge(self, e):
        self._edges.append(e)

class HalfEdge:
    def __init__(self):
        self._origin = None
        self._twin = None
        self._incidentFace = None
        self._next = None
        self._prev = None
        self._point = None
        self._vector = None

    def dest(self):
        return self._twin._origin

    def __str__(self):
        return 'origin: ' + str(list(map(Calc.roundBetter, self._origin)) if self._origin is not None else None) + ', dest: ' + str((list(map(Calc.roundBetter, self.dest()))) if self.dest() is not None else None) + ', point: ' + str(self._point) + ', vector: ' + str(self._vector)


class DCEL:
    def __init__(self):
        self._edges = set()
        self._vertices = set()
        self._faces = set()

    def contains(self, ele):
        return ele in self._edges or ele in self._vertices or ele in self._faces

    def incidentEdges(self, vertex):
        incidentEdges = []
        edge = vertex._incidentEdge._next
        while vertex._incidentEdge != edge:
            incidentEdges.append(edge)
            edge = edge._twin
            incidentEdges.append(edge)
            edge = edge._next
        return incidentEdges

    def boundingEdges(self, face):
        return face._edges

    def addFace(self):
        f = Face()
        self._faces.add(f)
        return f

    def faces(self):
        return self._faces

    def assignAdjacency(self, coord, edge1, edge2):
        if edge1._origin != coord:
            if edge2._origin != coord:
                edge1._next = edge2._twin
                edge1._twin._prev = edge2
                edge2._next = edge1._twin
                edge2._twin._prev = edge1
            else:
                edge1._next = edge2
                edge1._twin._prev = edge2._twin
                edge2._prev = edge1
                edge2._twin._next = edge1._twin
        else:
            if edge2._origin != coord:
                edge1._prev = edge2._twin
                edge1._twin._next = edge2
                edge2._prev = edge1._twin
                edge2._twin._next = edge1
            else:
                edge1._prev = edge2
                edge1._twin._next = edge2._twin
                edge2._next = edge1
                edge2._twin._prev = edge1._twin

    def edges(self):
        return self._edges

    def addVertex(self, xy):
        vertex = Vertex(xy)
        self._vertices.append(vertex)
        return vertex

    def addEdge(self, point):
        edge = HalfEdge()
        edge._twin = HalfEdge()
        self._edges.add(edge)
        self._edges.add(edge._twin)
        edge._point = point
        edge._twin._point = point
        edge._twin._twin = edge
        return edge

    def removeEdge(self, edge):
        self._edges.remove(edge)

    def initCircleVector(self, edge, bp, bottom):
        site1, site2 = bp
        point = edge._point
        futurePt = Calc.intersect((site1, site2), bottom[1]-0.1)
        edge._vector = Calc.subtract(futurePt, point)
        edge._origin = point
        edge._twin._vector = (-edge._vector[0], -edge._vector[1])

    def initSiteVector(self, edge, site1, site2):
        if site1[0] > site2[0]:
            temp = site1
            site1 = site2
            site2 = temp

        if site1[0] - site2[0] == 0:
            leftVector = (-1,0)
            rightVector = (1, 0)
        elif site1[1] - site2[1] == 0:
            leftVector = (0, 1)
            rightVector = (0, -1)
        else:
            slope = (site2[1] - site1[1])/(site2[0] - site1[0])
            leftVector = (-1, 1.0/slope)
            rightVector = (1, -1.0/slope)

        edge._vector = leftVector
        edge._twin._vector = rightVector

    def dest(self, edge):
        return edge._twin._origin

    def vertices(self):
        return self._vertices

    def __str__(self):
        string = 'HalfEdges: \n'
        for i in self._edges:
            string += str(i) + '\n'
        string += "\nVertices:\n"
        if len(self._vertices) == 0:
            string += "none\n"
        for i in self._vertices:
            string += str(i)
        return string
