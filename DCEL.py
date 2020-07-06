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
        self._point = None
        self._vector = None
    
    def dest(self):
        return self._twin._origin
    
    def __str__(self):
        return 'origin: ' + str(self._origin) + ', dest: ' + str(self.dest())


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
        return vertex
    
    def addOrigin(self, node, coord):
        if node._origin is None:
            node._origin = coord
        else:
            node._twin._origin = coord

    def addEdge(self, point, site1, site2):
        edge = HalfEdge()
        self._edges.append(edge)
        edge._twin = HalfEdge()
        edge._twin._twin = edge
        self._edges.append(edge._twin)
        edge._point = point
        edge._twin._point = point

        if site1[0] > site2[0]:
            temp = site1
            site1 = site2
            site2 = temp

        slope = (site2[1] - site1[1])/(site2[0] - site1[0])
        x0 = [0,-1.0/slope * (0-point[0]) + point[1]]
        x1 = [1,-1.0/slope * (1-point[0]) + point[1]]
        y0 = [-slope * (0-point[1]) + point[0],0]
        y1 = [-slope * (1-point[1]) + point[0],1]
        
        useful = []
        if (x0[1] > 0) and (x0[1] < 1):
            useful.append(x0)
        if (x1[1] > 0) and (x1[1] < 1):
            useful.append(x1)
        if (y0[0] >= 0) and (y0[0] <= 1):
            useful.append(y0)
        if (y1[0] >= 0) and (y1[0] <= 1):
            useful.append(y1)

        # INTERSECTION THAT GOES TO THE LEFT IS ASSIGNED TO EDGE
        left = useful[1] if useful[1][0] <= useful[0][0] else useful[0]
        right = useful[0] if useful[1][0] <= useful[0][0] else useful[1]
        edge._vector = [left[0] - point[0], left[1] - point[1]]
        edge._twin._vector = [right[0] - point[0], right[1] - point[1]]
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
