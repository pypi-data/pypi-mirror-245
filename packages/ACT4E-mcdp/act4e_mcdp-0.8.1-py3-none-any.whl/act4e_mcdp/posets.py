from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Collection, Generic, Optional, TypeVar, cast

__all__ = [
    "FinitePoset",
    "Interval",
    "LowerSet",
    "Numbers",
    "Poset",
    "PosetProduct",
    "UpperSet",
]

T = TypeVar("T")


class Poset(ABC, Generic[T]):
    """

    The base class for Posets


    Note:
        This class is only a general superclass for posets.
        It does not contain interface/information
        regarding the partial-order itself.

    """

    @abstractmethod
    def leq(self, x: T, y: T) -> bool:
        """Returns True if x <= y."""
        ...

    @abstractmethod
    def join(self, values: Collection[T]) -> Optional[T]:
        """Returns the join (max) of objects, or None if not joinable."""
        ...

    @abstractmethod
    def meet(self, values: Collection[T]) -> Optional[T]:
        """Returns the meet (min) of objects, or None if not meetable."""
        ...

    @abstractmethod
    def largest_upperset_above(self, x: T) -> "UpperSet[T]":
        """Returns the largest upperset in this poset that contains the principal upper set of x."""
        ...

    @abstractmethod
    def largest_lowerset_below(self, x: T) -> "LowerSet[T]":
        """Returns the largest lowerset in this poset that contains the principal lower set of x."""
        ...

    @abstractmethod
    def global_minima(self) -> "UpperSet[T]":
        """Returns the global minima of the poset."""
        ...

    @abstractmethod
    def global_maxima(self) -> "LowerSet[T]":
        """Returns the global maxima of the poset."""
        ...

    @abstractmethod
    def belongs(self, x: T) -> bool:
        """Check if the element belongs to the poset."""
        ...

    def eq(self, x: T, y: T) -> bool:
        """Returns True if x == y."""
        return self.leq(x, y) and self.leq(y, x)

    def lt(self, x: T, y: T) -> bool:
        """Returns True if x < y."""
        return self.leq(x, y) and not self.leq(y, x)

    def gt(self, x: T, y: T) -> bool:
        """Returns True if x > y."""
        return self.lt(y, x)

    def geq(self, x: T, y: T) -> bool:
        """Returns True if x >= y."""
        return self.leq(y, x)

    def minimals(self, elements: Collection[T]) -> set[T]:
        """Returns the minimal elements of the set."""
        res: set[T] = set()
        for x in elements:
            # check if x is dominated by other things in res
            dominated = any(self.leq(already, x) for already in res)
            if dominated:
                continue

            # check if x dominates other things in res
            non_dominated = [already for already in res if not self.leq(x, already)]

            res = set(non_dominated + [x])
        return res

    def maximals(self, elements: Collection[T]) -> set[T]:
        """Returns the minimal elements of the set."""
        res: set[T] = set()
        for x in elements:
            # check if x is dominated by other things in res
            dominated = any(self.leq(x, already) for already in res)
            if dominated:
                continue

            # check if x dominates other things in res
            non_dominated = [already for already in res if not self.leq(already, x)]

            res = set(non_dominated + [x])
        return res

    @abstractmethod
    def close(self, x: T, y: T, /, *, atol: float, rtol: float) -> bool:
        """
        returns True if x and y are close enough according to the given absolute and relative tolerances.
        """


