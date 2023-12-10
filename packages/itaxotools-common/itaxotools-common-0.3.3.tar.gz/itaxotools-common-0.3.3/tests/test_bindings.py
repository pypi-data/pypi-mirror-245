from itaxotools.common.bindings import Binder, Property, PropertyObject


class DummyObject(PropertyObject):
    dummy = Property(int, 0)


def test_simple_bind(qapp):
    a = DummyObject()
    b = DummyObject()

    binder = Binder()
    binder.bind(a.properties.dummy, b.properties.dummy)

    assert b.dummy == 0
    a.dummy = 42
    assert b.dummy == 42


def test_proxy_bind(qapp):
    a = DummyObject()
    b = DummyObject()

    binder = Binder()
    binder.bind(a.properties.dummy, b.properties.dummy, proxy=lambda x: x + 1)

    assert b.dummy == 1
    a.dummy = 42
    assert b.dummy == 43


def test_conditional_bind(qapp):
    a = DummyObject()
    b = DummyObject()

    binder = Binder()
    binder.bind(a.properties.dummy, b.properties.dummy, condition=lambda x: x > 10)

    assert b.dummy == 0

    a.dummy = 9
    assert b.dummy == 0

    a.dummy = 11
    assert b.dummy == 11


def test_binder_update(qapp):
    a = DummyObject()
    b = DummyObject()

    binder = Binder()
    binder.bind(a.properties.dummy, b.properties.dummy)

    a.dummy = 1
    assert b.dummy == 1

    b.dummy = 2
    assert b.dummy == 2

    binder.update()
    assert b.dummy == 1


def test_property_tags(qapp):
    class DummyTaggedObject(PropertyObject):
        x = Property(int, 0, tag="x")
        y = Property(int, 0, tag="y")
        z = Property(int, 0)

    a = DummyTaggedObject()

    assert a.properties.x.tag == "x"
    assert a.properties.y.tag == "y"
    assert a.properties.z.tag is None


def test_property_iteration(qapp):
    class DummyTaggedObject(PropertyObject):
        x = Property(int, 1)
        y = Property(int, 2)
        z = Property(int, 3)

    a = DummyTaggedObject()

    assert [x.key for x in a.properties] == ["x", "y", "z"]
    assert [x.value for x in a.properties] == [1, 2, 3]
