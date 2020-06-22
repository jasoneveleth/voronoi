from BinTree import BinTree
# from DCEL import *
from Heap import Event, Heap
from random import random

tree = BinTree()
# diagram = DCEL()

root = tree.addRoot('breakpoint', None, None)
n1 = tree.addLeft(root, 'breakpoint', None, None)
n2 = tree.addLeft(root, 'breakpoint', None, None)
n3 = tree.addLeft(n1, 'breakpoint', None, None)
n4 = tree.addRight(n1, 'breakpoint', None, None)
n5 = tree.addLeft(n2, 'breakpoint', None, None)
n6 = tree.addRight(n2, 'breakpoint', None, None)
n7 = tree.addLeft(n3, 'arc', None, None)
n8 = tree.addRight(n3, 'arc', None, None)
n9 = tree.addLeft(n4, 'arc', None, None)
n10 = tree.addRight(n4, 'arc', None, None)
n11 = tree.addLeft(n5, 'arc', None, None)
n12 = tree.addRight(n5, 'arc', None, None)
n13 = tree.addLeft(n6, 'arc', None, None)
n14 = tree.addRight(n6, 'arc', None, None)

print(tree)



#######WORKS#############
[[0.15936168470313505, 0.05549223972215378], [0.3264119831883383, 0.7485988116770119], [0.35975295413869335, 0.6027334041633864]]
[[0.8605032318442377, 0.2754527233087952], [0.8018987418131581, 0.3170743490900566], [0.267740151829563, 0.8443332012376055]]
[[0.84, 0.13], [0.89, 0.01], [0.3, 0.45]]

#######DOESNT#WORK#########
[[0.11356177315224081, 0.18959508175343265], [0.8594256278250202, 0.5764600163209086], [0.840236424913885, 0.36104791011358284]]
[[0.09, 0.22], [0.34, 0.78], [0.23, 0.67]]

# f1 = [random(),random()]
# f2 = [random(),random()]
# dr = random() - 1
# print(tree.intersect([f1,f2], dr))



# event7 = Event('circle event', 'yeet', [2,-1], [5,2], [2, 5])

# heap = Heap()
# e5 = heap.insert('site event', [0,5])
# e7 = heap.insert('site event', [0,7])
# e6 = heap.insert('site event', [0,6])
# e4 = heap.insert('site event', [0,4])
# e8 = heap.insert('site event', [0,8])
# e9 = heap.insert('site event', [0,9])
# e2 = heap.insert('site event', [0,2])
# heap.remove(e7)
# print(heap.removeMax() == e9)
# print(heap.removeMax() == e8)
# print(heap.removeMax() == e7)
# print(heap.removeMax() == e6)
# print(heap.removeMax() == e5)
# print(heap.removeMax() == e4)
# print(heap.removeMax() == e2)

e = Event('site event', 'nothing', 'nothing')
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
print(e.circum([0.36,0.6],[0.56,0.69],[0.3,0.62]))
# print(heap.intersect([0.36,0.6],[0.56,0.69],[0.3,0.62])
