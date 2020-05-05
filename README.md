# Dynamic Proximity Graphs
This is a completed research project focused on the visualization of dynamic proximity graphs. More info can be found [here](https://www.stat.berkeley.edu/~aldous/Research/SInetwork.html).
## grabriel_graph.py
1. Generates an animation of Gabriel graph. https://en.wikipedia.org/wiki/Gabriel_graph
## relative_neighborhood_graph.py
1. Generates an animation of the relative neighborhood graph. https://en.wikipedia.org/wiki/Relative_neighborhood_graph
## relative_neighborhood_graph_v2.py
1. Modified the original RNG rule by applying a new edge only if no other edge on either point forms an angle < 15 degrees to the new edge.
## RNG_v3.py
1. Added a new modification
  * If a new point is close to an existing edge then that edge may be replaced by two edges via the new point.
## RNG_v4.py
1. Refactored the code.

2. Added a new rule: 
  * First calculate which nodes we would link to A according to the RNG_v3 rule.  

  * Call these nodes B, C, D, ... in increasing order of straight-line distance from A.

  * First add the edge AB into our network.

  * Then figure the route length from A to C within the network (so using the edge from A to B as the first part of the shortest route from A to C).

  * If the straight-line distance from A to C is less than 0.7 times that route length from A to C, then add the edge AC to the network.

  * If not then do not add the edge AC.

  * Then consider the route length from A to D  within the network (so starting from A and using the edge to B or possibly to C).

  * If the straight-line distance from A to D is less than 0.7 times that route length from A to D, then add the edge AD to the network.

  * ...and so on.