@dataclass
class Numbers(Poset[Decimal]):
    """

    This represents a closed interval of numbers.

    The top and bottom are given as decimals. Top might be +inf.

    The units are given as a string. If empty, the units are dimensionless.

    The **step** is given as a decimal. If 0, the poset is "continuous", in the
    sense that all decimals are allowed. If non-zero, then it represents the steps.
    For example, the natural numbers are given by bottom=0, top=+inf, step=1.

    The numbers [0.5, 1.0, 1.5, 2.0] are given by bottom=0.5, top=2.0, step=0.5.


    Attributes:
        bottom (Decimal): Lower bound of the interval.
        top (Decimal): Upper bound of the interval.
        step (Decimal): Step of the interval. If 0, the poset is "continuous".
        units (str): Units of the interval. If an empty string, the units are dimensionless.

    """

    bottom: Decimal
    top: Decimal
    step: Decimal  # if 0 = "continuous"
    units: str  # if empty = dimensionless

    def belongs(self, x: Decimal) -> bool:
        if not isinstance(x, Decimal):  # type: ignore
            raise TypeError(f"Expected Decimal, got {type(x).__name__} = {x!r}")
        if x < self.bottom:
            return False
        if x > self.top:
            return False
        if self.step == 0:
            return True

        if x.is_infinite():
            return True

        p = (x - self.bottom) / self.step
        if not p == p.__ceil__():
            return False
        return True

    def leq(self, x: Decimal, y: Decimal) -> bool:
        assert isinstance(x, Decimal), x
        assert isinstance(y, Decimal), y
        return x <= y

    def largest_upperset_above(self, x: Decimal) -> "UpperSet[Decimal]":
        """Returns the largest upperset in this poset that contains the principal upper set of x."""

        if not isinstance(x, Decimal):  # type: ignore
            raise TypeError(f"Expected Decimal, got {type(x).__name__} = {x!r}")

        # if x is greater than the top, then the largest upperset is empty!
        if x > self.top:
            return cast(UpperSet[Decimal], UpperSet.empty())

        # this takes care also of the case x = +inf
        if x == self.top:
            return UpperSet.principal(self.top)

        if x.is_infinite():  # this is -inf
            return UpperSet.principal(self.bottom)

        # at this point, we know that x is finite
        assert x.is_finite(), x

        # first clamp x to the valid range
        x = max(x, self.bottom)
        x = min(x, self.top)

        # then round it UP to the nearest multiple of step
        if self.step == 0:
            x_rounded = x
        else:
            x_rounded = self.bottom + ((x - self.bottom) / self.step).__ceil__() * self.step

        # it could be that x_rounded is greater than the top
        if x_rounded > self.top:
            return cast(UpperSet[Decimal], UpperSet.empty())

        # then return the principal upper set of x_rounded
        return UpperSet.principal(x_rounded)

    def largest_lowerset_below(self, x: Decimal) -> "LowerSet[Decimal]":
        if not isinstance(x, Decimal):  # type: ignore
            raise TypeError(f"Expected Decimal, got {type(x).__name__} = {x!r}")

        # if x is smaller than the bottom, then the largest lowerset is empty!
        if x < self.bottom:
            return cast(LowerSet[Decimal], LowerSet.empty())

        # this takes care also of the case x = -inf
        if x == self.bottom:
            return LowerSet.principal(self.bottom)

        if x.is_infinite():  # this is +inf
            return LowerSet.principal(self.top)

        # at this point, we know that x is finite

        assert x.is_finite(), x

        # first clamp x to the valid range
        x = max(x, self.bottom)
        x = min(x, self.top)

        # then round it DOWN to the nearest multiple of step
        if self.step == 0:
            x_rounded = x
        else:
            x_rounded = self.bottom + ((x - self.bottom) / self.step).__floor__() * self.step

        # it could be that x_rounded is smaller than the bottom
        if x_rounded < self.bottom:
            return cast(LowerSet[Decimal], LowerSet.empty())

        # then return the principal lowerset of x_rounded
        return LowerSet.principal(x_rounded)

    def join(self, values: Collection[Decimal]) -> Decimal:
        return max(values)

    def meet(self, values: Collection[Decimal]) -> Decimal:
        return min(values)

    def close(self, x: Decimal, y: Decimal, /, *, atol: float, rtol: float) -> bool:
        if x == y:
            return True
        if x.is_infinite() and not y.is_infinite():
            return False
        if y.is_infinite() and not x.is_infinite():
            return False
        return abs(x - y) <= max(Decimal(atol), Decimal(rtol) * max(abs(x), abs(y)))

    def global_minima(self) -> "UpperSet[Decimal]":
        return UpperSet.principal(self.bottom)

    def global_maxima(self) -> "LowerSet[Decimal]":
        return LowerSet.principal(self.top)


