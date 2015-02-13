Tree-like data structure with property of lexicographic ordering, aka a prefix tree (version of hash tree)
This is perhaps useful for optimizing routines for mining frequent itemsets/maximal itemsets in algorithms such as
FP-Growth where combinatorial subset generation is too expensive for long itemsets.

Each leaf nodes of the tree is guarnateed to be a transaction. However, not all transations are guaranteed to be leaf
nodes, indeed any node in the tree can potentially be a transaction. Lexicographic ordering provides an efficient way
to enumerate subsets (parents can be considered subsets of their children) Each item in the itemset has a user defined
weight which affects ordering. Weights can affect lookup performance (by changing the structure of the tree)

Each node in the tree has a 'head' - which is an immutable set of items. Every leaf (L) which is a subnode of a
node (N) will contain all the items in the head of N. The size of the head is equal to the degree/level of the node

The tail of a node is the set union of descendent itemsets

There are three flavors in increasing level of optimization:

1) lexicotree - full implementation of a tree, all references are maintained unless they are pruned by the calling algorithm,
   calling algorithm must grow each leaf of the tree
2) setenumtree - optimized version of the above, this is also different in that the calling algorithm must:
   a) explicitly grow each level of the tree
   b) know the relative weights of each item (even though this is stored internally on the tree this is never used internally and should be considered marked for deprecation)
3) setenumtreerefless - differs from the above in that:
  - parent nodes of each node of the tree is not maintained
  - as a result, it is not possible to bfs/dfs traverse the entire enumeration from the tree object
