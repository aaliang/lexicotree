from collections import OrderedDict


#TODO: maybe use OO with the other tree types...
class SetEnumTreeRefless (object):
   '''
      Set enumeration tree (SE-tree), useful in optimizing combinatoric problems.
      This maintains no references to the nodes aside from the leafs. Allows the cPython gc to
      reclaim objects
   '''

   def __init__(self, rankings, items):
      # assert isinstance(rankings, DictType)

      null_node = SetEnumNode(head=tuple(), tail=tuple(items))
      self.rankings = rankings
      self.ranklist = tuple(sorted(items, key=lambda x: rankings[x]))

      self.leafs = OrderedDict((x, None) for x in null_node.gen_sub_nodes())

   def grow (self):
      new_leafs = OrderedDict()
      for x in self.leafs:
         new_leafs.update((y, None) for y in x.gen_sub_nodes())

      self.leafs = new_leafs
      print 'len(self.leafs): %s' % len(self.leafs)

   __slots__ = (
      'rankings', 'ranklist', 'leafs'
   )

class SetEnumNode (object):

   def __init__(self, head, tail):

      self.head = head
      self.tail = tail

   def gen_sub_nodes (self):

      new_nodes = []
      for i, x in enumerate(self.tail):
         assert x not in self.head
         new_child_head = self.head + (x, )
         new_child = SetEnumNode(head=new_child_head,
                                 tail=self.tail[i+1::],
                                 )
         new_nodes.append(new_child)
         # yield new_child

      return new_nodes

   #same as above, except this recurses...
   def spawn_children_exhaustive (self, candidates):
      # assert isinstance(candidates, (ListType, TupleType))
      for i, x in enumerate(candidates):
         assert x not in self.head
         new_child_head = self.head + (x,)
         new_child = SetEnumNode(new_child_head,
                                 tail=[],
                                 )
         self.tail.append(x)
         new_candidates = candidates[i+1::]

         new_child.spawn_exhaustive(new_candidates)

   __slots__ = (
      'level',
      'head',
      'tail',
   )