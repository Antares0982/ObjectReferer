import collections
import weakref
from typing import Dict, Generator, Generic, List, Set, Type, TypeVar

_T = TypeVar('_T')


class WeakRefSet(Generic[_T]):
    def __init__(self) -> None:
        self._set: Set[weakref.ref[_T]] = set()

    def add(self, obj: _T):
        self_ref = weakref.ref(self)

        def _remove(ref: weakref.ref[_T]) -> None:
            self = self_ref()
            if self is not None:
                self._set.remove(ref)
        self._set.add(weakref.ref(obj, _remove))

    def __iter__(self) -> Generator[_T, None, None]:
        l = list(self._set)
        for ref in l:
            obj = ref()
            if obj is not None:
                yield obj

    def __len__(self) -> int:
        return sum(1 for ref in self._set if ref() is not None)

    def __contains__(self, obj: _T) -> bool:
        if isinstance(obj, weakref.ref):
            return obj in self._set and obj() is not None
        return weakref.ref(obj) in self._set


class InheritanceTreeNode(Generic[_T]):
    __slots__ = ['kls', 'childrens',]

    def __init__(self, kls: Type[_T]) -> None:
        self.kls = kls
        self.childrens: List[InheritanceTreeNode] = []

    def __hash__(self) -> int:
        return hash(self.kls)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, InheritanceTreeNode) and self.kls == __value.kls

    def collect_by(self, s: Set[type]):
        if self.kls in s:
            return
        s.add(self.kls)
        for child in self.childrens:
            child.collect_by(s)


class ObjectReferrer(object):
    def __init__(self) -> None:
        self._object_weakref_sets: Dict[type, WeakRefSet] = collections.defaultdict(WeakRefSet)
        self._inheritance_trees: Dict[type, InheritanceTreeNode] = {}

    def register(self, obj: object) -> None:
        kls = obj.__class__
        self._object_weakref_sets[kls].add(obj)
        self._register_inheritance_tree(kls)

    def get(self, kls: Type[_T]) -> Generator[_T, None, None]:
        l = self._object_weakref_sets.get(kls)
        if l is not None:
            yield from l

    def get_by_base(self, kls: Type[_T]) -> Generator[_T, None, None]:
        node = self._inheritance_trees.get(kls)
        if node is None:
            return
        s: Set[type] = set()
        node.collect_by(s)
        for kls in s:
            yield from self.get(kls)

    def _register_inheritance_tree(self, kls: Type[_T]) -> InheritanceTreeNode[_T]:
        assert kls.__module__ != object.__module__  # do not register builtin classes!!
        son_node = self._inheritance_trees.get(kls)
        if son_node is not None:
            return son_node
        child_node = InheritanceTreeNode(kls)
        for base in kls.__bases__:
            if base.__module__ == object.__module__:
                continue
            base_node: InheritanceTreeNode = self._register_inheritance_tree(base)
            base_node.childrens.append(child_node)
        self._inheritance_trees[kls] = child_node
        return child_node

    def clear(self):
        self._object_weakref_sets.clear()
        self._inheritance_trees.clear()
