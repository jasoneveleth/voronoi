# Pseudocode #
This is designed as a better explanation of [this textbook's](https://people.inf.elte.hu/fekete/algoritmusok_msc/terinfo_geom/konyvek/Computational%20Geometry%20-%20Algorithms%20and%20Applications,%203rd%20Ed.pdf) explanation of contructing Voronoi diagrams, and I assume you've read this already (chapter 7 and the datastructures required). This README will help explain Voronoi.py which isn't commented.

## High Level Construction ##
<pre>
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
</pre>

## Handle Site Event ##
<pre>
handleSiteEvent(event)
1.  if tree is empty
2.      add arc as the root
3.      return
4.  oldNode <- node found above the event's node<a href="#findarc" id="fa"><sup>[1]</sup></a>
5.  remove false alarm circle event (if oldNode has an event)
6.  attach a subtree where oldNode used to be with two new breakpoints and 
    three new edges like this:
        [A,B]
        /   \
       A    [B,A]
            /   \
           B     A
7.  set the breakpoint's half edges as twins
8.  check for new circle event (if the breakpoint's half edges intersect
    after when they start)<a href="#checkcircle" id="cc"><sup>[2]</sup></a>
</pre>

## Handle Circle Event ##
<pre>
handleCircleEvent(leaf)
1.  get references to next leaf, previous leaf, next breakpoint, and 
    previous breakpoint.
2.  remove the leaf
3.  take the breakpoint (either next or prev) whose child was the leaf, and 
    replace it with the other child. Then reassign the other breakpoint 
    (either next or prev) so that the two points properly reflect what is 
    going on:
            [A,B]                   [A,C]
            /   \                   /   \
          ...    [B,C]            ...   ...
          /\     /   \    ->      / \   / \
        ... A   B    ...        ...  A C  ...
                     / \
                    C  ...

    as you can see, all the '...' stay the same, and the [B,C] breakpoint
    disappears, and the [A,B] breakpoint changes to [A,C].
4.  calculate the center of the circle, add a vertex there, add origins to
    the old edges
5.  make a new edge, and add the center of the circle as its origin
6.  
</pre>

<a id="findarc" href="#fa">[1]</a> Trace down the tree, and at each breakpoint, take the two sites, find the one with the higher y-value (the older one), and this shows if we are on the left, or right intersection of the parabolas.[⏎](#fa)


<a id="checkcircle" href="#cc">[2]</a> When we create half edges, we store 
the point that we know they contain, and the vector toward the edge, then 
when we solve the vector equation:
```p1 + t(v1) = p2 + s(v2)```
where p1, p2, v1, v2 are known vectors, and t, s are the unknowns. [⏎](#cc)
