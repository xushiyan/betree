from unittest import TestCase

from betree import Betree, Node

class DeserTestCase(TestCase):
    def setUp(self):
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

        self.t = Betree(root=a)

    def test_deser(self):
        s = self.t.serialize()
        t = Betree.deserialize(s)
        self.assertEqual(s, repr(t))

class BoolEvaluationTestCase(TestCase):
    def test_simple_AND_evaluation(self):
        a = Node(1, '&&')
        b = Node(2, 'purchased', evaluator=lambda: False)
        c = Node(3, 'activated', evaluator=lambda: False)
        a.addChild(b)
        a.addChild(c)
        t = Betree(root=a) 
        self.assertFalse(t())
        b.evaluator = lambda: True
        self.assertFalse(t())
        c.evaluator = lambda: True
        self.assertTrue(t())

    def test_simple_OR_evaluation(self):
        a = Node(1, '||')
        b = Node(2, 'purchased', evaluator=lambda: False)
        c = Node(3, 'activated', evaluator=lambda: False)
        a.addChild(b)
        a.addChild(c)
        t = Betree(root=a) 
        self.assertFalse(t())
        b.evaluator = lambda: True
        self.assertTrue(t())
        c.evaluator = lambda: True
        self.assertTrue(t())
