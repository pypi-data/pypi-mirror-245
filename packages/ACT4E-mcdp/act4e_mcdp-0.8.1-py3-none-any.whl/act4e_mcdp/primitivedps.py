from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Generic, Optional, TypeVar

from .coords import Coords
from .posets import Numbers, Poset, PosetProduct

__all__ = [
    "AmbientConversion",
    "CatalogueDP",
    "Constant",
    "DPLoop2",
    "DPSeries",
    "EntryInfo",
    "IdentityDP",
    "JoinNDP",
    "Limit",
    "M_Ceil_DP",
    "M_FloorFun_DP",
    "M_Fun_AddConstant_DP",
    "M_Fun_AddMany_DP",
    "M_Fun_MultiplyConstant_DP",
    "M_Fun_MultiplyMany_DP",
    "M_Fun_MultiplyMany_DP",
    "M_Power_DP",
    "M_Res_AddConstant_DP",
    "M_Res_AddMany_DP",
    "M_Res_DivideConstant_DP",
    "M_Res_MultiplyConstant_DP",
    "M_Res_MultiplyMany_DP",
    "MeetNDualDP",
    "MeetNDualDP",
    "Mux",
    "ParallelDP",
    "PrimitiveDP",
    "UnitConversion",
    "ValueFromPoset",
]

F = TypeVar("F")
R = TypeVar("R")

FT = TypeVar("FT")
RT = TypeVar("RT")
T = TypeVar("T")

Fcov = TypeVar("Fcov", covariant=True)
Rcov = TypeVar("Rcov", covariant=True)


@dataclass(frozen=True)
class PrimitiveDP(Generic[Fcov, Rcov]):
    r"""
    A generic PrimitiveDP; a morphism of the category DP.

    Other classes derive from this.

    Attributes:
        description: An optional string description.
        F: The functionality poset $\F$
        R: The resources poset $\R$


    Note:
        This class is only a general superclass
        for morphisms of the category DP.
        It does not contain interface/information
        regarding the feasible relationship itself.

    """

    description: Optional[str]
    F: Poset[Fcov]
    R: Poset[Rcov]


@dataclass(frozen=True)
class DPSeries(PrimitiveDP[object, object]):
    r"""
    A series composition of two or more DPs.

    Attributes:
        F: The functionality poset $\F$
        R: The resources poset $\R$
        subs: The list of DPs
    """

    subs: list[PrimitiveDP[object, object]]


@dataclass(frozen=True)
class ParallelDP(Generic[FT, RT], PrimitiveDP[tuple[FT, ...], tuple[RT, ...]]):
    r"""
    This is the parallel composition of two or more DPs.

    Note that the functionality poset is a PosetProduct of the functionality posets of the sub-DPs.
    The same holds for the resources poset.


    """
    F: PosetProduct[FT]
    R: PosetProduct[RT]

    subs: list[PrimitiveDP[FT, RT]]


@dataclass(frozen=True)
class ValueFromPoset(Generic[T]):
    r"""
    A value in a particular poset (a "typed" value).

    Depending on the poset, we have different types:

    - For [FinitePoset][act4e_mcdp.posets.FinitePoset] the values are strings.
    - For [Numbers][act4e_mcdp.posets.Numbers] the values are instances of Decimal.
    - For [PosetProduct][act4e_mcdp.posets.PosetProduct] the values are tuples of values.


    Attributes:
        value (str | Decimal | tuple): The value $x \in \posA$
        poset: The poset $\posA$

    """

    value: T
    poset: Poset[T]


@dataclass(frozen=True)
class M_Res_MultiplyConstant_DP(PrimitiveDP[Decimal, Decimal]):
    r"""
    Multiplication by a constant on the left side.

    Relation:

        $$
            \fun \cdot_{\opspace} v \leq_{\opspace} \res
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        vu: The value $v$ to be added.
        opspace: The poset $\opspace$ where the multiplication and comparison take place.

    """
    F: Numbers
    R: Numbers
    vu: ValueFromPoset[Decimal]
    opspace: Numbers


