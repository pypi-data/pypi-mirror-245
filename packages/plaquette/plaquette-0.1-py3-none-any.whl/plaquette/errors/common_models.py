# Copyright 2023, QC Design GmbH and the plaquette contributors
# SPDX-License-Identifier: Apache-2.0
"""Common Error Models used."""
from plaquette.codes import Code
from plaquette.errors import ErrorData
from plaquette.frontend import (
    GateErrorsConfig,
    QubitErrorsConfig,
    _GateErrorMetadata,
    _QubitErrorMetadata,
)


def generate_standard_circuit_noise(code: Code, p: float) -> ErrorData:
    """Generate the standard depolarizing circuit noise model.

    Args:
        code: The :class:`.Code` object to define errors for.
        p: The probability of the error model.

    Returns:
        An `ErrorData` object for the standard depolarizing noise model.
    """
    qubit_error_conf = QubitErrorsConfig(
        sample=True,
        X=_QubitErrorMetadata(distribution="constant", params=[p / 3], enabled=True),
        Y=_QubitErrorMetadata(distribution="constant", params=[p / 3], enabled=True),
        Z=_QubitErrorMetadata(distribution="constant", params=[p / 3], enabled=True),
        measurement=_QubitErrorMetadata(
            distribution="constant", params=[p], enabled=True
        ),
    ).simulated_errors
    gate_error_conf = GateErrorsConfig(
        sample=True,
        load_file=False,
        CX=_GateErrorMetadata(
            distribution=["constant"] * 15,
            induced_errors=[a + b for a in "IXYZ" for b in "IXYZ"][1:],
            params=[[p / 15]] * 15,
            enabled=True,
        ),
        CZ=_GateErrorMetadata(
            distribution=["constant"] * 15,
            induced_errors=[a + b for a in "IXYZ" for b in "IXYZ"][1:],
            params=[[p / 15]] * 15,
            enabled=True,
        ),
        H=_GateErrorMetadata(
            distribution=["constant"] * 15,
            induced_errors=[a for a in "XYZ"],
            params=[[p / 3]] * 3,
            enabled=True,
        ),
        R=_GateErrorMetadata(
            distribution=["constant"] * 15,
            induced_errors=[a for a in "XYZ"],
            params=[[p / 3]] * 3,
            enabled=True,
        ),
    ).simulated_errors
    return ErrorData.from_lattice(code, qubit_error_conf, gate_error_conf)


def generate_depolarizing_noise(code: Code, p: float, meas: bool = False) -> ErrorData:
    """Generate depolarizing noise model on qubits, possibly with measurement errors.

    Args:
        code: The :class:`.Code` on which to apply the errors.
        p: The error probability.
        meas: bool determining whether to include measurement errors.

    Returns:
        A `ErrorData` corresponding to the depolarizing noise model.
    """
    qubit_error_conf = QubitErrorsConfig(
        sample=True,
        X=_QubitErrorMetadata(distribution="constant", params=[p / 3], enabled=True),
        Y=_QubitErrorMetadata(distribution="constant", params=[p / 3], enabled=True),
        Z=_QubitErrorMetadata(distribution="constant", params=[p / 3], enabled=True),
        measurement=_QubitErrorMetadata(
            distribution="constant", params=[p], enabled=meas
        ),
    ).simulated_errors

    return ErrorData.from_lattice(code, qubit_error_conf, None)
