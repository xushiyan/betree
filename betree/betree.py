class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = None
    
    def addChild(self, node):
        if not isinstance(node, Node):
            raise TypeError
        if self.children is None:
            self.children = []
        self.children.append(node)

class Betree(object):
    def __init__(self, root=None):
        self.root = root

    def serialize(self):
        parts = []
        self._preorder(parts, self.root)
        return ''.join(parts)
    
    def _preorder(self, parts, node):
        if not node:
            return
        parts.append('(')
        parts.append(str(node.value))
        if node.children:
            for child in node.children:
                self._preorder(parts, child)
        parts.append(')')
    
def main():
    a = Node(1, 'a')
    b = Node(2, 'b')
    c = Node(3, 'c')
    d = Node(4, 'd')
    e = Node(5, 'e')
    f = Node(6, 'f')
    g = Node(7, 'g')
    h = Node(8, 'h')
    i = Node(9, 'i')
    j = Node(10, 'j')
    k = Node(11, 'k')

    a.addChild(b)
    a.addChild(c)
    a.addChild(d)

    b.addChild(e)
    b.addChild(f)

    f.addChild(k)

    d.addChild(g)
    d.addChild(h)
    d.addChild(i)
    d.addChild(j)

    t = Betree(root=a)
    print(t.serialize())

if __name__ == '__main__':
    main()
