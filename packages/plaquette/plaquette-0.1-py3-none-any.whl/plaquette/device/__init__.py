# Copyright 2023, QC Design GmbH and the plaquette contributors
# SPDX-License-Identifier: Apache-2.0
"""Quantum devices and error correction simulators.

This module provides tools for connecting to quantum devices and simulating
quantum error correction using suitable Clifford circuits. A circuit from
:mod:`plaquette.circuit` can be simulated as follows:

>>> from plaquette import codes
>>> from plaquette.circuit.generator import generate_qec_circuit
>>> from plaquette import Device
>>> circ = generate_qec_circuit(codes.Code.make_rotated_planar(5), {}, {}, "X")
>>> dev = Device("clifford")
>>> dev  # doctest: +ELLIPSIS
<plaquette.device.Device object at ...>

In addition to the built-in pure-Python circuit simulator backend, the faster
Stim simulator can be used by specifying ``"stim"`` as the backend:

>>> dev = Device("stim")
>>> dev.run(circ)
>>> raw, erasure = dev.get_sample()

``raw`` contains all the measurement results from measurement gates in the
circuit, while ``erasure`` contains information on erased qubits if
the :ref:`Gate E_ERASE` was used. The circuit returns measurement results as a
linear array and the function
:meth:`.MeasurementSample.from_code_and_raw_results` can be used to split this
array into different parts (this assumes that the circuit was generated using
:mod:`plaquette.circuit`).
"""

import abc
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pkg_resources

from plaquette import circuit as plaq_circuit
from plaquette import codes


@dataclass
class MeasurementSample:
    """One sample from a simulator.

    .. automethod:: __init__
    """

    logical_op_initial: np.ndarray
    """Measurement results for logical operators before QEC.

    Array with one entry for each logical operator (0 or 1).
    """
    logical_op_final: np.ndarray
    """Measurement results for logical operators after QEC.
    Array with one entry for each logical operator (0 or 1).
    """
    logical_op_toggle: np.ndarray
    """XOR between logical operator values before and after QEC.

    Array with one entry for each logical operator (0 or 1).
    """
    stabilizer_gen: np.ndarray
    """Measurement results for stabilizer generators.

    The shape is ``(n_rounds + 1, n_stabgens)``. The ``+1`` is necessary because it
    always includes one round of "initial" stabilizer measurements to prepare the
    initial state.
    """
    syndrome: np.ndarray
    """Syndrome data (derived from measurement results for stabilizer generators).

    The shape is ``(n_rounds, n_stabgens)``. It is obtained from ``stabilizer_gen``
    by taking the XOR of consecutive rounds.
    """
    erased_qubits: Optional[np.ndarray]
    """Erasure information

    The shape is ``(n_rounds, n_qubits)`` (only data qubits, no ancilla qubits).
    Each entry is a boolean and specifies whether the given qubit was erased in the
    given round.
    """

    @classmethod
    def from_code_and_raw_results(
        cls,
        code: codes.Code,
        logical_ops: str,
        raw_results: np.ndarray,
        erasure: Optional[np.ndarray] = None,
        n_rounds: int = 1,
    ):
        """Unpack the results from a simulator into a more convenient format.

        Args:
            code: the :class:`.Code` used to generate the circuit which
                produced the results you want to unpack.
            logical_ops: The measured logical operators of the code.
            n_rounds: number of measurement rounds that produced these results.
            raw_results: the measurement results from
                :meth:`AbstractSimulator.get_sample`.
            erasure: erasure information from
                :meth:`AbstractSimulator.get_sample`.
        """
        logop_idxs = [
            i + code.num_logical_qubits if op == "Z" else i
            for i, op in enumerate(logical_ops)
        ]
        logop_wts = [code.distances[j] for j in logop_idxs]
        logical_op_initial = np.array(
            [
                np.sum(raw_results[i * logop_wts[i] : (i + 1) * logop_wts[i]]) % 2
                for i in range(len(logical_ops))
            ],
            dtype=int,
        )
        # fmt: off
        logical_op_final = np.array(
            [
                np.sum(
                    raw_results[len(raw_results) - (i * logop_wts[i])
                        - logop_wts[i] : len(raw_results) - (i * logop_wts[i])]  # noqa
                ) % 2 for i in range(len(logical_ops))
            ][::-1], dtype=int,
        )
        ancillas = np.array(
            raw_results[np.sum(logop_wts):-np.sum(logop_wts)] # noqa
        )
        # fmt: on

        logical_toggle = logical_op_initial ^ logical_op_final
        meas_op_outcomes = ancillas.reshape(
            (n_rounds + 1, len(code.measured_operators))
        )
        stab = np.zeros((n_rounds + 1, code.num_stabilizers), dtype=bool)
        for i, rd in enumerate(meas_op_outcomes):
            for j, chk_idxs in enumerate(code.factorized_checks):
                stab[i][j] = np.logical_xor.reduce(rd[chk_idxs])

        syndrome = (stab[1:] ^ stab[:-1]).ravel()

        if erasure is not None:
            if erasure.shape != (n_rounds * code.num_data_qubits,):
                raise ValueError("Wrong number of erasure information pieces")

        return MeasurementSample(
            logical_op_initial=logical_op_initial,
            logical_op_final=logical_op_final,
            logical_op_toggle=logical_toggle,
            stabilizer_gen=stab,
            syndrome=syndrome,
            erased_qubits=erasure,
        )


