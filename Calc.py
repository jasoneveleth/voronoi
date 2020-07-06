from random import random

def circleCenter(a, b, c):
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    x = (1.0/d)*((a[0]**2 + a[1]**2)*(b[1] - c[1]) + (b[0]**2 + b[1]**2)*(c[1] - a[1]) + (c[0]**2 + c[1]**2)*(a[1] - b[1]))
    y = (1.0/d)*((a[0]**2 + a[1]**2)*(c[0] - b[0]) + (b[0]**2 + b[1]**2)*(a[0] - c[0]) + (c[0]**2 + c[1]**2)*(b[0] - a[0]))
    return [x,y]

def circleBottom(a, b, c):
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    x = (1.0/d)*((a[0]**2 + a[1]**2)*(b[1] - c[1]) + (b[0]**2 + b[1]**2)*(c[1] - a[1]) + (c[0]**2 + c[1]**2)*(a[1] - b[1]))
    y = (1.0/d)*((a[0]**2 + a[1]**2)*(c[0] - b[0]) + (b[0]**2 + b[1]**2)*(a[0] - c[0]) + (c[0]**2 + c[1]**2)*(b[0] - a[0]))
    r = ((a[0]-x)**2 + (a[1]-y)**2)**0.5
    return [x,y-r]

def intersect(breakpoint, l): # takes in list of two ordered focii, and a directrix
    p1 = breakpoint[0]
    p2 = breakpoint[1]

    a = 1.0/(2*(p1[1] - l)) - 1.0/(2*(p2[1] - l))
    b = float(p2[0])/(p2[1] - l) - float(p1[0])/(p1[1] - l)
    c = float(p1[0]**2 + p1[1]**2 - l**2)/(2*(p1[1]-l)) - float(p2[0]**2 + p2[1]**2 - l**2)/(2*(p2[1] - l))

    # this is for when multiple points have the same y value
    if a == 0:
        x1 = - c/b
        y1 = 1.0/(2*(p1[1] - l))*(x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2)
        return [x1,y1]

    x1 = (- b + (b**2 - 4*a*c)**0.5)/(2*a)
    y1 = 1.0/(2*(p1[1] - l))*(x1**2 - 2*p1[0]*x1 + p1[0]**2 + p1[1]**2 - l**2)
    x2 = (- b - (b**2 - 4*a*c)**0.5)/(2*a)
    y2 = 1.0/(2*(p1[1] - l))*(x2**2 - 2*p1[0]*x2 + p1[0]**2 + p1[1]**2 - l**2)

    larger = [x1,y1] if x1 > x2 else [x2,y2]
    smaller = [x2,y2] if x1 > x2 else [x1,y1]

    old = p2 if p1[1] < p2[1] else p1
    new = p1 if p1[1] < p2[1] else p2

    if [p1,p2] == [old,new]:
        return smaller
    elif [p1,p2] == [new,old]:
        return larger
    else:
        print('flag')

def rand():
    return round(random()*100)/100.0

def getPoints(n):
    points = []
    yvalues = []
    for _ in range(n):
        a = rand()
        while a in yvalues:
            a = rand()
        yvalues.append(a)
        points.append([rand(),a])
    print(points)
    return points

def getProjection(point, focus):
    directrix = point[0]
    y = (1.0/(2*(focus[1] - directrix))) * (point[0] - focus[0])**2 + (point[1] + focus[1])/2.0
    return [point[0], y] 

def converge(bp1, bp2):
    p1 = bp1._halfedge._point
    v1 = bp1._halfedge._vector
    p2 = bp2._halfedge._point
    v2 = bp2._halfedge._vector

    # intersection of parameterized lines: p1 + t(v1) and p2 + s(v2)
    s = (v1[0] * p1[1] - v1[0] * p2[1] + p2[0] * v1[1] - p1[0] * v1[1])/(v2[1] * v1[0] + v2[0] * v1[1])
    t = (p2[0] - p1[0] + s * v2[0])/v1[0]

    if (s > 0) and (t > 0):
        return True
    else:
        return False

def sumVector(v, w):
    return [v[0] + w[0], v[1] + w[1]]
