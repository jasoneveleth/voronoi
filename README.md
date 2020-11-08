# Voronoi Diagrams

### Set up
We use `venv`. For \*nix, run the following commands after cloning (choose your own <environment\_name>:

```bash
$ python -m venv <environment_name>
$ source <environment_name>/bin/activate
$ python -m pip install -r requirements.txt
...
  # good to go, use python to run Voronoi.py
...
$ deactivate
```

### Pseudocode
This is designed as a better explanation of [this textbook's](https://people.inf.elte.hu/fekete/algoritmusok_msc/terinfo_geom/konyvek/Computational%20Geometry%20-%20Algorithms%20and%20Applications,%203rd%20Ed.pdf) explanation of contructing Voronoi diagrams, and I assume you've read this already (chapter 7 and the datastructures required). This README will help explain some of my code which isn't commented.

#### High Level Construction
<pre>
fortunes(sites: list of [x,y])
1.  initialize heap, binary tree, and edge list
1.  add all sites to the heap
1.  check if the first two points have the same y value
1.  while the queue isn't empty
1.      get the event with largest y-value
1.      if the event is a site event
1.          handle site event
1.      else
1.          handle circle event
1.  deal with remaining state
1.  plot the points
1.  return the diagram
</pre>

#### Handle Site Event
<pre>
handleSiteEvent(event)
1.  if tree is empty
1.      add arc as the root
1.      return
1.  get reference oldNode to node found above the event's node<a href="#findarc" id="fa"><sup>[1]</sup></a>
1.  remove false alarm circle event (if oldNode has an event)
1.  attach a subtree where oldNode used to be with two new breakpoints and
    three new edges like this:
      A    ->       [A,B]
                    /   \
                   A    [B,A]
                        /   \
                       B     A
1.  set the breakpoint's half edges as twins
1.  check for new circle event (if the breakpoint's half edges intersect
    after when they start)<a href="#checkcircle" id="cc"><sup>[2]</sup></a>
</pre>

#### Handle Circle Event
<pre>
handleCircleEvent(leaf)
1.  get references to next leaf, previous leaf, next breakpoint, and
    previous breakpoint.
1.  remove the leaf
1.  take the breakpoint (either next or prev) whose child was the leaf, and
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
1.  calculate the center of the circle, add a vertex there, add origins to
    the old edges
1.  make a new edge, and add the center of the circle as its origin
1.  assign next and previous to the edges that you know
1.  check for circle events (the same way as before)
</pre>

<a id="findarc" href="#fa">[1]</a> Trace down the tree, and at each breakpoint, take the two sites, find the one with the higher y-value (the older one), and this shows if we are on the left, or right intersection of the parabolas. Then once a leaf is hit, return it.[⏎](#fa)


<a id="checkcircle" href="#cc">[2]</a> When we create half edges, we store
the point that we know they contain, and the vector toward the edge, then
when we solve the vector equation:
```p1 + t(v1) = p2 + s(v2)```
where p1, p2, v1, v2 are known vectors, and t, s are the unknowns. [⏎](#cc)
