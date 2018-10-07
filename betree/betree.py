import re


class Node(object):
    def __init__(self, key: int, value: str, *, evaluator=None, **evaluator_params):
        self.key = key
        self.value = value
        self.evaluator = evaluator if callable(evaluator) else lambda: NotImplemented
        self.evaluator_params = evaluator_params
        self.children = None
        if value in ('or', '||'):
            self.children_evaluator = any
        elif value in ('and', '&&'):
            self.children_evaluator = all
        else:
            self.children_evaluator = lambda *_: NotImplemented

    def __repr__(self):
        return f'{self.key}:{self.value}'

    def __call__(self):
        if self.children:
            return self.children_evaluator(c() for c in self.children)
        else:
            return self.evaluator(**self.evaluator_params)

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
    def __init__(self, root=None, nodes=None):
        self.root = root
        self.nodes = nodes

    def __repr__(self):
        return self.serialize()

    def __call__(self):
        r = self.root
        if not callable(r):
            raise ValueError
        return r()

    def get_node(self, key):
        return self.nodes.get(key)

    @classmethod
    def deserialize(cls, s):
        if not s or not isinstance(s, str):
            raise ValueError

        pattern = re.compile(r'\s+')
        s = re.sub(pattern, '', s)

        def parse_until_next_marker(i, s):
            begin = end = i + 1
            while s[end] not in ('(', ')'):
                end += 1
            return end, s[begin:end]

        nodes = {}
        cursor, l = 0, len(s)
        stack = []
        while cursor < l:
            c = s[cursor]
            if c == '(':  # push to stack
                cursor, r = parse_until_next_marker(cursor, s)
                node = Node.from_repr(r)
                if node.key in nodes:
                    raise KeyError(f'Duplicate node key found: {node.key}')
                nodes[node.key] = node
                stack.append(node)
            elif c == ')':  # make top of stack a child
                tos = stack.pop()
                if stack:
                    stack[-1].addChild(tos)
                cursor += 1
            else:
                raise ValueError(f'Expected cursor value: {cursor}')
        return Betree(root=tos, nodes=nodes)

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