local_simulators = {"clifford", "stim", "tableau"}


# The recognized quantum devices.
# Note that these are loaded once when the module has been loaded.
recognized_devices = {
    entry.name: entry for entry in pkg_resources.iter_entry_points("plaquette.device")
}


class Device:
    """Quantum device for accessing simulators or real quantum hardware.

    .. automethod:: __init__
    """

    def __init__(self, backend: str, *args, **kwargs):
        """Create a new quantum device.

        There are two built-in backends: ``"clifford"`` (simulator based on Clifford
        circuits) and ``"stim"`` (simulator using Stim as backend).

        Further devices may be provided as plugins to plaquette. Note that such
        plugins may have to be installed separately to plaquette and that a new
        Python session may have to be started to have such devices be
        recognized after installation.

        Args:
            backend: The name of the backend to use.
            args: Arguments that the backend takes.
            kwargs: Keyword arguments that the backend takes.

        Notes:
            Arguments and keyword arguments meant for the simulator are not
            checked on device creation. Running a circuit will fail if there
            are incorrect arguments passed. See the docs of the backend
            you plan on using for a list of accepted arguments and
            keyword arguments.
        """
        if backend not in recognized_devices:
            raise ValueError(f"Specified backend {backend} is not recognized.")

        self._args, self._kwargs = args, kwargs
        self._backend_name = backend
        self._backend_class = recognized_devices[backend].load()
        self._backend = self._backend_class(*self._args, **self._kwargs)

        self._circuit = None

    @property
    def circuit(self):
        """The underlying quantum circuit to simulate using the backend."""
        return self._backend.circ

    @circuit.setter
    def circuit(self, circuit):
        """Set the underlying quantum circuit to simulate using the backend."""
        self._backend.circ = circuit

    def __iter__(self):
        """Iterate through instructions one-by-one.

        The underlying backend has to define the ``__iter__`` method.
        """
        return self._backend.__iter__()

    def __next__(self):
        """Step to the next gate/instruction in the circuit sequence.

        The underlying backend has to define the ``__next__`` method.
        """
        return self._backend.__next__()

    @property
    def state(self):
        """The underlying quantum state of the backend, if available.

        The underlying backend has to define the ``state`` property.
        """
        return self._backend.state

    @property
    def n_qubits(self):
        """Number of qubits that underlying backend handles.

        The underlying backend has to define the ``n_qubits`` property.
        """
        return self._backend.n_qubits

    def reset_backend(self, *args, **kwargs):
        """Reset the underlying backend."""
        return self._backend.reset(*args, **kwargs)

    def run(
        self,
        circuit: plaq_circuit.Circuit | plaq_circuit.CircuitBuilder,
        *,
        shots=1,
        **kwargs,
    ):
        """Run the given circuit.

        Args:
            circuit: The circuit (or the builder containing it) to be simulated.

        Keyword Args:
            shots: for remote backends, the number of shots to execute the
                circuit with.
            kwargs: backend-specific keyword arguments. For the Clifford
                simulator, the ``after_reset`` keyword argument may be set. If
                ``False``, the returned measurement and erasures will still contain
                any data from previous runs.  Otherwise, both these results and the
                internal state will be reset.
        """
        return self._backend.run(circuit, shots=shots, **kwargs)

    def get_sample(self) -> tuple[np.ndarray, np.ndarray]:
        """Return the samples **after a circuit run**.

        Notes:
            This method returns the sample from the last run. Calling
            this method many times after only running the circuit once
            will return always the same sample related to that single
            circuit run. If you want a new sample, you need to also
            call :meth:`run` before this method.
        """
        return self._backend.get_sample()

    @property
    def is_completed(self) -> Optional[list[bool]]:
        """Returns whether the jobs submitted by the device have been completed.

        Notes:
            This method simply returns None for simulators.
        """
        if self._backend_name in local_simulators:
            return None
        return self._backend.is_completed


