class Node(object):
    def __init__(self, key: int, value: str, *, evaluator=lambda: NotImplemented):
        self.key = key
        self.value = value
        self.evaluator = evaluator
        self.children = None
    
    def __repr__(self):
        return f'{self.key}:{self.value}'
    
    def __call__(self):
        if self.children:
            if self.value == '||':
                return any(c() for c in self.children)
            elif self.value == '&&':
                return all(c() for c in self.children)
            else:
                raise ValueError(f'Unsupported value: {self.value}')
        else:
            return self.evaluator()

    @classmethod
    def from_repr(cls, s):
        k, v = s.split(':')
        return cls(int(k), v)
    
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
    
    def __call__(self):
        r = self.root
        if not callable(r):
            raise ValueError
        return r()
    
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
            if c == '(': # push to stack
                cursor, r = parse_until_next_marker(cursor, s)
                node = Node.from_repr(r)
                stack.append(node)
            elif c == ')': # make top of stack a child
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
    pass

if __name__ == '__main__':
    main()
