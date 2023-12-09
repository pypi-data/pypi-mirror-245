# Copyright 2023, QC Design GmbH and the plaquette contributors
# SPDX-License-Identifier: Apache-2.0
"""Quantum error-correcting codes."""

import typing as t
from dataclasses import dataclass, field
from enum import IntEnum
from functools import cached_property
from pprint import pformat

import numpy as np
import numpy.typing as npt
import rustworkx as rx

from plaquette import graph, pauli
from plaquette.codes._utils import _generate_factorized_checks
from plaquette.pauli import Tableau, argsort_operators_ref


def generate_layout_coordinates(
    nodes: list[int], edges: list[tuple[int, int]]
) -> dict[int, graph.Position]:
    """Generate the layout coordinates for the Tanner and orchestration graphs.

    Args:
        nodes: The list of node indices.
        edges: The list of edge tuples of the graph.

    Returns:
        A dictionary of node positions with node indices as keys.
    """
    g = rx.PyGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from_no_data(edges)
    layout = rx.spring_layout(g)

    # Convert the layout to a dictionary format
    coordinates = {}
    for idx, node in enumerate(nodes):
        coord = layout[idx]
        z_coord = 0.0 if len(coord) == 2 else coord[2]
        coordinates[node] = graph.Position(x=coord[0], y=coord[1], z=z_coord)

    return coordinates


class QubitType(IntEnum):
    """Type, or role, of a particular qubit."""

    data = 0
    stabilizer = 1
    gauge = 2
    flag = 3
    virtual = 4

    def __str__(self) -> str:  # noqa: D105
        return self.name


