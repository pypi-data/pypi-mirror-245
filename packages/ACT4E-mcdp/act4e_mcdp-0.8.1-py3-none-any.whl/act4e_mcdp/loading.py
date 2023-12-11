from decimal import Decimal
from typing import Any, Callable, Optional, Type, TypeVar, cast

import yaml

from . import logger
from .coords import ComposeList, Coords, CoordsComp, CoordsIdentity
from .nameddps import (
    CompositeNamedDP,
    Connection,
    ModelFunctionality,
    ModelResource,
    NamedDP,
    NodeFunctionality,
    NodeResource,
    SimpleWrap,
)
from .posets import FinitePoset, Numbers, Poset, PosetProduct
from .primitivedps import (
    AmbientConversion,
    CatalogueDP,
    Constant,
    DPLoop2,
    DPSeries,
    EntryInfo,
    IdentityDP,
    JoinNDP,
    Limit,
    M_Ceil_DP,
    M_FloorFun_DP,
    M_Fun_AddConstant_DP,
    M_Fun_AddMany_DP,
    M_Fun_MultiplyConstant_DP,
    M_Fun_MultiplyMany_DP,
    M_Power_DP,
    M_Res_AddConstant_DP,
    M_Res_AddMany_DP,
    M_Res_DivideConstant_DP,
    M_Res_MultiplyConstant_DP,
    M_Res_MultiplyMany_DP,
    MeetNDualDP,
    Mux,
    ParallelDP,
    PrimitiveDP,
    UnitConversion,
    ValueFromPoset,
)
from .solution_interface import Interval, LowerSet, UpperSet

__all__ = [
    "load_repr1",
    "loader_for",
    "parse_yaml_value",
]

FF = Callable[[dict[str, Any]], object]

loaders: dict[str, FF] = {}


def loader_for(classname: str) -> Callable[[FF], FF]:
    def dc(f: FF) -> FF:
        if classname in loaders:
            msg = f"Already registered loader for {classname!r}"
            raise ValueError(msg)
        loaders[classname] = f
        return f

    return dc


@loader_for("PosetProduct")
def load_PosetProduct(ob: dict[str, Any]) -> PosetProduct[Any]:
    subs: list[Poset[Any]] = []
    for ps in ob["subs"]:
        p: Poset[Any] = load_repr1(ps, Poset)
        subs.append(p)

    return PosetProduct(subs=subs)


def _load_DP_fields(ob: dict[str, Any]) -> dict[str, Any]:
    description = ob["$schema"].get("description", None)
    F: Poset[Any] = load_repr1(ob["F"], Poset)
    R: Poset[Any] = load_repr1(ob["R"], Poset)
    fields = dict(description=description, F=F, R=R)

    if "vu" in ob:
        fields["vu"] = load_repr1(ob["vu"], ValueFromPoset)
    if "c" in ob:
        fields["c"] = load_repr1(ob["c"], ValueFromPoset)
    if "opspace" in ob:
        fields["opspace"] = load_repr1(ob["opspace"], Poset)
    if "common" in ob:
        fields["common"] = load_repr1(ob["common"], Poset)
    if "C" in ob:
        fields["opspace"] = load_repr1(ob["C"], Poset)

    if "coords" in ob:
        fields["coords"] = load_repr1(ob["coords"], Coords)
    if "coords2" in ob:
        fields["coords2"] = load_repr1(ob["coords2"], Coords)
    if "factor" in ob:
        from fractions import Fraction

        fields["factor"] = Fraction(ob["factor"])
    return fields


@loader_for("ValueFromPoset")
def load_ValueFromPoset(ob: dict[str, Any]) -> ValueFromPoset[Any]:
    poset: Poset[Any] = load_repr1(ob["poset"], Poset)
    value = ob["value"]
    value = parse_yaml_value(poset, value)
    return ValueFromPoset(value=value, poset=poset)


@loader_for("CatalogueDP")
def load_CatalogueDP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    entries = fields["entries"] = {}
    for k, v in ob["entries"].items():
        f_max_raw = v["f_max"]
        r_min_raw = v["r_min"]
        F = fields["F"]
        R = fields["R"]
        f_max = parse_yaml_value(F, f_max_raw)
        r_min = parse_yaml_value(R, r_min_raw)
        entries[k] = EntryInfo(f_max=f_max, r_min=r_min)
    return CatalogueDP(**fields)


@loader_for("M_Res_MultiplyConstant_DP")
def load_M_Res_MultiplyConstant_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Res_MultiplyConstant_DP(**fields)


@loader_for("M_Res_DivideConstant_DP")
def load_M_Res_DivideConstant_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Res_DivideConstant_DP(**fields)


@loader_for("IdentityDP")
def load_Identity_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return IdentityDP(**fields)


