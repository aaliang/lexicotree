Tree-like data structure with property of lexicographic ordering, a version of a hash tree. This is most useful for modeling sets and their subsets when optimizing Apriori-like routines and  algorithms e.g. for mining frequent or maximal itemsets where combinatorial subset generation is too
expensive for long itemsets.

Each leaf nodes of the tree is guarnateed to be a transaction. However, not all transations are guaranteed to be leaf
nodes, indeed any node in the tree can potentially be a transaction. Lexicographic ordering provides an efficient way
to enumerate subsets (parents can be considered subsets of their children) Each item in the itemset has a user defined
weight which affects ordering. Weights can affect lookup performance (by changing the structure of the tree)

Each node in the tree has a 'head' - which is an immutable set of items. Every leaf (L) which is a subnode of a
node (N) will contain all the items in the head of N. The size of the head is equal to the degree/level of the node

The tail of a node is the set union of descendent itemsets
