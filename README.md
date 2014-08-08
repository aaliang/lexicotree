Tree-like data structure with property of lexical ordering. This is most useful for optimizing Apriori-like
routines and  algorithms e.g. for mining frequent or maximal itemsets where combinatorial generation is too
expensive for long itemsets.

Each leaf nodes of the tree is an itemset. Each item in the itemset has a user defined weight which affects ordering.

Each node in the tree has a 'head' - which is an immutable set of items. Every leaf (L) which is a subnode of a
node (N) will contain all the items in the head of N. The size of the head is equal to the degree/level of the node

The tail of a node is the set union of descendent itemsets