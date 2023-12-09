from __future__ import annotations
import itertools
from typing import (
    Callable,
    Iterable,
    TypeVar,
    Type,
    Any,
    Sized,
)

T = TypeVar("T")


class Predicates(object):
    """
    Collection of predicates for use in higher-order functions.
    """

    @classmethod
    def negation(cls, _predicate: Callable[[T], bool]) -> Callable[[T], bool]:
        """
        Determines the negation of the predicate.

        Signature: ``(T -> bool) -> (T) -> Bool``.
        """
        return lambda x: not _predicate(x)

    @classmethod
    def instanceof(cls, _type: Type[T]) -> Callable[[Any], bool]:
        """
        Given type ``T`` return predicate that evaluates true if instance of T.

        Signature: ``(T) -> (x) -> Bool``
        """
        return lambda x: isinstance(x, _type)

    @classmethod
    def not_instanceof(cls, _type: Type[T]) -> Callable[[Any], bool]:
        """
        The composition of :py:func:`P.instanceof` and :py:func:`P.negation`.

        Signature: ``(T) -> (x) -> Bool``.
        """
        return cls.negation(cls.instanceof(_type))

    @classmethod
    def empty(cls, _sized: Sized) -> bool:
        """
        Given argument with ``__len__``, evaluate true for non-zero ``__len__``.

        Signature: ``(x) -> Bool``.
        """
        return not len(_sized)

    @classmethod
    def singleton(cls, _sized: Sized) -> bool:
        """
        Given argument with ``__len__``, evaluate true for ``__len__`` of 1.

        Signature: ``(x) -> Bool``.
        """
        return len(_sized) == 1

    @classmethod
    def all(cls, _pred: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
        """
        Determines whether all elements of the iterable satisfy the predicate.

        Signature: ``(T -> Bool) -> ([T]) -> Bool``.

        This is equivalent to special fold ``all`` from haskell standard library
        https://hackage.haskell.org/package/base-4.19.0.0/docs/Prelude.html#g:14
        """
        return lambda x: all(map(_pred, x))

    @classmethod
    def any(cls, _pred: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
        """
        Determines whether any elements of the iterable satisfy the predicate.

        Signature: ``(T -> Bool) -> ([T]) -> Bool``.

        This is equivalent to special fold ``any`` from haskell standard library
        https://hackage.haskell.org/package/base-4.19.0.0/docs/Prelude.html#g:14
        """
        return lambda x: any(map(_pred, x))

    @classmethod
    def and_(cls, _iterable: Iterable[bool]) -> bool:
        """
        Determine the conjunction of the iterable of Boolean values.

        Signature: ``([Bool]) -> Bool``.

        This is equivalent to special fold ``and`` from haskell standard library
        https://hackage.haskell.org/package/base-4.19.0.0/docs/Prelude.html#g:14
        """
        return all(_iterable)

    @classmethod
    def or_(cls, _iterable: Iterable[bool]) -> bool:
        """
        Determine the disjunction of the iterable of Boolean values.

        Signature: ``([Bool]) -> Bool``.

        This is equivalent to special fold ``or`` from haskell standard library
        https://hackage.haskell.org/package/base-4.19.0.0/docs/Prelude.html#g:14
        """
        return any(_iterable)

    @classmethod
    def all_eq(cls, _iterable: Iterable[T]) -> bool:
        """
        Determines whether all elements of the iterable are equal.

        Signature: ``([T]) -> Bool``.

        Actual implementation from https://stackoverflow.com/a/3844832
        """
        g = itertools.groupby(iterable=_iterable)
        return next(g, True) and not next(g, False)


#: Alias ``P`` for ``Predicates``
P = Predicates
