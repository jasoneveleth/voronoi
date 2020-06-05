class Vertex:
    def __init__(self, coordinates):
        self._coordinates = coordinates
        self._incidentEdge = None

class Face:
    def __init__(self):
        self._outerComponent = None
        self._innerComponent = []


class HalfEdge:
    def __init__(self):
        self._origin = None
        self._twin = None
        self._incidentFace = None
        self.next = None
        self.prev = None


class DCEL:
    def __init__(self):
        self._edges = []
        self._vertices = []
        self._faces = []
    
    def contains(self, ele):
        return ele in self._edges or ele in self._vertices or ele in self._faces
    
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

    def faces(self):
        return self._faces