@loader_for("Mux")
def load_Mux(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    # fields["coords"] = load_repr1(ob["coords"], Coords)
    return Mux(**fields)


@loader_for("DPLoop2")
def load_DPLoop2(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    fields["dp"] = load_repr1(ob["dp1"], PrimitiveDP)
    return DPLoop2(**fields)


@loader_for("M_Fun_MultiplyConstant_DP")
def load_M_Fun_MultiplyConstant_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Fun_MultiplyConstant_DP(**fields)


@loader_for("M_Res_AddConstant_DP")
def load_M_Res_AddConstant_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Res_AddConstant_DP(**fields)


@loader_for("M_Fun_AddMany_DP")
def load_M_Fun_AddMany_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Fun_AddMany_DP(**fields)


@loader_for("M_Res_AddMany_DP")
def load_M_Res_AddMany_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Res_AddMany_DP(**fields)


@loader_for("M_Res_MultiplyMany_DP")
def load_M_Res_MultiplyMany_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return M_Res_MultiplyMany_DP(**fields)


@loader_for("M_Fun_MultiplyMany_DP")
def load_M_Fun_MultiplyMany_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)

    return M_Fun_MultiplyMany_DP(**fields)


@loader_for("M_Power_DP")
def load_M_Power_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)

    return M_Power_DP(**fields, num=ob["num"], den=ob["den"])


@loader_for("M_Ceil_DP")
def load_M_Ceil_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)

    return M_Ceil_DP(**fields)


@loader_for("M_FloorFun_DP")
def load_M_FloorFun_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)

    return M_FloorFun_DP(**fields)


# @loader_for("Conversion")
# def load_Conversion(ob: dict[str, Any]):
#     fields = _load_DP_fields(ob)
#
#     raise NotImplementedError(ob)
#


@loader_for("SeriesN")
def load_SeriesN(ob: dict[str, Any]) -> DPSeries:
    fields = _load_DP_fields(ob)

    subs: list[PrimitiveDP[Any, Any]] = []
    for dps in ob["dps"]:
        dp: PrimitiveDP[Any, Any] = load_repr1(dps, PrimitiveDP)
        subs.append(dp)

    return DPSeries(**fields, subs=subs)


@loader_for("ParallelN")
def load_ParallelN(ob: dict[str, Any]) -> ParallelDP[Any, Any]:
    fields = _load_DP_fields(ob)

    subs: list[PrimitiveDP[Any, Any]] = []
    for dps in ob["dps"]:
        dp: PrimitiveDP[Any, Any] = load_repr1(dps, PrimitiveDP)
        subs.append(dp)

    return ParallelDP(**fields, subs=subs)


#
# @loader_for('M_Ceil_DP')
# def load_M_Ceil_DP(ob: dict[str, Any]):
#     F = load_repr1(ob['F'], Poset)
#     R = load_repr1(ob['R'], Poset)
#
#     return PrimitiveDP(F=F, R=R)


@loader_for("M_Fun_AddConstant_DP")
def load_M_Fun_AddConstant_DP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)

    return M_Fun_AddConstant_DP(**fields)


@loader_for("AmbientConversion")
def load_AmbientConversion(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)

    return AmbientConversion(**fields)