@dataclass(frozen=True)
class M_Res_DivideConstant_DP(PrimitiveDP[Decimal, Decimal]):
    r"""

    Division by a constant

    Relation:

        $$
            \fun /_{\opspace} v \leq_{\opspace} \res
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        vu: The value $v$ to be added.
        opspace: The poset $\opspace$ where the division and comparison take place.
    """

    F: Numbers
    R: Numbers
    vu: ValueFromPoset[Decimal]
    opspace: Numbers


@dataclass(frozen=True)
class M_Fun_MultiplyConstant_DP(PrimitiveDP[Decimal, Decimal]):
    r"""
    Multiplication by a constant on the right side.

    Relation:

        $$
            \fun \leq_{\opspace} \res  \cdot_{\opspace} v
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        vu: The value $v$ to be added.
        opspace: The poset $\opspace$ where the multiplication and comparison take place.

    """
    F: Numbers
    R: Numbers
    vu: ValueFromPoset[Decimal]
    opspace: Numbers


@dataclass(frozen=True)
class M_Res_AddConstant_DP(PrimitiveDP[Decimal, Decimal]):
    r"""
    Addition of a constant on the left side.

    Relation:

        $$
            \fun +_{\opspace} v \leq_{\opspace} \res
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        vu: The value $v$ to be added.
        opspace: The poset $\opspace$ where the multiplication and comparison take place.

    """
    F: Numbers
    R: Numbers
    vu: ValueFromPoset[Decimal]
    opspace: Numbers


@dataclass(frozen=True)
class M_Fun_AddMany_DP(PrimitiveDP[Decimal, tuple[Decimal, ...]]):
    r"""
    Addition on the right side.

    The resources posets is a PosetProduct of, in general, $n$ elements $\F_1, \F_2, \dots$.
    (You can assume $n = 2$).


    Relation:

        $$
            \fun \leq_{\opspace}  \res_1 +_{\opspace} \res_2 +_{\opspace} \dots
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        opspace: The poset $\opspace$ where the operations and comparisons take place.

    """
    opspace: Numbers


@dataclass(frozen=True)
class M_Res_AddMany_DP(PrimitiveDP[tuple[Decimal, ...], Decimal]):
    r"""
    Addition on the left side.


    Relation:

        $$
            \fun_1 +_{\opspace} \fun_2 +_{\opspace} \dots \leq_{\opspace}  \res
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        opspace: The poset $\opspace$ where the operations and comparisons take place.

    """
    F: PosetProduct[Decimal]
    R: Numbers
    opspace: Numbers


@dataclass(frozen=True)
class JoinNDP(Generic[T], PrimitiveDP[tuple[T, ...], T]):
    r"""
    This DP is used as plumbing. It is the dual of [MeetNDualDP][act4e_mcdp.primitivedps.MeetNDualDP].


    The functionality posets is a PosetProduct of, in general, $n$ elements $\F_1, \F_2, \dots$.

    We ask that the resource is greater than each of the functionalities.

    The comparison is done in a poset $\opspace$ which contains $\R, \F_1, \F_2,  \dots$.

    Relation:

        $$
            (\fun_1 \leq_{\opspace}  \res) \wedge (\fun_2 \leq_{\opspace} \res) \wedge \dots
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        opspace: The poset $\opspace$ where the comparisons take place.


    """
    F: PosetProduct[T]
    R: Poset[T]
    opspace: Poset[T]


