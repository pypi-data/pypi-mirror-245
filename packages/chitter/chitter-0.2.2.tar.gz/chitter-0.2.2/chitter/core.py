from __future__ import annotations

import builtins
import collections
import functools
import itertools
import typing

T = typing.TypeVar("T")

if typing.TYPE_CHECKING:
    from typing import Callable, Self, Protocol, Any, ParamSpec
    from collections.abc import Iterable, Iterator, Sequence

    class SupportsLessThan(Protocol):

        def __lt__(self, __other: Any) -> bool:
            ...

    KeyFunc = Callable[[T], SupportsLessThan]
    Predicate = Callable[[T], bool]
    U = typing.TypeVar("U")
    P = ParamSpec('P')


def magicify(func):

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # make sure self is an `ChainableIter` in case it's called as a "static" function
        if not isinstance(self, ChainableIter):
            self = ChainableIter(self)
        # make sure the output gets wrapped up as `ChainableIter` as well
        result = func(self, *args, **kwargs)
        if not isinstance(result, ChainableIter):
            result = ChainableIter(result)
        return result

    return wrapper


class ChainableIter(typing.Generic[T]):
    """
    Wrapper class around python iterators

    After wrapping any iterable in this class it will have access to all the methods listed below.
    These methods also return an `ChainableIter` instance to make them chainable.
    """

    # ==== BASICS ====

    def __init__(
        self,
        iterable: Iterable[T],
    ) -> None:
        self._iterator = builtins.iter(iterable)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        return next(self._iterator)

    # ==== TRANSFORMATIONS (ChainableIter -> ChainableIter) ====

    # TODO:
    # step_by
    # group_by (itertools)

    def sorted(self, *, key: KeyFunc[T] | None = None, reverse: bool = False) -> ChainableIter[T]:
        """This method is not good performance-wise"""
        return ChainableIter(sorted(
            list(self),
            key=key, # type: ignore
            reverse=reverse,
        ))

    def reversed(self) -> ChainableIter[T]:
        """This method is not good performance-wise"""
        return ChainableIter(reversed(list(self)))

    def map(self, function: Callable[[T], U]) -> ChainableIter[U]:
        return ChainableIter(builtins.map(function, self))

    def flatten(self) -> ChainableIter[Any]:   # TODO: type annotations
        return ChainableIter(itertools.chain.from_iterable(self))   # type: ignore

    def flat_map(self, function: Callable[[T], Iterable[U]]) -> ChainableIter[U]:
        return self.map(function).flatten()

    def star_map(self, function) -> ChainableIter[Any]:   # TODO: type annotations
        return ChainableIter(itertools.starmap(function, self))   # type: ignore

    def filter(self, predicate: Predicate | None = None) -> ChainableIter[T]:
        return ChainableIter(builtins.filter(
            function=predicate, # type: ignore
            iterable=self,
        ))

    def filter_false(self, predicate: Predicate[T] | None = None) -> ChainableIter[T]:
        return ChainableIter(itertools.filterfalse(predicate, self))

    def enumerate(self, start: int = 0) -> ChainableIter[tuple[int, T]]:
        return ChainableIter(builtins.enumerate(self, start))

    def zip(self, *others: Iterable[Any], strict: bool = False) -> ChainableIter[tuple[Any, ...]]:
        return ChainableIter(builtins.zip(self, *others, strict=strict))

    def zip_longest(
        self,
        *others: Iterable[Any],
        fill_value: Any = None,
    ) -> ChainableIter[tuple[Any, ...]]:
        return ChainableIter(itertools.zip_longest(self, *others, fillvalue=fill_value))

    def slice(self, s: slice) -> ChainableIter[T]:
        return ChainableIter(itertools.islice(self, s.start, s.stop, s.step))

    def take(self, n: int) -> ChainableIter[T]:
        return self.slice(slice(n))

    def take_while(self, predicate: Predicate[T]) -> ChainableIter[T]:
        return ChainableIter(itertools.takewhile(predicate, self))

    def drop(self, n: int | None) -> Self:
        "Advance the iterator n-steps ahead. If n is None, consume entirely."
        if n is None:
            collections.deque(self, maxlen=0)
        else:
            next(self.slice(slice(n, n)), None)
        return self

    def drop_while(self, predicate: Predicate[T]) -> ChainableIter[T]:
        return ChainableIter(itertools.dropwhile(predicate, self))

    def inspect(self, function: Callable[[T], None]) -> ChainableIter[T]:
        # FIXME: kind of a sloppy implementation
        def _inspect(iterator: Iterable[T], function: Callable[[T], None]) -> Iterable[T]:
            for i in iterator:
                function(i)
                yield i

        return ChainableIter(_inspect(self, function))

    def chain(self, *iterables: Iterable[T]) -> ChainableIter[T]:
        return ChainableIter(itertools.chain(self, *iterables))

    def compress(self, selectors: Iterable[object]) -> ChainableIter[T]:
        return ChainableIter(itertools.compress(self, selectors))

    def product(self, *iterables, repeat=1) -> 'ChainableIter':
        return ChainableIter(itertools.product(self, *iterables, repeat=repeat))

    def permutations(self, length: int | None = None) -> ChainableIter[tuple[T, ...]]:
        return ChainableIter(itertools.permutations(self, r=length))

    def combinations(self, length: int) -> ChainableIter[tuple[T, ...]]:
        return ChainableIter(itertools.combinations(self, r=length))

    def combinations_with_replacement(self, length: int) -> ChainableIter[tuple[T, ...]]:
        return ChainableIter(itertools.combinations_with_replacement(self, r=length))

    def cycle(self) -> ChainableIter[T]:
        return ChainableIter(itertools.cycle(self))

    def _split_head(self, predicate: Predicate[T]) -> ChainableIter[ChainableIter[T]]:
        batch: list[T] = []
        for item in self:
            if predicate(item):
                yield ChainableIter(batch)
                batch = []
            batch.append(item)
        yield ChainableIter(batch)

    def split_head(self, predicate: Predicate[T]) -> ChainableIter[ChainableIter[T]]:
        return ChainableIter(self._split_head(predicate))

    def _split_tail(self, predicate: Predicate[T]) -> ChainableIter[ChainableIter[T]]:
        batch: list[T] = []
        for item in self:
            batch.append(item)
            if predicate(item):
                yield ChainableIter(batch)
                batch = []
        yield ChainableIter(batch)

    def split_tail(self, predicate: Predicate[T]) -> ChainableIter[ChainableIter[T]]:
        return ChainableIter(self._split_tail(predicate))

    def _split(self, predicate: Predicate[T]) -> Iterable[ChainableIter[T]]:
        batch: list[T] = []
        for item in self:
            if predicate(item):
                yield ChainableIter(batch)
                batch = []
            else:
                batch.append(item)
        yield ChainableIter(batch)

    def split(self, predicate: Predicate[T]) -> ChainableIter[ChainableIter[T]]:
        return ChainableIter(self._split(predicate))

    # ==== TERMINATORS (ChainableIter -> object) ====

    # TODO:
    # all
    # any
    # min, max
    # sum
    # product # conflicts with the cartesian/set product
    # length

    def first(self, default: Any = None) -> T | Any:
        return next(self, default)

    def nth(self, index: int) -> T | None:
        return self.drop(index).first()

    def last(self, default: Any = None) -> T | Any:
        item = default
        for item in self:
            pass
        return item

    def for_each(self, func: Callable[[T], None]) -> None:
        for item in self:
            func(item)

    def find(self, needle: T, default: Any = None) -> tuple[int, T] | Any:
        return self.enumerate().drop_while(lambda item: item[1] != needle).first(default)

    def tee(self, n: int) -> tuple[ChainableIter[T], ...]:
        return tuple(ChainableIter(i) for i in itertools.tee(self, n))

    def partition(self, predicate: Predicate[T]) -> tuple[ChainableIter[T], ChainableIter[T]]:
        "Use a predicate to partition entries into false entries and true entries"
        # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
        t1, t2 = itertools.tee(self)
        return ChainableIter(t1).filter_false(predicate), ChainableIter(t2).filter(predicate)

    def reduce(self, initial: T, function: Callable[[T, T], T]) -> T:
        return functools.reduce(function, self, initial)

    def next(self, default: Any = None) -> T | Any:
        return next(self, default)

    def collect(self, constructor: Callable[[Iterable[T]], Sequence[T]]) -> Sequence[T]:
        return constructor(self)

    def to_list(self) -> list[T]:
        return typing.cast(list[T], self.collect(list))

    # ==== Generators (new ChainableIter) ====

    # TODO:
    # successors (rust)
    # unzip

    @classmethod
    def range(cls, *args) -> ChainableIter[int]:
        return ChainableIter(range(*args))

    @classmethod
    def count(cls, start: int = 0, step: int = 1) -> ChainableIter[int]:
        return ChainableIter(itertools.count(start, step))

    @classmethod
    def repeat(cls, item: T, times: int | None = None) -> ChainableIter[T]:
        return ChainableIter(itertools.repeat(item, times))   # type: ignore
