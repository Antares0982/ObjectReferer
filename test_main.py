if __name__ == "__main__":
    from object_referer import ObjectReferrer
    referer = ObjectReferrer()

    class Base(object):
        def __init__(self) -> None:
            referer.register(self)

        def f(self):
            print("Base.f")

    class A(Base):
        def f(self):
            print("A.f")

    class B(Base):
        def f(self):
            print("B.f")

    class Child(A, B):
        def f(self):
            print("Child.f")

    def do(kls):
        for obj in referer.get_by_base(kls):
            obj.f()

    child = Child()

    print("Expected: Child.f * 4")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    a = A()
    b = B()

    print("Expected: Child.f * 4, A.f * 2, B.f * 2")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    base = Base()

    print("Expected: Child.f * 4, A.f * 2, B.f * 2, Base.f * 1")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    del a

    print("Expected: Child.f * 4, B.f * 2, Base.f * 1")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    del child

    print("Expected: B.f * 2, Base.f * 1")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    del base

    print("Expected: B.f * 2")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    del b

    print("Expected: Nothing")

    do(Base)
    do(A)
    do(B)
    do(Child)

    print("----------")

    print("Test over!")
