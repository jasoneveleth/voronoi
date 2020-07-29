from Diagram import Diagram
import Calc
import random
import math

if __name__ == '__main__':
    points = Calc.getSitePoints(50)
    minData = Diagram(points)
    testData = Diagram(points)

    for _ in range(1000):
        i = random.randint(0, len(points))
        minPerimeter = math.inf
        for j in range(10):
            points[i] = Calc.wiggle(points[i], 0.02)
            testData._sites = points
            testData.fortunes()
            p = testData.getPerimeter()
            if p < minPerimeter:
                minData = testData
                minPerimeter = p
        minData.plot()

