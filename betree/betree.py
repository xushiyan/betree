class Node(object):
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value
        self.children = None
    
    def __repr__(self):
        return f'{self.key}:{self.value}'
    
    @classmethod
    def from_repr(self, s):
        k, v = s.split(':')
        return Node(int(k), v)
    
    def addChild(self, node):
        if not isinstance(node, Node):
            raise TypeError
        if self.children is None:
            self.children = []
        self.children.append(node)

class Betree(object):
    def __init__(self, root=None):
        self.root = root
    
    def __repr__(self):
        return self.serialize()
    
    @classmethod
    def deserialize(cls, s):
        if not s or not isinstance(s, str):
            raise ValueError
        
        def parse_until_next_marker(i, s):
            begin = end = i + 1
            while s[end] not in ('(', ')'):
                end += 1
            return end, s[begin:end]
        
        cursor, l = 0, len(s)
        stack = []
        while cursor < l:
            c = s[cursor]
            if c == '(': 
                # push to stack
                cursor, r = parse_until_next_marker(cursor, s)
                node = Node.from_repr(r)
                stack.append(node)
            elif c == ')':
                # make top of stack a child
                tos = stack.pop()
                if stack:
                    stack[-1].addChild(tos)
                cursor += 1
            else:
                raise ValueError(f'Expected cursor value: {cursor}')
        return Betree(root=tos)

    def serialize(self):
        parts = []
        self._preorder(parts, self.root)
        return ''.join(parts)
    
    def _preorder(self, parts, node):
        if not node:
            return
        parts.append('(')
        parts.append(repr(node))
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
    s = repr(t)
    print(s)
    t = Betree.deserialize(s)
    print(t)

if __name__ == '__main__':
    main()
