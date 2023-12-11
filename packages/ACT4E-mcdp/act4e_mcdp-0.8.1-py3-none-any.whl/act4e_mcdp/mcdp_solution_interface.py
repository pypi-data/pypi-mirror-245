from abc import ABC, abstractmethod
from typing import Any, Mapping, TypeVar

from .nameddps import NamedDP
from .posets import Interval, LowerSet, UpperSet

__all__ = [
    "MCDPSolverInterface",
]

FT = TypeVar("FT")
RT = TypeVar("RT")


class MCDPSolverInterface(ABC):
    """An abstract class that describes the interface of a solver for NamedDPs."""

    @abstractmethod
    def solve_mcdp_FixFunMinRes(
        self,
        graph: NamedDP[FT, RT],
        functionality_needed: Mapping[str, FT],
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[UpperSet[Mapping[str, RT]]]:
        """

        Solves the problem of finding the minimal resources needed to satisfy a given functional requirement.

        The problem is defined by a model and a query. The model is a NamedDP, and the query is a mapping from
        the names of the resources to the values of the resources.

        The solution is a finitely-supported upper set.


        For example, this is what we expect from a solver for the empty model:

        ```python

            solver: SolverInterface = ...

            empty = CompositeNamedDP(functionalities={}, resources={}, nodes={}, connections=[])

            result: UpperSet = solver.solve_FixFunMinRes(empty, {})

            # We expect that the result is a list containing the empty dictionary

            assert list(result.minima) == [{}]

        ```

        In a more complex example, we can have a model describing the identity:

        ```python

            solver: SolverInterface = ...

            P = FinitePoset({'a', 'b'}, {('a', 'b')})

            identity = CompositeNamedDP(
                functionalities={'f1': P},
                resources={'r1': P},
                nodes={},
                connections=[
                    Connection(
                        source=ModelFunctionality('f1'),
                        target=ModelResource('r1')
                    )]
            )

            result: UpperSet = solver.solve_FixFunMinRes(identity, {'f1': 'a'})

            # We expect that the result is a list containing only one element

            assert list(result.minima) == [{'r1': 'a'}]
        ```


        Parameters:
            graph: The model of the problem.
            functionality_needed: The functionality needed (key-value dictionary).
            resolution_optimistic: An integer returning the resolution of the optimistic answer,
                to be used in the case of DPs that are not computable.
            resolution_pessimistic: Same thing, for the pessimistic answer.

        Returns:

            An interval of upper sets.

        """
        raise NotImplementedError

    @abstractmethod
    def solve_mcdp_FixResMaxFun(
        self,
        graph: NamedDP[FT, RT],
        resources_budget: Mapping[str, FT],
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[LowerSet[Mapping[str, RT]]]:
        """
        This is the dual of solve_FixFunMinRes. It solves the problem of finding the maximal functionality
        that can be provided with a given budget of resources.


        For example, this is what we expect from a solver for the empty model:

        ```python

            solver: SolverInterface = ...

            empty = CompositeNamedDP(functionalities={}, resources={}, nodes={}, connections=[])

            result: LowerSet = solver.solve_FixResMaxFun(empty, {})

            # We expect that the result is a list containing the empty dictionary

            assert list(result.maxima) == [{}]

        ```

        Parameters:
            graph: The model of the problem.
            resources_budget: The maximum budget that we have (key-value dictionary).
            resolution_optimistic: An integer returning the resolution of the optimistic answer,
                to be used in the case of DPs that are not computable.
            resolution_pessimistic: Same thing, for the pessimistic answer.

        Returns:

             An interval of lower sets.


        """
        raise NotImplementedError
