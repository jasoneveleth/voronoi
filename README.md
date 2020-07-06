# Pseudocode #
This is designed as a better explanation of [this textbook's explanation](https://people.inf.elte.hu/fekete/algoritmusok_msc/terinfo_geom/konyvek/Computational%20Geometry%20-%20Algorithms%20and%20Applications,%203rd%20Ed.pdf) of contructing Voronoi diagrams, and I assume you've read this already (chapter 7 and the datastructures required). This README will help explain Voronoi.py which isn't commented.

## High Level Construction ##
```
makeDiagram(sites: list of [x,y])
1.  initialize heap, binary tree, and edge list
2.  add all sites to the heap
3.  while the queue isn't empty
4.      get the event with largest y-value
5.      if the event is a site event
6.          handle site event
7.      else
8.          handle circle event
9.  deal with remaining state
10. plot the points
11. return the diagram
```

## Handle Site Event ##
```
handleSiteEvent(event)
1.  if tree is empty
2.      add arc as the root
3.      return
4.  oldNode <- node found above the event's node
5.  remove false alarm circle event (if oldNode has an event)
6.  attach a subtree where oldNode used to be with two new breakpoints and 
    three new edges like this:
        [A,B]
        /   \
       A    [B,A]
            /   \
           B     A
7.  set the breakpoint's half edges as twins
8.   
```
