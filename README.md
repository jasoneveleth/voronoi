# Pseudocode #
## High Level Construction ##
makeDiagram(sites)
1.  initialize heap, binary tree, and edge list
2.  add all sites to the heap
3.  while the queue isn't empty
4.      get the event with largest y-value
5.      if the event is a site event
6.          handle site event
7.      else
8.          handle circle event
9.  collect remaining state
10. plot the points
11. return the diagram

## Handle Site Event ##
```
handleSiteEvent(event)
1.  if tree is empty
2.      add arc as the root
3.      return
4.  oldNode <- node found above the event's node
5.  remove false alarm circle events (if oldNode has an event)
6.  
```