@dataclass(kw_only=True)
class Code:
    """Class to represent subsystem codes.

    This class has no lattice associated with it. This contains simply a list of
    stabilizers, gauges, and logical operators.

    The generated code and associated graph structures are immutable: if you need a
    slightly modified version of a code you need to make a new one from scratch.
    """

    logical_ops: t.Sequence[Tableau]
    """The logical operators of the code.

    Each logical operator has length equal to the number of data qubits in the non
    sparse representation. This only stores a pair of logical operators per logical
    qubit. If not user provided, the default only will be the least weight logical
    operators respectively.

    Logical operators need to be ordered in the following way: for each logical
    qubit, first list all logical :math:`X` operators, then the :math:`Z`.
    """
    measured_operators: t.Sequence[Tableau]
    """The operators measured in the single round of QEC.

    This sequence contains the list of operators that need to measured to implement the
    quantum code. A broad definition to include the choice of operators that are
    being measured. This can be :attr:`~factorized_checks` to generate the
    stabilizers, gauge operators of the code.
    """

    factorized_checks: t.Sequence[t.Sequence[int]] = field(default_factory=list)
    """The factors of the stabilizers that are measured.

    A nested list of integers. The outer list has the same length as the number of
    stabilizers of the quantum code. Each inner list contains the indices of
    :attr:`measured_operators` that can be combined to generate the corresponding
    stabilizer generator of the code.
    """

    ancilla_supports: t.Sequence[t.Sequence[int]] = field(default_factory=list)
    """The checks that each ancilla supports.

    Here, by support we mean the measurement of the check is mediated through an
    ancilla. The outermost list cycles through the ancillas. For each ancilla,
    the index of the checks that make use of it are the elements of the inner list.
    """
    _tanner_graph: graph.TannerGraph = field(init=False)
    """The Tanner Graph defining the code."""
    _orchestration_graph: graph.TannerGraph = field(init=False)
    """The orchestration graph implementing the code on hardware."""
    _primal_measured_operators_indices: list[int] = field(init=False)
    """Indices of the primal stabilisers of the code from :attr:`stabilizers`."""
    _dual_measured_operators_indices: list[int] = field(init=False)
    """Indices of the dual stabilisers of the code from :attr:`stabilizers`."""

    # Dunder Methods

    def __post_init__(self):
        """Construct the graphs from the given user data and fill properties."""
        # When factorized checks are not provided, we assume that the measured
        # operators are stabilizers of the code.

        argsorted_mops = argsort_operators_ref(self.measured_operators)
        inverse_args = [0] * len(argsorted_mops)
        for new_index, original_index in enumerate(argsorted_mops):
            inverse_args[original_index] = new_index

        self.measured_operators = [self.measured_operators[i] for i in argsorted_mops]
        if not self.factorized_checks:
            self.factorized_checks = list(
                [i] for i in range(len(self.measured_operators))
            )
        else:
            self.factorized_checks = [
                [inverse_args[idx] for idx in inner_list]
                for inner_list in self.factorized_checks
            ]

        if not self.ancilla_supports:
            self.ancilla_supports = list(
                [i] for i in range(len(self.measured_operators))
            )
        else:
            self.ancilla_supports = [
                [inverse_args[idx] for idx in inner_list]
                for inner_list in self.ancilla_supports
            ]

        # This assumes that the measured operators contain no Y factors
        self._primal_measured_operators_indices = []
        self._dual_measured_operators_indices = []
        for i, meas_op in enumerate(self.measured_operators):
            # Take an operator first and, for each qubit, check if the
            # operator has any X component, assign it to the primal,
            # otherwise to the dual
            x, z, _ = pauli.unpack_tableau(meas_op)
            if np.any(x & z):  # there's a y component?
                raise ValueError(
                    "Cannot decompose stabilisers in primal and dual if they "
                    "contain Y factors."
                )
            if x.any():
                self._dual_measured_operators_indices.append(i)
            else:
                self._primal_measured_operators_indices.append(i)
        # For convenience, we also split the stabilisers in primal and dual. These lists
        # contain indices to factorized_checks to define the stabiliser they represent.
        self._primal_factorized_checks = []
        self._dual_factorized_checks = []
        for check, meas_ops in enumerate(self.factorized_checks):
            # If all measured operators are in the primal group, then add the check that
            # they compose to the primal group of the checks.
            if all(
                map(lambda m: m in self._primal_measured_operators_indices, meas_ops)
            ):
                self._primal_factorized_checks.append(check)
            elif all(
                map(lambda m: m in self._dual_measured_operators_indices, meas_ops)
            ):
                self._dual_factorized_checks.append(check)

        self._generate_tanner_graph()
        self._generate_orchestration_graph()

    def __repr__(self):
        """Make dataclass representation more straightforward."""
        return f"Code<[{pformat(self.code_parameters)}]>"

    @cached_property
    def stabilizers(self) -> npt.NDArray[np.dtype[np.uint8]]:
        """Stabilizers of the Quantum Code.

        Code stabilizers generated from :attr:`measured_operators` and
        :attr:`factorized_checks`.
        """
        checks: list[Tableau] = list()
        for op_idxs in self.factorized_checks:
            ops_list = [self.measured_operators[o] for o in op_idxs]
            checks.append(pauli.multiply(*ops_list)[0])
        return np.array(checks)

    @cached_property
    def primal_stabilizers(self) -> npt.NDArray[np.dtype[np.uint8]]:
        """Primal stabilizers of this code.

        These are the stabilizers who anti-commute with at least one
        :math:`Z` operator acting on a data qubit.
        """
        return self.stabilizers[self._primal_factorized_checks]

    @cached_property
    def dual_stabilizers(self) -> npt.NDArray[np.dtype[np.uint8]]:
        """Dual stabilizers of this code.

        These are the stabilizers who anti-commute with at least one
        :math:`X` operator acting on a data qubit.
        """
        return self.stabilizers[self._dual_factorized_checks]

    @property
    def num_qubits(self) -> int:
        """Number of physical qubits in the code."""
        return self._orchestration_graph.n_nodes

    @property
    def code_parameters(self) -> dict:
        """The parameters of a quantum code.

        Notes:
            There are five parameters definining each code in Plaquette.
            - The total of number of qubits used to implement the code (Code.num_qubits)
            - The number of stabilizers of the quantum code (Code.num_stabilizers)
            - The number of measured operators (Code.num_measured_operators)
            - The number of logical qubits (Code.num_logical qubits)
            - The distances of each logical operator (Code.distances)
        """
        return {
            "num_qubits": self.num_qubits,
            "num_data_qubits": self.num_data_qubits,
            "num_stabilizers": self.num_stabilizers,
            "num_measured_operators": self.num_measured_operators,
            "num_logical_qubits": self.num_logical_qubits,
            "distances": self.distances,
        }

    @cached_property
    def num_data_qubits(self) -> int:
        """Number of data qubits in the code."""
        return pauli.count_qubits(self.stabilizers[0])[0]

    @cached_property
    def num_stabilizers(self) -> int:
        """The number of stabilizer generators of the code.

        By default, we always assume that it's the minimum generating set and the
        stabilizers are independent of each other.

        Notes:
            Using a cached property because it is a possible variable that will be
            accessed multiple times during calculations.
        """
        return len(self.stabilizers)

    @cached_property
    def num_measured_operators(self):
        """Number of measured operators in the code."""
        return len(self.measured_operators)

    @cached_property
    def num_logical_qubits(self) -> int:
        """Number of logical qubits in the code."""
        return len(self.logical_ops) // 2

    @property
    def distance(self) -> int:
        """The distance of the given Code.

        By definition, the distance of a code is the least weight logical operator
        of the code and we assume the provided operators is the least weight logical
        operator.
        """
        return np.min(self.distances)

    @property
    def distances(self) -> np.ndarray:
        """The X and Z distances of each logical qubit."""
        return np.array([np.count_nonzero(op) for op in self.logical_ops])

    @property
    def tanner_graph(self) -> graph.TannerGraph:
        """The graph with edges between stabiliser checks and data qubits.

        Each stabiliser check defines a new node (ancilla/stabiliser node) and
        each qubit involved in the check is a data-qubit node.
        """
        return self._tanner_graph

    @property
    def orchestration_graph(self) -> graph.TannerGraph:
        """The graph describing the actual connectivity between the qubits.

        It's the graph used to generate the actual circuit. A QEC code is always defined
        theoretically by its Tanner graph, but we need this "orchestration" graph when
        generating the circuit in those cases where the user wants to either re-use
        ancillas across checks or the opposite, where they want to split checks among
        different ancillas.

        Each edge carries the information of Pauli factor involved in the checks.

        See Also:
            :doc:`How to create your own codes </advanced/codes/index>`
        """
        return self._orchestration_graph

    @cached_property
    def data_qubit_indices(self):
        """Indices of the data qubits of this code."""
        return [i for i, d in enumerate(self.tanner_graph.nodes) if d.type == "data"]

    @cached_property
    def check_node_indices(self):
        """Indices of the check nodes from the Tanner graph of this code."""
        return [
            i for i, d in enumerate(self.tanner_graph.nodes) if d.type == "stabilizer"
        ]

    @cached_property
    def ancilla_qubit_indices(self):
        """Indices of the ancilla qubits of this code."""
        return [
            i
            for i, d in enumerate(self.orchestration_graph.nodes)
            if d.type == "stabilizer"
        ]

    def _generate_orchestration_graph(self) -> None:
        """Generate the graph of how the Tanner graph is embedded on a real device.

        The current assumption where we don't deal with flags is that
        factorized_checks also define the device connectivity. This is the graph
        which will be used to generate the circuits.

        """
        edges: list[graph.Edge] = list()
        # Indexing is done data-qubits first.
        nodes: list[graph.Node] = list(
            graph.Node(pos=None, type="data") for _ in range(self.num_data_qubits)
        ) + list(
            graph.Node(pos=None, type="stabilizer")
            for _ in range(len(self.ancilla_supports))
        )
        measop_to_edges_map: list[list[int]] = list(
            [] for _ in range(len(self.measured_operators))
        )
        for i, checks in enumerate(self.ancilla_supports):
            for check_idx in checks:
                new_edges = [
                    graph.Edge(
                        a=i + self.num_data_qubits,
                        b=data,  # type: ignore
                        type=factor.name,  # type: ignore
                    )
                    for data, factor in pauli.pauli_to_dict(
                        self.measured_operators[check_idx]
                    ).items()
                ]
                measop_to_edges_map[check_idx] = [
                    i + len(edges) for i in range(len(new_edges))
                ]
                edges.extend(new_edges)

        node_pos = generate_layout_coordinates(
            nodes=list(range(len(nodes))), edges=[(e.a, e.b) for e in edges]
        )
        for idx, pos in node_pos.items():
            nodes[idx].pos = pos

        self._orchestration_graph = graph.TannerGraph(
            nodes=nodes,
            edges=edges,
            checks=measop_to_edges_map,
            primal=self._primal_measured_operators_indices,
            dual=self._dual_measured_operators_indices,
        )

    def _generate_tanner_graph(self):
        """Generate the Tanner graph of data and ancilla qubits."""
        nodes: list[graph.Node] = [
            graph.Node(pos=None, type="data") for _ in range(self.num_data_qubits)
        ] + [
            graph.Node(pos=None, type="stabilizer")
            for _ in range(len(self.factorized_checks))
        ]
        edges: list[graph.Edge] = list()
        edge_to_check_map: list[list[int]] = list()
        for i, support in enumerate([pauli.pauli_to_dict(s) for s in self.stabilizers]):
            ancilla_idx = i + self.num_data_qubits
            edge_to_check_map.append([i + len(edges) for i in range(len(support))])
            edges.extend(
                [
                    graph.Edge(a=ancilla_idx, b=qubit_idx, type=support[qubit_idx].name)
                    for qubit_idx in sorted(support)
                ]
            )

        node_pos = generate_layout_coordinates(
            nodes=list(range(len(nodes))), edges=[(e.a, e.b) for e in edges]
        )
        for idx, pos in node_pos.items():
            nodes[idx].pos = pos

        self._tanner_graph = graph.TannerGraph(
            nodes=nodes,
            edges=edges,
            checks=edge_to_check_map,
            primal=self._primal_factorized_checks,
            dual=self._dual_factorized_checks,
        )

    def to_json(self) -> str:
        """JSON representation of this code, to be used by the visualizer."""
        base = self.tanner_graph
        return graph.CodeGraph(
            nodes=base.nodes,
            edges=base.edges,
            checks=[list(pauli.pauli_to_dict(s).keys()) for s in self.stabilizers],
            logical_surfaces=[
                list(pauli.pauli_to_dict(lo).keys()) for lo in self.logical_ops
            ],
            primal=self.tanner_graph.primal,
            dual=self.tanner_graph.dual,
        ).model_dump_json()

    @classmethod
    def make_rotated_planar(
        cls, distance: int | tuple[int, int], xzzx: bool = False
    ) -> "Code":
        """Generate a :class:`Code` object for rotated planar code.

        Args:
            distance: The distance of the code.
                If ``int``, both X and Z distances are considered to be the same.
                If ``tuple`` of length 2, then interpreted as (X, Z) distances
                respectively.
            xzzx: Bool to determine whether to use xxzx checks.

        Returns:
             A :class:`Code` object corresponding to the rotated planar code.
        """
        if isinstance(distance, int):
            x_distance, z_distance = distance, distance
        elif isinstance(distance, tuple) and len(distance) == 2:
            x_distance, z_distance = distance
        else:
            raise ValueError(
                "distance of must be an integer or tuple of ints of len 2."
            )
        qubit_number = x_distance * z_distance
        if xzzx:
            stabs = []
            for row in range(x_distance - 1):
                for col in range(z_distance - 1):
                    stabs.append(
                        pauli.string_to_pauli(
                            f"X{z_distance * row + col}"
                            f"Z{z_distance * row + col + 1}"
                            f"X{z_distance * (row + 1) + col + 1}"
                            f"Z{z_distance * (row + 1) + col}",
                            qubits=z_distance * x_distance,
                        )
                    )

                    if row == 0 and (col + row) % 2 == 0:
                        stabs.append(
                            pauli.string_to_pauli(
                                f"Z{col}X{col + 1}", qubits=z_distance * x_distance
                            )
                        )
                        stabs.append(
                            pauli.string_to_pauli(
                                f"X{z_distance * (x_distance - 1) + col + 1}"
                                f"Z{z_distance * (x_distance - 1) + col + 2}",
                                qubits=z_distance * x_distance,
                            )
                        )
                    elif col == 0 and (col + row) % 2 != 0:
                        stabs.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * row}X{z_distance * (row + 1)}",
                                qubits=z_distance * x_distance,
                            )
                        )
                        stabs.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * row + z_distance - 1}"
                                f"X{z_distance * (row - 1) + z_distance - 1}",
                                qubits=z_distance * x_distance,
                            )
                        )
            logical_x = pauli.string_to_pauli(
                "".join(
                    [
                        f"Z{z_distance * j}" if j % 2 == 0 else f"X{z_distance*j}"
                        for j in range(x_distance)
                    ]
                ),
                qubit_number,
            )
            logical_z = pauli.string_to_pauli(
                "".join(
                    [f"X{i}" if i % 2 == 0 else f"Z{i}" for i in range(z_distance)]
                ),
                qubit_number,
            )

        else:
            x_stabs = []
            z_stabs = []

            # X boundaries are on top and bottom
            # Z boundaries are on left and right.
            for row in range(x_distance - 1):
                for col in range(z_distance - 1):
                    if (col + row) % 2 == 0:
                        z_stabs.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * row + col}"
                                f"Z{z_distance * row + col + 1}"
                                f"Z{z_distance * (row + 1) + col}"
                                f"Z{z_distance * (row + 1) + col + 1}",
                                qubit_number,
                            )
                        )
                        if row == 0:
                            x_stabs.append(
                                pauli.string_to_pauli(f"X{col}X{col + 1}", qubit_number)
                            )
                            # FIXME: extra qubit count for even indices.
                            x_stabs.append(
                                pauli.string_to_pauli(
                                    f"X{z_distance * (x_distance - 1) + col + 1}"
                                    f"X{z_distance * (x_distance - 1) + col + 2}",
                                    qubit_number,
                                )
                            )

                    else:
                        x_stabs.append(
                            pauli.string_to_pauli(
                                f"X{z_distance * row + col}"
                                f"X{z_distance * row + col + 1}"
                                f"X{z_distance * (row + 1) + col}"
                                f"X{z_distance * (row + 1) + col + 1}",
                                qubit_number,
                            )
                        )
                        if col == 0:
                            z_stabs.append(
                                pauli.string_to_pauli(
                                    f"Z{z_distance * row}Z{z_distance * (row + 1)}",
                                    qubit_number,
                                )
                            )

                            z_stabs.append(
                                pauli.string_to_pauli(
                                    f"Z{z_distance * row + z_distance - 1}"
                                    f"Z{z_distance * (row - 1) + z_distance - 1}",
                                    qubit_number,
                                )
                            )

            stabs = x_stabs + z_stabs

            logical_x = pauli.string_to_pauli(
                "".join([f"X{z_distance * j}" for j in range(x_distance)]),
                qubit_number,
            )
            logical_z = pauli.string_to_pauli(
                "".join([f"Z{i}" for i in range(z_distance)]),
                qubit_number,
            )

        return cls(
            logical_ops=[logical_x, logical_z],
            measured_operators=stabs,
        )

    @classmethod
    def make_bacon_shor(
        cls, distance: int | tuple[int, int], measure_gauges: bool = False
    ) -> "Code":
        """Generate a :class:`Code` object for the Bacon-Shor Code.

        The Bacon Shor code is defined on a square lattice with data qubits on
        vertices of the lattice. When measuring through gauges, the ancilla qubits
        lie on the edges, with X gauges on vertical edges and Z gauges on horizontal
        edges.

        Args:
            distance: The distance of the code.
                If ``int``, both X and Z distances are considered to be the same.
                If ``tuple`` of length 2, then interpreted as (X, Z) distances
                respectively.
            measure_gauges: Bool to determine measure gauges or stabilizer directly.

        Returns:
            A :class:`Code` object corresponding to the 2D Bacon-Shor code.
        """
        if isinstance(distance, int):
            x_distance, z_distance = distance, distance
        elif isinstance(distance, tuple) and len(distance) == 2:
            x_distance, z_distance = distance
        else:
            raise ValueError(
                "distance of must be an integer or tuple of ints of len 2."
            )

        qubit_number = x_distance * z_distance

        stabs = pauli.sort_operators_ref(
            [
                pauli.string_to_pauli(
                    "".join(
                        [
                            f"X{j * x_distance + i}X{(j + 1) * x_distance + i}"
                            for i in range(x_distance)
                        ]
                    ),
                    qubit_number,
                )
                for j in range(z_distance - 1)
            ]
            + [
                pauli.string_to_pauli(
                    "".join(
                        [
                            f"Z{j * x_distance + i}Z{j * x_distance + i + 1}"
                            for j in range(z_distance)
                        ]
                    ),
                    qubit_number,
                )
                for i in range(x_distance - 1)
            ]
        )

        gauges = pauli.sort_operators_ref(
            [
                pauli.string_to_pauli(
                    f"X{j * x_distance + i}X{(j + 1) * x_distance + i}",
                    qubit_number,
                )
                for i in range(x_distance)
                for j in range(z_distance - 1)
            ]
            + [
                pauli.string_to_pauli(
                    f"Z{j * x_distance + i}Z{j * x_distance + i + 1}",
                    qubit_number,
                )
                for i in range(x_distance - 1)
                for j in range(z_distance)
            ]
        )

        logical_x = pauli.string_to_pauli(
            "".join([f"X{i}" for i in range(x_distance)]),
            qubit_number,
        )
        logical_z = pauli.string_to_pauli(
            "".join([f"Z{j * x_distance}" for j in range(z_distance)]),
            qubit_number,
        )

        if measure_gauges:
            bs = cls(
                measured_operators=gauges,
                logical_ops=[logical_x, logical_z],
                factorized_checks=_generate_factorized_checks(stabs, gauges),
            )
        else:
            bs = cls(measured_operators=stabs, logical_ops=[logical_x, logical_z])

        for row in range(x_distance):
            for col in range(z_distance):
                idx = row * x_distance + col
                pos = graph.Position(x=col, y=row * x_distance, z=0)
                bs.tanner_graph.nodes[idx].pos = pos
                bs.orchestration_graph.nodes[idx].pos = pos

        for anc in bs.check_node_indices:
            neigh: list[graph.Position] = list()
            for v in bs.tanner_graph.neighbours_of(anc):
                pos = t.cast(graph.Position, bs.tanner_graph.nodes[v].pos)
                if pos is not None:
                    x, y, z = pos
                    neigh.append(graph.Position(x=x, y=y, z=z))
            bs.tanner_graph.nodes[anc].pos = graph.center_of_mass(neigh)

        for anc in bs.ancilla_qubit_indices:
            neigh = list()
            for v in bs.orchestration_graph.neighbours_of(anc):
                pos = t.cast(graph.Position, bs.orchestration_graph.nodes[v].pos)
                if pos is not None:
                    x, y, z = pos
                    neigh.append(graph.Position(x=x, y=y, z=z))
            bs.orchestration_graph.nodes[anc].pos = graph.center_of_mass(neigh)
        return bs

    @classmethod
    def make_planar(cls, distance: int | tuple[int, int]) -> "Code":
        """Generate a :class:`Code` object for planar code.

        Args:
            distance: The distance of the code.
                    If ``int``, both X and Z distances are considered to be the same.
                    If ``tuple`` of length 2, then interpreted as (X, Z) distances
                    respectively.

        Returns:
            A :class:`Code` object corresponding to the planar code.

        """
        if isinstance(distance, int | np.integer):
            x_distance, z_distance = distance, distance
        elif isinstance(distance, tuple) and len(distance) == 2:
            x_distance, z_distance = distance
        else:
            raise ValueError(
                "distance of must be an integer or tuple of ints of len 2."
            )

        data_indices = []  # list containing the indices of the data qubits.
        nodes_coords: list[dict] = []
        num_data = 0  # counter for the data qubit index
        # populate data qubit list.
        for row in range(2 * z_distance - 1):
            if row % 2 == 0:
                data_indices.append(list(range(num_data, num_data + x_distance)))
                num_data = num_data + x_distance
            else:
                data_indices.append(list(range(num_data, num_data + x_distance - 1)))
                num_data = num_data + x_distance - 1

            for col in range(2 * x_distance - 1):
                # add coords
                if ((row % 2) and (col % 2)) or (not ((row % 2) or (col % 2))):
                    nodes_coords.append(dict(x=col, y=row, z=0))

        z_stabs, x_stabs = [], []

        for r, qubits in enumerate(data_indices):
            # use even row for Z stabilisers
            if r % 2 == 0:
                for qubit_index in qubits[:-1]:
                    if r == 0:
                        # if bottom boundary add 3 body stabilisers pointing up.
                        z_stabs.append(
                            pauli.string_to_pauli(
                                f"Z{qubit_index}"
                                f"Z{qubit_index + 1}"
                                f"Z{qubit_index + x_distance}",
                                qubits=num_data,
                            )
                        )
                    elif r == len(data_indices) - 1:
                        # if top boundary add 3 body stabilisers pointing down.
                        z_stabs.append(
                            pauli.string_to_pauli(
                                f"Z{qubit_index}"
                                f"Z{qubit_index + 1}"
                                f"Z{qubit_index - x_distance + 1}",
                                qubits=num_data,
                            )
                        )
                    else:
                        z_stabs.append(
                            pauli.string_to_pauli(
                                f"Z{qubit_index}"
                                f"Z{qubit_index + 1}"
                                f"Z{qubit_index + x_distance}"
                                f"Z{qubit_index - x_distance + 1}",
                                qubits=num_data,
                            )
                        )
            # use odd rows or X stabilisers
            else:
                for c, qubit_index in enumerate(qubits):
                    if c == len(qubits) - 1:
                        # if right boundary, add 3 body stabiliser pointing left.
                        x_stabs.append(
                            pauli.string_to_pauli(
                                f"X{qubit_index}"
                                f"X{qubit_index - x_distance + 1}"
                                f"X{qubit_index + x_distance}",
                                qubits=num_data,
                            )
                        )
                        continue
                    elif c == 0:
                        # if left boundary, add 3 body stabiliser pointing right.
                        # there is no continue in this elif block, because num
                        # qubits in this row is one less than number of
                        # stabiliser added in this row. We are adding twice for
                        # the first entry of the row.
                        x_stabs.append(
                            pauli.string_to_pauli(
                                f"X{qubit_index}"
                                f"X{qubit_index - x_distance}"
                                f"X{qubit_index + x_distance - 1}",
                                qubits=num_data,
                            )
                        )

                    x_stabs.append(
                        pauli.string_to_pauli(
                            f"X{qubit_index}"
                            f"X{qubit_index + 1}"
                            f"X{qubit_index + x_distance}"
                            f"X{qubit_index - x_distance + 1}",
                            qubits=num_data,
                        )
                    )

        logicals = [
            pauli.string_to_pauli(
                "".join([f"X{i}" for i in range(x_distance)]), qubits=num_data
            )
        ] + [
            pauli.string_to_pauli(
                "".join(
                    [
                        f"Z{data_indices[i][0]}"
                        for i in range(len(data_indices))
                        if i % 2 == 0
                    ]
                ),
                qubits=num_data,
            )
        ]
        ssc = Code(measured_operators=z_stabs + x_stabs, logical_ops=logicals)
        for node in range(ssc.num_data_qubits):
            ssc.tanner_graph.nodes[node].pos = graph.Position(**nodes_coords[node])

        # Add ancilla coords
        for anc in ssc.check_node_indices:
            neigh = list()
            for v in ssc.tanner_graph.neighbours_of(anc):
                if (pos := ssc.tanner_graph.nodes[v].pos) is not None:
                    x, y, z = pos
                    neigh.append(graph.Position(x=x, y=y, z=z))
            ssc.tanner_graph.nodes[anc].pos = graph.center_of_mass(neigh)

        return ssc

    @classmethod
    def make_repetition(cls, distance: int, phase_flip: bool = False) -> "Code":
        """Generate a :class:`Code` object for bit(phase) flip repetition code.

        By default, it makes the code the corrects bit flips.

        Args:
            distance: The distance of the code.
            phase_flip: Bool to determine if the correct bit flips or phase flips.
                Defaults to ``False``, which correct bit flips.
                If ``True``, generates stabilisers to correct for phase flips.

        Returns:
            A :class:`Code` object corresponding to the bit(phase) flip
            repetition code.
        """
        if not phase_flip:
            stab_factor = "Z"
            logicals = [
                pauli.string_to_pauli("X" * distance),
                pauli.string_to_pauli("Z0", qubits=distance),
            ]

        else:
            stab_factor = "X"
            logicals = [
                pauli.string_to_pauli("X0", qubits=distance),
                pauli.string_to_pauli("Z" * distance),
            ]

        stabs = [
            pauli.string_to_pauli(
                f"{stab_factor}{i}{stab_factor}{i + 1}", qubits=distance
            )
            for i in range(distance - 1)
        ]
        return Code(measured_operators=stabs, logical_ops=logicals)

    @classmethod
    def make_steane(cls, compact=False):
        """Generate a :class:`Code` object for the Steane code.

        Args:
            compact: Bool to determine whether any ancilla is used across multiple
                measurements.

        Returns:
            A :class:`Code` object corresponding to the Steane code.
        """
        stabs = [
            pauli.string_to_pauli("X0X1X3X4", 7),
            pauli.string_to_pauli("X1X2X4X5", 7),
            pauli.string_to_pauli("X3X4X5X6", 7),
        ] + [
            pauli.string_to_pauli("Z0Z1Z3Z4", 7),
            pauli.string_to_pauli("Z1Z2Z4Z5", 7),
            pauli.string_to_pauli("Z3Z4Z5Z6", 7),
        ]
        logicals = [
            pauli.string_to_pauli("X0X1X2", qubits=7),
            pauli.string_to_pauli("Z0Z1Z2", qubits=7),
        ]

        if not compact:
            return Code(measured_operators=stabs, logical_ops=logicals)
        if compact:
            return Code(
                measured_operators=stabs,
                logical_ops=logicals,
                ancilla_supports=[[i, i + 3] for i in range(3)],
            )

    @classmethod
    def make_heavy_hex_without_flag(
        cls, distance: int | tuple[int, int], measure_gauges=True, compact=False
    ):
        """Class method to make the heavy hexagon code.

        This implementation does not add the flag qubits.

        Args:
            distance: The distance of the code.
                If ``int``, both X and Z distances are considered to be the same.
                If ``tuple`` of length 2, then interpreted as (X, Z) distances
                respectively.
            compact: Bool to determine whether ancilla are shared across stabilisers.
            measure_gauges: Bool to determine whether to measure gauges of stabilisers.

        Returns:
            A :class:`~Code` corresponding to the heavy hexagon code without
            the flag qubits.

        TODO: Bug fixes are required for the correct edges. Currently it generates a
        wrong list.
        """
        if isinstance(distance, int):
            x_distance, z_distance = distance, distance
        elif isinstance(distance, tuple) and len(distance) == 2:
            x_distance, z_distance = distance
        else:
            raise ValueError(
                "distance of must be an integer or tuple of ints of len 2."
            )

        # X boundaries lie on top and bottom.
        # Z boundaries lie on left and right.

        x_gauges, z_gauges = [], []
        z_stabs = []

        x_stabs = [
            pauli.string_to_pauli(
                "".join(
                    [
                        f"X{x_distance * row + col}X{x_distance * row + col + 1}"
                        for row in range(x_distance)
                    ]
                ),
                qubits=z_distance * x_distance,
            )
            for col in range(z_distance - 1)
        ]

        for row in range(x_distance - 1):
            for col in range(z_distance - 1):
                if (row + col) % 2 == 0:
                    x_gauges.append(
                        pauli.string_to_pauli(
                            f"X{z_distance * row + col}"
                            f"X{z_distance * row + col + 1}"
                            f"X{z_distance * (row + 1) + col}"
                            f"X{z_distance * (row + 1) + col + 1}",
                            qubits=z_distance * x_distance,
                        )
                    )
                    if col == 0:
                        z_gauges.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * (row + 2) + col}"
                                f"Z{z_distance * (row + 1) + col}",
                                qubits=z_distance * x_distance,
                            )
                        )
                        z_gauges.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * (row + 2) - 1}"
                                f"Z{z_distance * (row + 3) - 1}",
                                qubits=z_distance * x_distance,
                            )
                        )
                        z_stabs.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * (row + 2) - 1}"
                                f"Z{z_distance * (row + 3) - 1}",
                                qubits=z_distance * x_distance,
                            )
                        )

                        z_stabs.append(
                            pauli.string_to_pauli(
                                f"Z{z_distance * row + col}"
                                f"Z{z_distance * (row + 1) + col}",
                                qubits=z_distance * x_distance,
                            )
                        )

                else:
                    z_stabs.append(
                        pauli.string_to_pauli(
                            f"Z{z_distance * row + col}"
                            f"Z{z_distance * row + col + 1}"
                            f"Z{z_distance * (row + 1) + col}"
                            f"Z{z_distance * (row + 1) + col + 1}",
                            qubits=z_distance * x_distance,
                        )
                    )
                    z_gauges.append(
                        pauli.string_to_pauli(
                            f"Z{z_distance * row + col}"
                            f"Z{z_distance * (row + 1) + col}",
                            qubits=z_distance * x_distance,
                        )
                    )
                    z_gauges.append(
                        pauli.string_to_pauli(
                            f"Z{z_distance * row + col + 1}"
                            f"Z{z_distance * (row + 1) + col + 1}",
                            qubits=z_distance * x_distance,
                        )
                    )
                    if row == 0:
                        x_gauges.append(
                            pauli.string_to_pauli(
                                f"X{col}X{col + 1}", qubits=z_distance * x_distance
                            )
                        )
                        x_gauges.append(
                            pauli.string_to_pauli(
                                f"X{col + z_distance * (x_distance - 1)}"
                                f"X{col + z_distance * (x_distance - 1) - 1}",
                                qubits=z_distance * x_distance,
                            )
                        )

        logical_x = pauli.string_to_pauli(
            "".join([f"X{z_distance * j}" for j in range(x_distance)]),
            qubits=z_distance * x_distance,
        )
        logical_z = pauli.string_to_pauli(
            "".join([f"Z{i}" for i in range(z_distance)]),
            qubits=z_distance * x_distance,
        )

        if not compact:
            if measure_gauges:
                raise NotImplementedError(
                    "Only direct measurement these stabilizers is possible currently."
                )
            else:
                return Code(
                    measured_operators=x_stabs + z_stabs,
                    logical_ops=[logical_x + logical_z],
                )
        else:
            if measure_gauges:
                raise NotImplementedError(
                    "Only direct measurement these stabilizers is possible currently."
                )
            else:
                raise NotImplementedError(
                    "Only direct measurement these stabilizers is possible currently."
                )

    @classmethod
    def make_five_qubit(cls) -> "Code":
        """Generate :class:`Code` object for the five qubit code."""
        stabiliser = [
            pauli.string_to_pauli(s, qubits=5)
            for s in "XZZXI IXZZX XIXZZ ZXIXZ".split()
        ]
        logical_ops = [
            pauli.string_to_pauli(log, qubits=5) for log in "XXXXX ZZZZZ".split()
        ]

        return cls(measured_operators=stabiliser, logical_ops=logical_ops)

    @classmethod
    def make_shor(cls) -> "Code":
        """Generate :class:`Code` object for the 9-qubit Shor code."""
        stabilisers = [
            pauli.string_to_pauli(s, qubits=9)
            for s in """
            ZZIIIIIII
            IZZIIIIII
            XXXXXXIII
            IIIZZIIII
            IIIIZZIII
            IIIXXXXXX
            IIIIIIZZI
            IIIIIIIZZ
            """.split()
        ]
        logicals = [pauli.string_to_pauli(log, qubits=9) for log in [9 * "Z", 9 * "X"]]
        return cls(measured_operators=stabilisers, logical_ops=logicals)

    @classmethod
    def make_subsystem_surface_code(cls, distance: int):
        """Generate a :class:`Code` object for rotated planar code.

        Args:
            distance: The distance of the code.
                If ``int``, both X and Z distances are considered to be the same.
                If ``tuple`` of length 2, then interpreted as (X, Z) distances
                respectively.

        Returns:
             A :class:`Code` object corresponding to the subsystem surface code.
        """
        gauges = []
        n_data = 3 * distance**2 + 4 * distance + 1

        # nodes on vertices and horizontal edges.
        vtx_he = np.vstack(
            [
                np.arange(i, i + 2 * distance + 1)
                for i in np.arange(0, n_data, 3 * distance + 2)
            ]
        )
        # nodes on vertical edges.
        v_e = np.vstack(
            [
                np.arange(i, i + distance + 1)
                for i in np.arange(2 * distance + 1, n_data, 3 * distance + 2)
            ]
        )

        factorized_checks: list[list[int]] = []

        def pre_process_op(spt: tuple, factor: str) -> pauli.Tableau:
            """Preprocess Op to add to the gauge or logop list.

            Args:
                spt: Support of the operator
                factor: The pauli factor
            """
            return pauli.string_to_pauli(
                "".join([f"{factor}{k}" for k in spt]), qubits=n_data
            )

        for i in range(v_e.shape[0]):
            for j in range(v_e.shape[1]):
                # top part of the plaquette
                if j == 0:
                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i][2 * j], vtx_he[i][2 * j + 1]), "X"
                        )
                    )

                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i + 1][2 * j], vtx_he[i + 1][2 * j + 1]),
                            factor="Z",
                        )
                    )

                elif j == distance:
                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i][2 * j - 1], vtx_he[i][2 * j]), "Z"
                        )
                    )
                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i + 1][2 * j - 1], vtx_he[i + 1][2 * j]),
                            "X",
                        )
                    )

                else:
                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i][2 * j - 1], vtx_he[i][2 * j]), "Z"
                        )
                    )
                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i + 1][2 * j - 1], vtx_he[i + 1][2 * j]),
                            "X",
                        )
                    )

                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i][2 * j], vtx_he[i][2 * j + 1]),
                            "X",
                        )
                    )

                    gauges.append(
                        pre_process_op(
                            (v_e[i][j], vtx_he[i + 1][2 * j], vtx_he[i + 1][2 * j + 1]),
                            "Z",
                        )
                    )

        logops = []
        logops.append(
            pauli.string_to_pauli("".join([f"Z{i}" for i in vtx_he[0]]), qubits=n_data)
        )
        logops.append(
            pauli.string_to_pauli(
                "".join([f"X{r[0]}" for r in vtx_he] + [f"X{r[0]}" for r in v_e]),
                qubits=n_data,
            )
        )
        gauges = pauli.sort_operators_ref(gauges)
        logs = pauli.sort_operators_ref(logops)

        g_idxs = np.arange(len(gauges)).reshape(2 * 2 * distance, distance)

        for i in range(0, g_idxs.shape[0], 2):
            for j in range(g_idxs.shape[1]):
                factorized_checks.append([g_idxs[i][j], g_idxs[i + 1][j]])

        bdry_stabs = []

        # X boundaries on the top and bottom.

        bdry_stabs.extend(
            [
                pre_process_op((vtx_he[0][i], vtx_he[0][i + 1]), "X")
                for i in range(1, 2 * distance + 1, 2)
            ]
        )

        bdry_stabs.extend(
            [
                pre_process_op((vtx_he[-1][i], vtx_he[-1][i + 1]), "X")
                for i in range(0, 2 * distance, 2)
            ]
        )

        # Z boundaries on the left and right,
        bdry_stabs.extend(
            [pre_process_op((vtx_he[i][0], v_e[i][0]), "Z") for i in range(len(v_e))]
        )
        bdry_stabs.extend(
            [
                pre_process_op((vtx_he[i + 1][-1], v_e[i][-1]), "Z")
                for i in range(len(v_e))
            ]
        )

        factorized_checks.extend(
            [[i] for i in range(len(gauges), len(gauges) + len(bdry_stabs))]
        )

        ssc = Code(
            measured_operators=gauges + bdry_stabs,
            logical_ops=logs,
            factorized_checks=factorized_checks,
        )

        for row in range(2 * distance + 1):
            if row % 2 == 0:
                for k, idx in enumerate(vtx_he[row // 2]):
                    ssc.tanner_graph.nodes[idx].pos = graph.Position(x=k, y=row, z=0)
                    ssc.orchestration_graph.nodes[idx].pos = graph.Position(
                        x=k, y=row, z=0
                    )
            else:
                for k, idx in enumerate(v_e[row // 2]):
                    ssc.tanner_graph.nodes[idx].pos = graph.Position(
                        x=2 * k, y=row, z=0
                    )
                    ssc.orchestration_graph.nodes[idx].pos = graph.Position(
                        x=2 * k, y=row, z=0
                    )

        for anc in ssc.check_node_indices:
            neigh = list()
            for v in ssc.tanner_graph.neighbours_of(anc):
                if (pos := ssc.tanner_graph.nodes[v].pos) is not None:
                    x, y, z = pos
                    neigh.append(graph.Position(x=x, y=y, z=z))
            ssc.tanner_graph.nodes[anc].pos = graph.center_of_mass(neigh)

        for anc in ssc.ancilla_qubit_indices:
            neigh = list()
            for v in ssc.orchestration_graph.neighbours_of(anc):
                if (pos := ssc.orchestration_graph.nodes[v].pos) is not None:
                    x, y, z = pos
                    neigh.append(graph.Position(x=x, y=y, z=z))
            ssc.orchestration_graph.nodes[anc].pos = graph.center_of_mass(neigh)

        return ssc