class AbstractSimulator(metaclass=abc.ABCMeta):
    """Simulator base class.

    .. automethod:: __init__
    """

    @abc.abstractmethod
    def reset(self):
        """Reset this simulator to its default state.

        The simulator will discard all data that it stored which came from
        circuit runs, if any, and will reset any internal state it has to its
        appropriate "zero" state.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def run(
        self,
        circuit: plaq_circuit.Circuit | plaq_circuit.CircuitBuilder,
        *,
        shots=1,
        **kwargs,
    ):
        """Run the given circuit.

        Args:
            circuit: The Clifford circuit (or the builder containing it) to be
                simulated.

        Keyword Args:
            shots: for remote backends, the number of shots to execute the
                circuit with.
            kwargs: backend-specific keyword arguments. For the Clifford
                simulator, the ``after_reset`` keyword argument may be set. If
                ``False``, the returned measurement and erasures will still contain
                any data from previous runs.  Otherwise, both these results and the
                internal state will be reset.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_sample(self) -> tuple[np.ndarray, np.ndarray]:
        """Return the samples **after a circuit run**.

        Returns:
            a tuple whose first item is an array of measurement outcomes and
            whose second item is the erasure information.

        Notes:
            The **measurements** item in the returned tuple is a one-dimensional array
            which contains the following entries, in sequence:

            * ``n_logical_qubits`` results from logical operator measurements for state
              preparation.
            * ``(n_rounds + 1) * n_stabgens`` results from stabilizer generator
              measurements:

              * ``n_stabgens`` results from initial stabilizer generator measurements
                for state preparation.
              * ``n_rounds * n_stabgens`` results from stabilizer generator
                measurements.
            * ``n_logical_qubits`` results from logical operator measurements for state
              verification.

            Here, ``n_logical_qubits`` is the number of logical qubits, ``n_stabgens``
            is the number of stabilizer generators and ``n_rounds`` is the number of
            rounds of stabilizer measurements.

            The described sequence of measurements is implemented in the circuit
            generator in :meth:`~.QECCircuitGenerator.get_circuit`.

            The **erasure** array specifies, for each data qubit and each round of
            measurements, whether it was erased or not. The shape of this array is
            ``[n_rounds * n_qubits]``.

            To unpack these arrays, you can use
            :meth:`~plaquette.device.MeasurementSample.from_code_and_raw_results`.

            .. todo::
                We need to come up with a way to remove this additional step.
                In theory, a simulator class should immediately return a
                :class:`.MeasurementSample`, and not require this class method.
        """
        raise NotImplementedError()