@dataclass
class FinitePoset(Poset[str]):
    """
    Represents a finite poset of elements


    Attributes:
        elements: A set of strings
        relations: A set of pairs of strings that represent the relations between the elements


    `('a', 'b')`  in relations represents `a <= b`

    Examples:

        >>> FinitePoset(elements={'a', 'b', 'c'}, relations={('a', 'b'), ('b', 'c')})

    """

    elements: set[str]
    relations: set[tuple[str, str]]

    def belongs(self, x: str) -> bool:
        if not isinstance(x, str):  # type: ignore
            raise TypeError(f"Expected str, got {type(x).__name__} = {x!r}")
        return x in self.elements

    def leq(self, x: str, y: str) -> bool:
        raise NotImplementedError("leq for FinitePoset")

    def join(self, values: Collection[str]) -> Optional[str]:
        raise NotImplementedError("join for FinitePoset")

    def meet(self, values: Collection[str]) -> Optional[str]:
        raise NotImplementedError("meet for FinitePoset")

    def largest_upperset_above(self, x: str) -> "UpperSet[str]":
        raise NotImplementedError("largest_upperset_above for FinitePoset")

    def largest_lowerset_below(self, x: str) -> "LowerSet[str]":
        raise NotImplementedError("largest_lowerset_below for FinitePoset")

    def close(self, x: str, y: str, /, *, atol: float, rtol: float) -> bool:
        return self.eq(x, y)

    def global_minima(self) -> "UpperSet[str]":
        raise NotImplementedError("global_minima for FinitePoset")

    def global_maxima(self) -> "LowerSet[str]":
        raise NotImplementedError("global_maxima for FinitePoset")


@dataclass
class PosetProduct(Generic[T], Poset[tuple[T, ...]]):
    """
    Represents the product of 0 or more posets.
    Its elements are tuples of elements of the posets.

    """

    def belongs(self, x: tuple[T, ...]) -> bool:
        if not isinstance(x, tuple):  # type: ignore
            raise TypeError(f"Expected tuple, got {type(x).__name__} = {x!r}")
        if len(x) != len(self.subs):
            raise ValueError(f"Expected tuple of length {len(self.subs)}, got {len(x)}")

        # logger.debug('belongs x %s  subs %s', x, self.subs)
        for xi, Pi in zip(x, self.subs):
            if not Pi.belongs(xi):
                return False
        return True

    subs: list[Poset[T]]

    def leq(self, x: tuple[T, ...], y: tuple[T, ...]) -> bool:
        assert len(x) == len(y)
        for P_i, x_i, y_i in zip(self.subs, x, y):
            if not P_i.leq(x_i, y_i):
                return False
        return True

    def join(self, values: Collection[tuple[T, ...]]) -> Optional[tuple[T, ...]]:
        raise NotImplementedError("join for PosetProduct")

    def meet(self, values: Collection[tuple[T, ...]]) -> Optional[tuple[T, ...]]:
        raise NotImplementedError("meet for PosetProduct")

    def largest_upperset_above(self, x: tuple[T, ...]) -> "UpperSet[tuple[T, ...]]":
        above = [P.largest_upperset_above(x_i) for P, x_i in zip(self.subs, x)]
        return UpperSet.product(above)

    def largest_lowerset_below(self, x: tuple[T, ...]) -> "LowerSet[tuple[T, ...]]":
        below = [P.largest_lowerset_below(x_i) for P, x_i in zip(self.subs, x)]
        return LowerSet.product(below)

    def close(self, x: tuple[T, ...], y: tuple[T, ...], /, *, atol: float, rtol: float) -> bool:
        for P_i, x_i, y_i in zip(self.subs, x, y):
            if not P_i.close(x_i, y_i, atol=atol, rtol=rtol):
                return False

        return True

    def global_minima(self) -> "UpperSet[tuple[T, ...]]":
        minima = [P.global_minima() for P in self.subs]
        return UpperSet.product(minima)

    def global_maxima(self) -> "LowerSet[tuple[T, ...]]":
        maxima = [P.global_maxima() for P in self.subs]
        return LowerSet.product(maxima)