@dataclass(frozen=True)
class MeetNDualDP(Generic[T], PrimitiveDP[T, tuple[T, ...]]):
    r"""
    This DP is used as plumbing. It is the dual of [JoinNDP][act4e_mcdp.primitivedps.JoinNDP].

    The resources posets is a PosetProduct of, in general, $n$ elements $\R_1, \R_2, \dots$.

    We ask that the functionality is less than each of the resources.

    The comparison is done in a poset $\opspace$ which contains $\F, \R_1, \R_2, \dots$.

    Relation:

        $$
            (\fun \leq_{\opspace}  \res_1) \wedge (\fun \leq_{\opspace} \res_2) \wedge \dots
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        opspace: The poset $\opspace$ where the comparisons take place.


    """
    F: Poset[T]
    R: PosetProduct[T]
    opspace: Poset[T]


@dataclass(frozen=True)
class Mux(PrimitiveDP[object, object]):
    r""" """

    coords: Coords
    coords2: Coords

    def __post_init__(self):
        assert isinstance(self.coords, Coords), self


@dataclass(frozen=True)
class M_Power_DP(PrimitiveDP[Decimal, Decimal]):
    r"""
    Exponentiation of functionalities.


    Relation:

        $$
            \fun ^ (n / d) \leq_{\opspace}  \res
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        num: numerator of the exponent
        den: denominator of the exponent

    """
    num: int
    den: int


@dataclass(frozen=True)
class M_Fun_MultiplyMany_DP(PrimitiveDP[Decimal, tuple[Decimal, ...]]):
    r"""
    Multiplication on the right side.


    Relation:

        $$
            \fun \leq_{\opspace}  \res_1 \cdot_{\opspace} \res_2 \cdot_{\opspace} \dots
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        opspace: The poset $\opspace$ where the operations and comparisons take place.
    """
    opspace: Numbers


@dataclass(frozen=True)
class M_Res_MultiplyMany_DP(PrimitiveDP[tuple[Decimal, ...], Decimal]):
    r"""
    Multiplication on the left side.


    Relation:

        $$
            \fun_1 \cdot_{\opspace} \fun_2 \cdot_{\opspace} \dots \leq_{\opspace}  \res
        $$

    Attributes:
        F (Poset): The functionality poset $\F$ must be Numbers
        R (Poset): The resources poset $\R$ must be Numbers
        opspace: The poset $\opspace$ where the operations and comparisons take place.

    """
    F: PosetProduct[Decimal]
    R: Numbers
    opspace: Numbers


@dataclass(frozen=True)
class M_Ceil_DP(PrimitiveDP[Decimal, Decimal]):
    r"""

    Relation:

        $$
            \text{ceil}(\fun) ≤_{\opspace} \res
        $$

    Attributes:
       F (Poset): The functionality poset $\F$ must be Numbers
       R (Poset): The resources poset $\R$ must be Numbers
       opspace: The poset $\opspace$ where the comparisons take place.

    """
    F: Numbers
    R: Numbers
    opspace: Numbers


@dataclass(frozen=True)
class M_FloorFun_DP(PrimitiveDP[Decimal, Decimal]):
    r"""

    Relation:

        $$
            \fun ≤_{\opspace} \text{floor}(\res)
        $$

    Attributes:
       F (Poset): The functionality poset $\F$
       R (Poset): The resources poset $\R$
       opspace: The poset $\opspace$ where the comparisons take place.

    """

    opspace: Numbers
    F: Numbers
    R: Numbers


@dataclass(frozen=True)
class M_Fun_AddConstant_DP(PrimitiveDP[Decimal, Decimal]):
    r"""
    Addition of a constant on the right side.

    Relation:

        $$
            \fun \leq_{\opspace} \res +_{\opspace} v
        $$

    Attributes:
        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        vu: The value $v$ to be added.
        opspace: The poset $\opspace$ where the multiplication and comparison take place.

    """
    F: Numbers
    R: Numbers
    vu: ValueFromPoset[Decimal]
    opspace: Numbers


