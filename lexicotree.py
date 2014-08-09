from collections import Counter
from types import IntType, DictType, ListType, TupleType

class LexicoTree (object):
   '''
      Tree-like data structure with property of lexical ordering. This is most useful for optimizing Apriori-like
      routines and  algorithms e.g. for mining frequent or maximal itemsets where combinatorial generation is too
      expensive for long itemsets.

      Each leaf nodes of the tree is an itemset. Each item in the itemset has a user defined weight which affects ordering.

      Each node in the tree has a 'head' - which is an immutable set of items. Every leaf (L) which is a subnode of a
      node (N) will contain all the items in the head of N. The size of the head is equal to the degree/level of the node

      The tail of a node is the set union of descendent itemsets
   '''

   def __init__(self, values, rankings):
      assert isinstance(rankings, DictType), type(rankings)

      self.rankings = rankings
      self.values = values
      self.null_node = LexicoNode(level=0, head=frozenset(), tail=set(), children_nodes={}, parent_node=None)
      #also known as the root node

      for value in values:
         self.add_value_to_tree(value)

   def add_value_to_tree (self, raw_value):
      '''
         Adds a raw value to the tree
      '''

      #sort the value to a list, and pass it to null_node.branch
      itemset = sorted( raw_value,
                        key=self.rankings.get,
                        reverse=False)

      node = self.null_node
      for x in xrange(len(itemset)):
         node = node.branch(itemset)

   __slots__ = ('rankings',
                'values',
                'null_node')


class LexicoNode (object):
   '''
      A Node in the tree described in LexicoTree
   '''
   def __init__(self, level, head, tail, children_nodes, parent_node):
      assert isinstance(level, IntType), type(level)
      assert level >= -1
      assert isinstance(head, frozenset)# or head is None
      assert isinstance(tail, (set, ListType, TupleType))# or tail is None
      assert isinstance(children_nodes, (DictType))
      if level > 0:
         assert isinstance(parent_node, (LexicoNode))

      self.level = level
      self.head = head
      self.tail = tail
      self.children_nodes = children_nodes
      self.parent_node = parent_node

   def branch(self, itemset):
      '''
         Given an L{itemset}, returns the next node down the chain. If it doesn't exist yet, it will be created.
         This will likely be changed to 'traverse' and the creation will be delegated to the caller.

         @param itemset: itemset to insert, based on weight
         @type itemset: ListType
         @returns LexicoNode
      '''
      assert isinstance(itemset, ListType), type(itemset)
      assert itemset

      self.tail.update(x for x in itemset if x not in self.head)

      child_e = itemset[self.level] #the element in the next level thats augmented to the current level
      if child_e not in self.children_nodes:
         new_head = frozenset(self.head.union((child_e,)))

         self.children_nodes[child_e] =  LexicoNode(level=self.level+1,
                               head=new_head,
                               tail=set(x for x in itemset if x not in new_head),
                               children_nodes={},
                               parent_node=self)

      return self.children_nodes[child_e]

   def prune (self, child):
      '''
         Prunes child from this node

         @type child: frozenset or set
      '''
      assert isinstance(child, (set, frozenset))
      if child in self.children_nodes:
         del self.children_nodes[child] #so easy with python/gc!
      else:
         assert False # this should never happen

   __slots__ = (
      'level',
      'head',
      'tail',
      'children_nodes',
      'parent_node'
   )

#implementation example, more to come later
if __name__ == "__main__":
   import json

   # filename = sys.argv[1]
   statuses = json.load(open ('../twitter-trends/output/boston/Xbox1407335516789.json'))['statuses']
   cnt = Counter()

   tweets = [tuple(x['text'].encode('utf-8').split()) for x in statuses]
   tweets_as_tokens = [set([y.lower() for y in x]) for x in tweets]
   #this is redundant

   for token_set in tweets_as_tokens:
      cnt.update(token_set)

   # can use a namedtuple instead, may be more efficient
   rankings_dict = dict((v, i) for i,(v,_) in enumerate(cnt.most_common()))

   lt = LexicoTree(tweets_as_tokens, rankings_dict)