@dataclass
class UpperSet(Generic[T]):
    """
    Describes a finitely-supported **upper set** of elements of type T.

    Attributes:
        minimals: A list of elements of type T, which are the minimal elements of the set.

    """

    minimals: list[T]

    @classmethod
    def from_points(
        cls,
        P: Poset[T],
        points: "Collection[T]",
    ) -> "UpperSet[T]":
        """Returns the lower set generated by the points."""
        minimals = P.minimals(points)
        return cls(minimals=list(minimals))

    @classmethod
    def principal(cls, value: T) -> "UpperSet[T]":
        return cls(minimals=[value])

    @classmethod
    def empty(cls) -> "UpperSet[T]":
        return cls(minimals=[])

    @classmethod
    def product(cls, sets: "Collection[UpperSet[T]]") -> "UpperSet[tuple[T, ...]]":
        """Computes the product of upper sets"""
        minimals_sets: list[list[T]] = [_.minimals for _ in sets]
        from itertools import product

        minimals: list[tuple[T, ...]] = list(product(*minimals_sets))
        return cls(minimals=minimals)  # type: ignore

    @classmethod
    def union(cls, sets: "Collection[UpperSet[T]]", P: Poset[T]) -> "UpperSet[T]":
        # Computes the union of upper sets in the Poset P

        all_elements: set[T] = set()
        for s in sets:
            all_elements.update(s.minimals)

        minimal_elements = P.minimals(all_elements)

        return cls(minimals=list(minimal_elements))

    @classmethod
    def close(cls, p: Poset[T], x: "UpperSet[T]", y: "UpperSet[T]", /, *, atol: float, rtol: float) -> bool:
        assert isinstance(x, UpperSet), x
        assert isinstance(y, UpperSet), y
        return close_seq(p, x.minimals, y.minimals, atol=atol, rtol=rtol)


def close_seq(p: Poset[T], x: "list[T]", y: "list[T]", /, *, atol: float, rtol: float) -> bool:
    if x and not y:
        return False
    if y and not x:
        return False
    for xi in x:
        nclose = 0
        for yi in y:
            if p.close(xi, yi, atol=atol, rtol=rtol):
                nclose += 1
                break
        if nclose == 0:
            return False

    for yi in y:
        nclose = 0
        for xi in x:
            if p.close(xi, yi, atol=atol, rtol=rtol):
                nclose += 1
                break
        if nclose == 0:
            return False
    return True


@dataclass
class LowerSet(Generic[T]):
    """
    Describes a finitely-supported **lower set** of elements of type T.

    Attributes:
        maximals: A list of elements of type T, which are the minimal elements of the set.

    """

    maximals: list[T]

    @classmethod
    def from_points(cls, P: Poset[T], points: "Collection[T]") -> "LowerSet[T]":
        """Returns the lower set generated by the points."""
        maximals = P.maximals(points)
        return cls(maximals=list(maximals))

    @classmethod
    def principal(cls, value: T) -> "LowerSet[T]":
        return cls(maximals=[value])

    @classmethod
    def empty(cls) -> "LowerSet[T]":
        return cls(maximals=[])

    @classmethod
    def product(cls, sets: "Collection[LowerSet[T]]") -> "LowerSet[tuple[T, ...]]":
        maximals_sets: list[list[T]] = [_.maximals for _ in sets]
        from itertools import product

        maximals = list(product(*maximals_sets))
        return cls(maximals=maximals)  # type: ignore

    @classmethod
    def union(cls, sets: "Collection[LowerSet[T]]", P: Poset[T]) -> "LowerSet[tuple[T, ...]]":
        # Computes the union of upper sets in the Poset P

        all_elements: set[T] = set()
        for s in sets:
            all_elements.update(s.maximals)

        maximal_elements = P.maximals(all_elements)

        return cls(maximals=list(maximal_elements))  # type: ignore

    @classmethod
    def close(cls, p: Poset[T], x: "LowerSet[T]", y: "LowerSet[T]", /, *, atol: float, rtol: float) -> bool:
        assert isinstance(x, LowerSet), x
        assert isinstance(y, LowerSet), y
        return close_seq(p, x.maximals, y.maximals, atol=atol, rtol=rtol)


@dataclass(kw_only=True)
class Interval(Generic[T]):
    """
    Describes an optimistic-pessimistic interval for a quantity of type T.

    The two values can be the same if there is no uncertainty.

    Attributes:
        pessimistic: The pessimistic value
        optimistic: The optimistic value

    """

    pessimistic: T
    optimistic: T

    @classmethod
    def degenerate(cls, value: T) -> "Interval[T]":
        return cls(pessimistic=value, optimistic=value)
