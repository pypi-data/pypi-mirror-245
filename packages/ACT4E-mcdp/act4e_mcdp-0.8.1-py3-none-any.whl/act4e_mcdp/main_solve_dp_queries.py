import argparse
import glob
import os
import sys
import traceback
from typing import Any, Literal, Optional, cast

import yaml

from . import logger
from .loading import load_repr1, parse_yaml_value
from .primitivedps import PrimitiveDP
from .solution_interface import (
    DPSolverInterface,
    FixFunMinResQuery,
    FixResMaxFunQuery,
    FunctionNotImplemented,
    Interval,
    LowerSet,
    UpperSet,
)
from .utils import import_from_string, rich_format

__all__ = [
    "solve_dp_queries_main",
]


def solve_dp_queries_main() -> None:
    parser = argparse.ArgumentParser()
    # parser.add_argument("-d", "--queries-dir", help="Where the queries are", required=False)
    # parser.add_argument("-f", "--files", help="Individual tests", required=False)
    parser.add_argument("-o", "--output", help="Output summary", default="output_summary.yaml")
    parser.add_argument("--solver", help="Model source (file or URL)", required=True)
    parser.add_argument("-q", "--quiet", action="store_true", help="Only print errors")

    args, extra = parser.parse_known_args()

    try:
        solver0 = import_from_string(args.solver)
    except Exception as e:
        logger.error("Could not import solver %r", args.solver, exc_info=e)
        sys.exit(1)

    solver: DPSolverInterface

    if isinstance(solver0, DPSolverInterface):
        solver = solver0
    else:
        # noinspection PyCallingNonCallable
        solver = solver0()  # type: ignore
    if not isinstance(solver, DPSolverInterface):
        msg = f"Expected a DPSolverInterface, got {solver!r}"
        raise ValueError(msg)

    all_output = {}

    summary: dict[str, list[str]] = {
        "failed": [],
        "succeeded": [],
        "comparison_not_implemented": [],
        "not_implemented": [],
        "exception": [],
    }

    exception: str
    tb: str
    not_implemented_messages: set[str] = set()

    if not extra:
        logger.error("Need to specify some filenames or directories ")
        sys.exit(1)

    filenames: list[str] = []

    for x in extra:
        if not os.path.exists(x):
            logger.error("File or directory %r does not exist", x)
            sys.exit(1)

        if os.path.isdir(x):
            pattern = "*.dp-queries.*.mcdpr1.yaml"
            inside = list(glob.glob(x + f"/**/{pattern}", recursive=True))
            if not inside:
                logger.error("No files with pattern %r found in directory %r", pattern, x)
                sys.exit(1)
            filenames.extend(inside)
        elif os.path.isfile(x):
            filenames.append(x)
        else:
            logger.warn("Ignoring %r", x)

    for fn in sorted(set(filenames)):
        data = yaml.load(open(fn).read(), Loader=yaml.SafeLoader)
        filename_rel = cast(str, data["dp"])
        dp_filename = os.path.join(os.path.dirname(fn), filename_rel)
        if not os.path.exists(dp_filename):
            logger.error("File %r does not exist", dp_filename)
            sys.exit(1)
        with open(dp_filename) as f:
            data_dp = yaml.load(f.read(), Loader=yaml.SafeLoader)
        model: PrimitiveDP[Any, Any] = load_repr1(data_dp, PrimitiveDP)

        # logger.info(f"query: {fn} {data} {model}")
        query = data["query"]
        approximated = data["approximated"]
        result: Interval[UpperSet[Any]] | Interval[LowerSet[Any]]

        if query == "FixFunMinRes":
            data_parsed = parse_yaml_value(model.F, data["value"])
            result0: Interval[UpperSet[Any]] = load_repr1(data["result"], Interval)
            result0.pessimistic.minimals = [
                parse_yaml_value(model.R, x) for x in result0.pessimistic.minimals
            ]
            result0.optimistic.minimals = [parse_yaml_value(model.R, x) for x in result0.optimistic.minimals]

            result = result0
            query_data = FixFunMinResQuery(
                functionality=data_parsed, resolution_pessimistic=0, resolution_optimistic=0
            )

            f: Any = solver.solve_dp_FixFunMinRes

        elif query == "FixResMaxFun":
            data_parsed = parse_yaml_value(model.R, data["value"])

            result1: Interval[LowerSet[Any]] = load_repr1(data["result"], Interval)

            result1.pessimistic.maximals = [
                parse_yaml_value(model.F, x) for x in result1.pessimistic.maximals
            ]
            result1.optimistic.maximals = [parse_yaml_value(model.F, x) for x in result1.optimistic.maximals]

            result = result1
            query_data = FixResMaxFunQuery(
                resources=data_parsed, resolution_pessimistic=0, resolution_optimistic=0
            )

            f: Any = solver.solve_dp_FixResMaxFun

        else:
            logger.error("Unknown query %r", query)
            sys.exit(1)

        try:
            solution = f(model, query_data)
            exception = ""
            tb = ""
        except (FunctionNotImplemented, NotImplementedError) as e:
            status = "not_implemented"
            solution = None
            tb = traceback.format_exc()
            exception = str(e)
            not_implemented_messages.add(exception)

        except Exception as e:
            status = "exception"
            solution = None
            exception = str(e)
            tb = traceback.format_exc()
        else:
            atol = 0.0001
            rtol = 0.00001

            if approximated:
                status = "comparison_not_implemented"
            else:
                if query == "FixFunMinRes":
                    P = model.R
                    logger.info("query: %s , solution: %s", query, solution)
                    result = cast(Interval[UpperSet[Any]], result)
                    solution = cast(Interval[UpperSet[Any]], solution)

                    ok1 = UpperSet.close(P, solution.pessimistic, result.pessimistic, atol=atol, rtol=rtol)
                    ok2 = UpperSet.close(P, solution.optimistic, result.optimistic, atol=atol, rtol=rtol)
                    ok = ok1 and ok2
                elif query == "FixResMaxFun":
                    P = model.F
                    result = cast(Interval[LowerSet[Any]], result)
                    solution = cast(Interval[LowerSet[Any]], solution)
                    ok1 = LowerSet.close(P, solution.pessimistic, result.pessimistic, atol=atol, rtol=rtol)
                    ok2 = LowerSet.close(P, solution.optimistic, result.optimistic, atol=atol, rtol=rtol)
                    ok = ok1 and ok2
                    logger.info("ok1: %s", ok1)
                else:
                    assert False, query

                if ok:
                    status = "succeeded"
                else:
                    status = "failed"

                    exception = f"Expected:\n\n {rich_format(result)}\n\nobtained\n\n {rich_format(solution)}"

        info_struct = {
            "testcase": fn,
            "dp": remove_escapes(rich_format(model)),
            "query": query,
            "value": repr(data_parsed),
            "result_expected": repr(result),
            "result_obtained": repr(solution),
            "status": status,
            "exception": exception,
            "traceback": tb,
        }

        summary[status].append(fn)

        all_output[fn] = info_struct
        postfix = fn + " - " + type(model).__name__ + " - " + query

        log_type: Literal["info", "error", "warning"]
        extra = ""
        if status == "failed":
            log_type = "error"
            model_desc = rich_format(model, max_width=100)
            extra = (
                "\nModel:\n\n" + model_desc + "\n\nQuery:\n\n" + rich_format(query_data) + "\n\n" + exception
            )
        elif status == "exception":
            # if 'NotImplementedError' in exception:
            #     msg = 'NOT IMPLEMENTED: ' + postfix
            #     logger.warn(msg)
            # else:
            log_type = "error"
            extra = tb
        elif status == "not_implemented":
            log_type = "warning"
            # extra = exception
        elif status == "comparison_not_implemented":
            log_type = "warning"
        else:
            msg = "OK:              " + postfix
            logger.info(msg)
            log_type = "info"

        msg = status.upper().rjust(14) + ": " + postfix + "\n" + extra
        msg = msg.strip()

        if not args.quiet or log_type == "error":
            if log_type == "info":
                logger.info(msg)
            elif log_type == "warning":
                logger.warn(msg)
            elif log_type == "error":
                logger.error(msg)

        # logger.info(yaml.dump(info_struct))

    fn_out = args.output
    dn = os.path.dirname(fn_out)
    if dn:
        os.makedirs(dn, exist_ok=True)

    from . import __version__

    output = {"metadata": {"ACT4E-mcdp-version": __version__}, "queries": all_output, "summary": summary}
    with open(fn_out, "w") as f:
        f.write(yaml.dump(output, allow_unicode=True, default_flow_style=False))

    # logger.info("Summary:\n" + yaml.dump(summary, allow_unicode=True, default_flow_style=False))

    logger.info("Find the entire output at %r", fn_out)

    num_ok = len(summary["succeeded"])
    num_failed = len(summary["failed"])
    num_exceptions = len(summary["exception"])
    num_not_implemented = len(summary["not_implemented"])

    logger.info("OK: %d", num_ok)
    if num_failed:
        logger.error("FAILED: %d", num_failed)
    if num_exceptions:
        logger.error("EXCEPTION (includes NotImplemented): %d", num_exceptions)

    if num_not_implemented:
        logger.error("NOT IMPLEMENTED: %d", num_not_implemented)
        m = "".join(f"{x}\n" for x in sorted(not_implemented_messages))
        logger.error(m)

    total_failed = num_failed + num_exceptions + num_not_implemented

    methods = get_all_methods(solver)
    fixfunminres_defined = set([x for x in methods if x.startswith("solve_dp_FixFunMinRes_")])
    fixresmaxfun_defined = set([x for x in methods if x.startswith("solve_dp_FixResMaxFun_")])
    fixfunminres_used = DPSolverInterface.fixfunminres_used
    fixresmaxfun_used = DPSolverInterface.fixresmaxfun_used
    fixfunminres_not_used = fixfunminres_defined - fixfunminres_used
    fixresmaxfun_not_used = fixresmaxfun_defined - fixresmaxfun_used
    fixfunminres_not_defined = fixfunminres_used - fixfunminres_defined
    fixresmaxfun_not_defined = fixresmaxfun_used - fixresmaxfun_defined
    assert not fixfunminres_not_defined
    assert not fixresmaxfun_not_defined
    logger.info("FixFunMinRes used:\n" + "".join(f"- {_}\n" for _ in sorted(fixfunminres_used)))

    logger.info("FixFunMinRes not used:\n" + "".join(f"- {_}\n" for _ in sorted(fixfunminres_not_used)))
    # logger.info("FixFunMinRes used but not defined:\n" + "".join(f'- {_}\n' for _ in sorted(fixfunminres_not_defined)))

    logger.info("FixResMaxFun not used:\n" + "".join(f"- {_}\n" for _ in sorted(fixresmaxfun_not_used)))
    logger.info("FixResMaxFun used:\n" + "".join(f"- {_}\n" for _ in sorted(fixresmaxfun_used)))
    #
    # logger.info("FixResMaxFun used but not defined:\n" + "".join(f'- {_}\n' for _ in sorted(fixresmaxfun_not_defined)))

    sys.exit(total_failed)


def get_all_methods(obj: Any) -> set[str]:
    methods: set[str] = set()
    # Iterate over all superclasses
    for superclass in obj.__class__.__mro__:
        # Exclude the base 'object' class to avoid default Python methods
        if superclass is not object:
            methods.update(method for method in dir(superclass) if callable(getattr(superclass, method)))

    return methods


import re

escape = re.compile(r"\x1b\[[\d;]*?m")
escape1 = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")


def remove_escapes(s: str) -> str:
    # check_isinstance(s, str)
    if s.isprintable():
        return s
    for es in [escape, escape1]:
        s = es.sub("", s)
    return s
