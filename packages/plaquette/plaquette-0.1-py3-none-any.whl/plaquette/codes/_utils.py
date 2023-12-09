"""Utility functions to work with Plaquette codes."""
import typing as t

from plaquette import pauli
from plaquette.pauli import Tableau


def _generate_factorized_checks(
    checks: t.Sequence[Tableau], meas_ops: t.Sequence[Tableau]
) -> list[list[int]]:
    """Generate the factorized checks for the measurement operators.

    Args:
        checks: The checks of the quantum code.
        meas_ops: The measured operators to implement the code.

    Returns:
        The nested list of integers with each inner list containing indices of meas_ops.
        Each inner list maps to corresponding check of the same index.
    """
    factorized_checks: list[list[int]] = [list() for _ in range(len(checks))]

    checks_dict = [pauli.pauli_to_dict(t.cast(Tableau, op)) for op in checks]

    gauges = [pauli.pauli_to_dict(t.cast(Tableau, op)) for op in meas_ops]

    # list to keep track of matched gauge op
    matched_gauges: list[int] = []

    for s, stab in enumerate(checks_dict):
        to_match = set(stab.items())
        factors: list[int] = []  # list of factors for a given stabiliser.
        for g, gauge in enumerate(gauges):
            if set(gauge.items()).issubset(to_match):
                factors.append(g)
                to_match.difference_update(gauge.items())
                if len(to_match) == 0:
                    break

        matched_gauges.extend(factors)
        factorized_checks[s] = factors

    return factorized_checks
