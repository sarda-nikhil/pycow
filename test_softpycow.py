from pycow import Proxy

def test_softpycow():
    class Point:
        x = None
        y = None
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class TwoPoints:
        a = None
        b = None
        def __init__(self, a, b):
            self.a = a
            self.b = b

    a = Point(1,2)
    b = Point(3,4)
    c = TwoPoints(a,b)
    d = Proxy(c)

    a.x = 10
    assert c.a.x == 10
    assert d.a.x == 10

    b.y = 20
    assert c.b.y == 20
    assert d.b.y == 20

    assert isinstance(d.a, Proxy)
    assert isinstance(d.b, Proxy)
    
    d.a.x = 100
    assert d.a.x == 100
    assert d.a.y == a.y
    assert a.x == 10
    assert c.a.x == 10
    assert isinstance(d.a, Point)
    assert isinstance(d.b, Point)
    assert isinstance(d, TwoPoints)
