from collections import Counter, deque
from types import IntType, DictType, ListType, TupleType, FunctionType

class LexicoTree (object):
   '''
      Tree-like data structure with property of lexicographic ordering, a version of a hash tree. This is most useful for
      optimizing routines for mining frequent itemsets/maximal itemsets in algorithms such as FP-Growth where combinatorial
      subset generation is too expensive for long itemsets.

      Each leaf nodes of the tree is guarnateed to be a transaction. However, not all transations are guaranteed to be leaf
      nodes, indeed any node in the tree can potentially be a transaction. Lexicographic ordering provides an efficient way
      to enumerate subsets (parents can be considered subsets of their children) Each item in the itemset has a user defined
      weight which affects ordering. Weights can affect lookup performance (by changing the structure of the tree)

      Each node in the tree has a 'head' - which is an immutable set of items. Every leaf (L) which is a subnode of a
      node (N) will contain all the items in the head of N. The size of the head is equal to the degree/level of the node

      The tail of a node is the set union of descendent itemsets
   '''

   def __init__(self, values, rankings):
      assert isinstance(values, ListType), type (values)
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


   def traverse_breadth_first (self, func, initial_node=None):
      '''
         Applies L{func} to every node in the tree, breadth first

         @type func: FunctionType
      '''
      assert isinstance(func, FunctionType)

      if initial_node is None:
         initial_node = self.null_node
      else: assert isinstance(initial_node, LexicoNode)

      func(initial_node) #explicitly call it on the null_node
      node_queue = deque(v for (c, v) in initial_node.children_nodes.iteritems())
      while (len(node_queue) > 0):
         el = node_queue.popleft()
         func(el)
         node_queue.extend(v for c, v in el.children_nodes.iteritems())

   def traverse_depth_first (self, func, initial_node=None):
      '''
         Applies L{func} to every node in the tree, depth first

         @type func: FunctionType
      '''
      assert isinstance(func, FunctionType)

      if initial_node is None:
         initial_node = self.null_node
      else: assert isinstance(initial_node, LexicoNode)

      func(self.null_node)
      node_queue = deque(v for (c, v) in self.null_node.children_nodes.iteritems())
      while (len(node_queue) > 0):
         el = node_queue.pop()
         func(el)
         node_queue.extend(v for c, v in el.children_nodes.iteritems())


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

   def __repr__(self):
      return ','.join(str(e) for e in self.head)


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

      #the element in the next level thats augmented to the current level
      new_head = frozenset(self.head.union((itemset[self.level],)))
      if new_head not in self.children_nodes:

         self.children_nodes[new_head] = LexicoNode(level=self.level+1,
                               head=new_head,
                               tail=set(x for x in itemset if x not in new_head),
                               children_nodes={},
                               parent_node=self)

      return self.children_nodes[new_head]

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

   def pr (x):
      print ','.join(str(e) for e in x.head)

   lt.traverse_breadth_first(pr)
