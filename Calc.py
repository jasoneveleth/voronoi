from random import random
from functools import reduce

class IntersectError(Exception):
    def __init__(self, message):
        self.message = message


class CurvatureError(Exception):
    def __init__(self, message):
        self.message = message


def circleCenter(a, b, c):
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    x = (1.0/d)*((a[0]**2 + a[1]**2)*(b[1] - c[1]) 
                 + (b[0]**2 + b[1]**2)*(c[1] - a[1]) 
                 + (c[0]**2 + c[1]**2)*(a[1] - b[1]))
    y = (1.0/d)*((a[0]**2 + a[1]**2)*(c[0] - b[0]) 
                 + (b[0]**2 + b[1]**2)*(a[0] - c[0]) 
                 + (c[0]**2 + c[1]**2)*(b[0] - a[0]))
    return (x,y)

def circleBottom(a, b, c):
    x,y = circleCenter(a, b, c)
    r = ((a[0]-x)**2 + (a[1]-y)**2)**0.5
    return (x,y-r)

def intersect(breakpoint, l):
    """takes in list of two ordered focii, and a directrix
    """
    p1, p2 = breakpoint

    a = 1.0/(2*(p1[1]-l)) - 1.0/(2*(p2[1] - l))
    b = float(p2[0])/(p2[1] - l) - float(p1[0])/(p1[1] - l)
    c = (float(p1[0]**2 + p1[1]**2 - l**2)/(2*(p1[1]-l)) 
        - float(p2[0]**2 + p2[1]**2 - l**2)/(2*(p2[1] - l)))

    # this is for when multiple points have the same y value
    if a == 0:
        x = - c/b
        y = (1.0/(2*(p1[1] - l))
            * (x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2))
        return (x,y)

    x1,x2 = quadraticFormula(a, b, c)
    y1 = (1.0/(2*(p1[1] - l))
         * (x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2))
    y2 = (1.0/(2*(p1[1] - l))
         * (x2**2 - 2*p1[0]*x2 + p1[0]**2 + p1[1]**2 - l**2))

    right = (x1,y1) if x1 > x2 else (x2,y2)
    left = (x2,y2) if x1 > x2 else (x1,y1)
    old = p2 if p1[1] < p2[1] else p1
    new = p1 if p1[1] < p2[1] else p2

    if (p1,p2) == (old,new):
        return left
    elif (p1,p2) == (new,old):
        return right
    else:
        raise IntersectError('flag')

def quadraticFormula(a, b, c):
    return ((-b + (b**2 - 4*a*c)**0.5)/(2*a),
            (-b - (b**2 - 4*a*c)**0.5)/(2*a),)

def rand():
    return roundBetter(random())

def roundBetter(x):
    n = 1000000
    return round(x*n)/n

def getSitePoints(n):
    points = []
    yvalues = []
    for _ in range(n):
        a = rand()
        while a in yvalues:
            a = rand()
        yvalues.append(a)
        points.append([rand(),a])
    return points

def getProjection(point, focus):
    directrix = point[1]
    y = ((1.0/(2*(focus[1] - directrix))) * (point[0] - focus[0])**2 
         + (point[1] + focus[1])/2.0)
    return (point[0], y) 

def converge(p1, v1, p2, v2):
    """intersection of parameterized lines: p1 + t(v1) and p2 + s(v2)"""
    s = ((v1[0]*p1[1] - v1[0]*p2[1] + v1[1]*p2[0] - v1[1]*p1[0])
         / (v2[1]*v1[0] - v2[0]*v1[1]))
    t = (p2[0] - p1[0] + s*v2[0])/v1[0]
    return (s > 0) and (t > 0)

pointsOutward = lambda o,v: (o is not None) and (extend(o, v) is None)

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def notEqual(n, m):
    return round(n*(10**8))/(10**8) != round(m*(10**8))/(10**8)

def subtract(a, b):
    return (a[0] - b[0], a[1] - b[1])

def sumVectors(v, w):
    return (v[0] + w[0], v[1] + w[1])

def isOutside(point):
    if (point[0]>1) or (point[1]>1) or (point[0]<0) or (point[1]<0):
        return True
    else:
        return False

def getTime(dest, v):
    """solving: dest = t * v, for t"""
    if (notEqual(v[0], 0)) and (notEqual(v[1], 0)):
        if notEqual(dest[0]/v[0], dest[1]/v[1]):
            raise CurvatureError('the edge is curved {},{}'.format(dest[0]/v[0], dest[1]/v[1]))
        return dest[0]/v[0]
    elif notEqual(v[0], 0):
        return dest[0]/v[0]
    else:
        return dest[1]/v[1]

def extend(point, vector):
    boundingPts = getUseful(point, vector)
    t = getTime(subtract(boundingPts[0], point), vector)
    s = getTime(subtract(boundingPts[1], point), vector)
    if (t >= 0) and (s >= 0):
        return boundingPts[0] if t >= s else boundingPts[1]
    elif t >= 0:
        return boundingPts[0]
    elif s >= 0:
        return boundingPts[1]
    else:
        return None

def shorten(point, vector):
    boundingPts = getUseful(point, vector)
    t = getTime(subtract(boundingPts[0], point), vector)
    s = getTime(subtract(boundingPts[1], point), vector)
    if (t >= 0) and (s >= 0):
        return boundingPts[0] if t <= s else boundingPts[1]
    elif t >= 0:
        return boundingPts[0]
    elif s >= 0:
        return boundingPts[1]
    else:
        return None

def getUseful(point, vector):
    if vector[1] == 0: # vector horizontal
        y = point[1] 
        return [(0,y),(1,y)]
    elif vector[0] == 0: # vector vertical
        x = point[0]
        return [(x,0),(x,1)]

    slope = float(vector[1]/vector[0])
    x0 = (0, slope*(0-point[0]) + point[1])
    x1 = (1, slope*(1-point[0]) + point[1])
    y0 = (1/slope*(0-point[1]) + point[0], 0)
    y1 = (1/slope*(1-point[1]) + point[0], 1)

    inclusive = lambda x: (x >= 0) and (x <= 1)
    exclusive = lambda x: (x > 0) and (x < 1)
    useful = [i for i in [x0, x1] if exclusive(i[1])]
    useful += [i for i in [y0, y1] if inclusive(i[0])]
    return useful


