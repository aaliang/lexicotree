from types import DictType, IntType, ListType, TupleType, FunctionType
from collections import deque
import operator

#TODO: maybe use OO with the other tree types...
class SetEnumTree (object):
   '''
      Set enumeration tree (SE-tree), useful in optimizing combinatoric problems
   '''

   def __init__(self, rankings, items):
      # assert isinstance(rankings, DictType)

      self.null_node = SetEnumNode(head=tuple(), tail=tuple(items), children_nodes={}, parent_node=None)
      self.rankings = rankings
      self.ranklist = tuple(sorted(items, key=lambda x: rankings[x]))

      self.leafs = set(self.null_node.gen_sub_nodes())

   def grow (self):
      '''
         Grows each leaf in the tree
      '''
      new_leafs = set()
      for x in self.leafs:
         new_leafs.update(x.gen_sub_nodes())
         # new_leafs.extend(x.gen_sub_nodes())
      self.leafs = new_leafs

   def bfs_traverse (self, func, initial_node = None):
      # assert isinstance(func, FunctionType)
      if initial_node is None:
         initial_node = self.null_node
      # else: assert isinstance(initial_node, SetEnumNode)

      func(initial_node) #explicitly call it on the null_node
      node_queue = deque(v for (c, v) in initial_node.children_nodes.iteritems())
      while (len(node_queue) > 0):
         el = node_queue.popleft()
         func(el)
         node_queue.extend(v for c, v in el.children_nodes.iteritems())


class SetEnumNode (object):

   def __init__(self, head, tail, children_nodes, parent_node):
      # assert isinstance(head, TupleType)# or head is None
      # assert isinstance(tail, ListType)# or tail is None
      # assert isinstance(children_nodes, (DictType))

      self.head = head
      self.tail = tail
      self.children_nodes = children_nodes
      self.parent_node = parent_node

   def gen_sub_nodes (self):
      new_nodes = []
      for i, x in enumerate(self.tail):
         assert x not in self.head
         new_child_head = self.head + (x, )
         # new_child_head_tail = self.tail[i+1::]
         new_child = SetEnumNode(head=new_child_head,
                                 tail=self.tail[i+1::],
                                 children_nodes={},
                                 parent_node=self)
         self.children_nodes[new_child_head] = new_child
         new_nodes.append(new_child)

      return new_nodes

   #same as above, except this recurses exhaustively...
   def spawn_children_exhaustive (self, candidates):
      # assert isinstance(candidates, (ListType, TupleType))
      for i, x in enumerate(candidates):
         assert x not in self.head
         new_child_head = self.head + (x,)
         new_child = SetEnumNode(new_child_head, tail=[], children_nodes={}, parent_node=self)
         self.children_nodes[new_child_head] = new_child
         self.tail.append(x)
         new_candidates = candidates[i+1::]

         new_child.spawn_exhaustive(new_candidates)

   __slots__ = (
      'level',
      'head',
      'tail',
      'children_nodes',
      'parent_node',
   )