@loader_for("UnitConversion")
def load_UnitConversion(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return UnitConversion(**fields)


@loader_for("JoinNDP")
def load_JoinNDP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return JoinNDP(**fields)


@loader_for("MeetNDualDP")
def load_MeetNDualDP(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return MeetNDualDP(**fields)


@loader_for("Limit")
def load_Limit(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return Limit(**fields)


@loader_for("Constant")
def load_Constant(ob: dict[str, Any]):
    fields = _load_DP_fields(ob)
    return Constant(**fields)


#
# @loader_for('M_Fun_MultiplyConstant_DP')
# def load_M_Fun_MultiplyConstant_DP(ob: dict[str, Any]):
#     F = load_repr1(ob['F'], Poset)
#     R = load_repr1(ob['R'], Poset)
#
#     return PrimitiveDP(F=F, R=R)


@loader_for("CompositeNamedDP")
def load_CompositeNamedDP(ob: dict[str, Any]):
    functionalities_s = ob["functionalities"]
    resources_s = ob["resources"]

    functionalities: dict[str, Any] = {k: load_repr1(v, Poset) for k, v in functionalities_s.items()}
    resources: dict[str, Any] = {k: load_repr1(v, Poset) for k, v in resources_s.items()}
    loaded_nodes = {}
    nodes = ob["nodes"]
    for k, v in nodes.items():
        node: NamedDP[Any, Any] = load_repr1(v, NamedDP)
        loaded_nodes[k] = node
    connections: list[Connection] = []

    for c in ob["connections"]:
        source = c["from"]
        target = c["to"]
        if "node" in source:
            source = NodeResource(source["node"], source["node_resource"])
        else:
            source = ModelFunctionality(source["functionality"])

        if "node" in target:
            target = NodeFunctionality(target["node"], target["node_functionality"])
        else:
            target = ModelResource(target["resource"])

        connections.append(Connection(source=source, target=target))

    return CompositeNamedDP(
        functionalities=functionalities, resources=resources, nodes=loaded_nodes, connections=connections
    )


@loader_for("SimpleWrap")
def load_SimpleWrap(ob: dict[str, Any]) -> SimpleWrap[object, object]:
    functionalities = {}
    for k, v in ob["functionalities"].items():
        functionalities[k] = load_repr1(v, Poset)
    resources = {}
    for k, v in ob["resources"].items():
        resources[k] = load_repr1(v, Poset)
    dp: PrimitiveDP[Any, Any] = load_repr1(ob["dp"], PrimitiveDP)
    return SimpleWrap(functionalities=functionalities, resources=resources, dp=dp)


@loader_for("FinitePoset")
def load_FinitePoset(ob: dict[str, Any]) -> FinitePoset:
    elements = ob["elements"]
    relations = ob["relations"]
    # TODO: validation of relations
    relations: set[tuple[str, str]] = set(tuple(x) for x in relations)  # type: ignore
    elements: set[str] = set(elements)
    return FinitePoset(elements=elements, relations=relations)


@loader_for("Interval")
def load_Interval(ob: dict[str, Any]) -> Interval[Any]:
    pessimistic = load_repr1(ob["pessimistic"], object)
    optimistic = load_repr1(ob["optimistic"], object)
    return Interval(pessimistic=pessimistic, optimistic=optimistic)


@loader_for("LowerSet")
def load_LowerSet(ob: dict[str, Any]):
    maximals = ob["maximals"]
    return LowerSet(maximals=maximals)


@loader_for("UpperSet")
def load_UpperSet(ob: dict[str, Any]):
    minimals = ob["minimals"]
    return UpperSet(minimals=minimals)


@loader_for("Numbers")
def load_Numbers(ob: dict[str, Any]):
    bottom = Decimal(ob["bottom"])
    top = Decimal(ob["top"])
    units = ob.get("units", "")
    step = Decimal(ob.get("step", 0))
    return Numbers(bottom=bottom, top=top, step=step, units=units)


# write the implementation for `loader_for` that allows to  register
# a function for a given class name

X = TypeVar("X")


def load_repr1(data: dict[str, Any], T: Optional[Type[X]] = None) -> X:
    if "$schema" not in data:
        raise ValueError("Missing $schema")
    schema = data["$schema"]
    title = schema.get("title", None)
    if title not in loaders:
        msg = f"Cannot find loader for {title!r}: known are {list(loaders)}"
        raise ValueError(msg)
    loader = loaders[title]
    try:
        res = loader(data)

        if T is not None:
            if not isinstance(res, T):
                msg = f"Expected {T!r}, got {type(res)!r}"
                raise ValueError(msg)

        return cast(X, res)
    except Exception as e:
        datas = yaml.dump(data, allow_unicode=True)
        logger.exception("Error while loading %r\n%s", title, datas, exc_info=e)
        msg = f"Error while loading {title!r}:"
        raise ValueError(msg) from e


@loader_for("ComposeList")
def load_ComposeList(ob: dict[str, Any]) -> ComposeList:
    res: list[Coords] = []
    for c in ob["components"]:
        r = load_repr1(c, Coords)
        res.append(r)

    return ComposeList(components=tuple(res))


@loader_for("CoordsComp")
def load_CoordsComp(ob: dict[str, Any]) -> CoordsComp:
    index = ob["index"]
    ntot = ob["ntot"]
    rest = ob["rest"]
    rest = load_repr1(rest, Coords)
    return CoordsComp(index=index, ntot=ntot, rest=rest)


@loader_for("CoordsIdentity")
def load_CoordsIdentity(ob: dict[str, Any]) -> CoordsIdentity:
    return CoordsIdentity()


def parse_yaml_value(poset: Poset[X], ob: object) -> X:
    match poset:
        case Numbers():
            if not isinstance(ob, (int, str, float, bool)):
                msg = "For Poset of numbers, expected string or int, got %s.\b%s" % (type(ob), repr(ob))
                raise ValueError(msg)
            return Decimal(ob)  # type: ignore
        case FinitePoset():
            if not isinstance(ob, str):
                msg = "For FinitePoset, expected string, got %s.\b%s" % (type(ob), repr(ob))
                raise ValueError(msg)
            return ob  # type: ignore
        case PosetProduct() as PP:
            subs: list[Poset[Any]] = PP.subs
            if not isinstance(ob, list):
                msg = "Expected list, got %s" % type(ob)
                raise ValueError(msg)
            obl = cast(list[Any], ob)
            val: list[Any] = []
            for el, sub in zip(obl, subs):  # type: ignore
                sub = cast(Poset[Any], sub)
                el = parse_yaml_value(sub, el)
                val.append(el)
            return tuple(val)  # type: ignore
        case _:
            raise NotImplementedError(type(poset))
