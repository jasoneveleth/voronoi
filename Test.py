from BinTree import BinTree
# from DCEL import *
from Heap import Event, Heap
from random import random

tree = BinTree()
# diagram = DCEL()

root = tree.addRoot('breakpoint', None, None)
n1 = tree.root().addLeft('arc', None, None)
n2 = tree.root().addLeft('arc', None, None)

# f1 = [random(),random()]
# f2 = [random(),random()]
# dr = random() - 1
# print(tree.intersect([f1,f2], dr))



event7 = Event('circle event', 'yeet', [2,-1], [5,2], [2, 5])

heap = Heap()
e5 = heap.insert('site event', [0,5])
e7 = heap.insert('site event', [0,7])
e6 = heap.insert('site event', [0,6])
e4 = heap.insert('site event', [0,4])
e8 = heap.insert('site event', [0,8])
e9 = heap.insert('site event', [0,9])
e2 = heap.insert('site event', [0,2])
heap.remove(e7)
# print(heap.removeMax() == e9)
# print(heap.removeMax() == e8)
# print(heap.removeMax() == e7)
# print(heap.removeMax() == e6)
# print(heap.removeMax() == e5)
# print(heap.removeMax() == e4)
# print(heap.removeMax() == e2)

# e = Event('site event', 'nothing')
# a = [random(),random()]
# b = [random(),random()]
# c = [random(),random()]
# print(str(a) + " " + str(b) + " " + str(c))
# a = [0,1]
# b = [-1,0]
# c = [1,0]

# boolean = True
# for i, j in zip(e.circle(a, b, c), e.circum(a, b, c)):
#     if round(i*1000)/1000.0 != round(j*1000)/1000.0:
#         boolean = False

# print(boolean)
# print(e.circum(a, b, c))
# print(e.circle(a, b, c))