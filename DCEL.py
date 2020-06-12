class Vertex:
    def __init__(self, coordinates):
        self._coordinates = coordinates
        self._incidentEdge = None
    
    def __str__(self):
        return 'coordinates: ' + str(self._coordinates)


class HalfEdge:
    def __init__(self):
        self._origin = None
        self._twin = None
        self._incidentFace = None
        self._next = None
        self._prev = None
    
    def dest(self):
        return self._twin._origin
    
    def __str__(self):
        # return 'origin: ' + str(self._origin) + ', dest: ' + str(self.dest())
        # return 'object: ' + repr(self) + ', origin: ' + str(self._origin) + ', dest: ' + str(self.dest()) + ', twin: ' + repr(self._twin)
        return 'origin: ' + str(self._origin) + ', dest: ' + str(self.dest()) + ', next: ' + str(self._next) + ', prev: ' + str(self._prev)
        # return 'origin: ' + str(self._origin) + ', dest: ' + str(self.dest()) + ', next: ' + str(self._next) + ', prev: ' + str(self._prev) + ', twin: ' + repr(self._twin)


class DCEL:
    def __init__(self):
        self._edges = []
        self._vertices = []
    
    def contains(self, ele):
        return ele in self._edges or ele in self._vertices
    
    def incidentEdges(self, vertex):
        incidentEdges = []
        edge = vertex._incidentEdge
        if edge._origin == vertex:
            while True:
                incidentEdges.append(edge)
                edge = edge._twin
                incidentEdges.append(edge)
                edge = edge._next
                if vertex._incidentEdge == edge:
                    break
    
    def edges(self):
        return self._edges
    
    def addVertex(self, xy):
        vertex = Vertex(xy)
        return vertex
    
    def addEdge(self):
        edge = HalfEdge()
        self._edges.append(edge)
        return edge
    
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