@dataclass(frozen=True)
class UnitConversion(PrimitiveDP[Decimal, Decimal]):
    r"""

    A unit conversion between real numbers
    given by a factor F (a fraction).

    Relation:

        $$
          \fun \cdot \text{factor} \leq \res
        $$


    Attributes:

        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        factor: The fraction $\text{factor}$

    """
    F: Numbers
    R: Numbers
    opspace: Numbers
    factor: Fraction


@dataclass(frozen=True)
class AmbientConversion(Generic[T], PrimitiveDP[T, T]):
    r"""
    A "conversion" between two posets $\F, \R$ that are subposets of a common ambient poset $\common$.

    Relation:

        $$
          \fun \leq_{\common}  \res
        $$

        where $\common$ is the common ambient poset.

    Attributes:

        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        common: The common ambient poset $\common$

    """
    F: Poset[T]
    R: Poset[T]
    common: Poset[T]


@dataclass(frozen=True)
class IdentityDP(Generic[T], PrimitiveDP[T, T]):
    r"""
    This is the identity DP ($\F = \R$)

    Relation:

        $$
          \fun \leq \res
        $$


    Attributes:

        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$


    Note:

        It can be seen as a special case
        of [AmbientConversion][act4e_mcdp.primitivedps.AmbientConversion]
        where $\common = \F = \R$.
    """
    F: Poset[T]
    R: Poset[T]


F1 = TypeVar("F1")

R1 = TypeVar("R1")
M = TypeVar("M")


@dataclass(frozen=True)
class DPLoop2(Generic[F1, R1, M], PrimitiveDP[F1, R1]):
    r""" """
    dp: PrimitiveDP[tuple[F1, M], tuple[R1, M]]


@dataclass(frozen=True)
class Limit(Generic[T], PrimitiveDP[T, tuple[()]]):
    r"""
    Implements a bound on the functionality.

    This is the dual of [Constant][act4e_mcdp.primitivedps.Constant].

    Relation:

        $$
          \fun \leq  c
        $$

    Note that the resources $\res$ do not appear in the relation.
    As long as the functionality is below the limit, the resources can be anything.

    Attributes:

        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        c: The constant $c$

    """

    F: Poset[T]
    R: Poset[tuple[()]]

    c: ValueFromPoset[T]


@dataclass(frozen=True)
class Constant(Generic[T], PrimitiveDP[tuple[()], T]):
    r"""
    Implements a bound on the resources.

    This is the dual of [Limit][act4e_mcdp.primitivedps.Limit].

    Relation:

        $$
          c \leq  \res
        $$

        Note that the functionality $\fun$ do not appear in the relation.
        As long as the resources is above the limit, the functionality can be anything.

    Attributes:

        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        c: The constant $c$

    """

    F: Poset[tuple[()]]
    R: Poset[T]

    c: ValueFromPoset[T]


@dataclass(frozen=True)
class EntryInfo(Generic[FT, RT]):
    r"""
    Describes $\fun^{\max}_{\imp}$ and $\res^{\min}_{\imp}$ for an implementation.


    Attributes:
        f_max: The maximum functionality $\fun^{\max}_{\imp}$
        r_min: The minimum resources $\res^{\min}_{\imp}$

    """
    f_max: FT
    r_min: RT


@dataclass(frozen=True)
class CatalogueDP(Generic[FT, RT], PrimitiveDP[FT, RT]):
    r"""
    Implements a catalogue.

    The available implementations are strings and each of them has a (max) functionality and a (min) resource.

    Relation:

        $$
           \bigvee_{\imp \in \impspace}   ( \fun \leq \fun^{\max}_{\imp}) \wedge (\res^{\min}_{\imp} \leq
           \res)
        $$

        where $\impspace$ is the set of implementations and $\fun^{\max}_{\imp}, \res^{\min}_{\imp}$ are
        the functionality and resources of the implementation $\imp$.

    Attributes:

        F (Poset): The functionality poset $\F$
        R (Poset): The resources poset $\R$
        entries: A dictionary of entries.

    """

    entries: dict[str, EntryInfo[FT, RT]]
