import scala.collection.JavaConversions._
//scala translation. disclaimer: have never run it yet and I probably never will considering the SetEnumTree
//is better in every way

class LexicoNode (level: Int,
  head: Set[String],
  tail: Set[String], //may want to consider making this mutable
  cNodes: java.util.HashMap[Set[String], LexicoNode],
  parentNode: Option[LexicoNode]) {

  val childrenNodes = cNodes

  var frequencyCount = 0

  def branch (transactions: List[String]): LexicoNode = {

    tail.addAll(for (t <- transactions if !head.contains(t)) yield t)

    val newHead = head.union(Set(transactions{level}))

    for (x <- transactions if newHead.contains(x) )yield x
    if (!childrenNodes.containsKey(newHead)) {
      childrenNodes.put(newHead, new LexicoNode (
        level+1,
        newHead,
        Set[String](),
        new java.util.HashMap[Set[String], LexicoNode](),
        Some(this)
      ))
    }

    childrenNodes.get(newHead)
  }

  def prune (child: Set[String]) {
    childrenNodes.remove(child)
  }
}

class LexicoTree (values: List[Set[String]], rankings:java.util.HashMap[String, Int]) {

  val nullNode = new LexicoNode(
    0,
    Set[String](),
    Set[String](),
    new java.util.HashMap[Set[String], LexicoNode](),
    None
  )

  for (x <- values) {
    addValueToTree (x)
  }

  def addValueToTree(xSet : Set[String]) = {
    val sortedList = xSet.toList.sortWith((x, y) => rankings.get(x) < rankings.get(y))

    var node = nullNode

    node.frequencyCount += 1

    for (_ <- sortedList) {
      node = node.branch(sortedList)
      node.frequencyCount += 1
    }
  }

  def traverseDepthFirst (f: LexicoNode => Unit, inode:Option[LexicoNode]) {
    val initialNode = inode match {
      case None => nullNode
      case Some(i) => i
    }

    f(initialNode)

    var queue = initialNode.childrenNodes.map {c => c._2}

    while (queue.size > 0) {
      f(queue.head)
      queue = queue.tail++queue.head.childrenNodes.map{c => c._2}
    }
  }
}
