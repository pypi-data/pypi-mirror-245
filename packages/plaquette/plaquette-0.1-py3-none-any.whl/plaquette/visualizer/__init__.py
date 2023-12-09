# Copyright 2023, QC Design GmbH and the plaquette contributors
# SPDX-License-Identifier: Apache-2.0

# TODO: remove once new API is working:
# type: ignore # noqa
"""Visualization tools.

When working with a QEC code, it can be useful to work with a graphical
representation of the whole code, which describes both data and ancilla qubits.
Such a graphical representation can be obtained as follows:

>>> from plaquette import codes, visualizer
>>> code = codes.Code.make_planar(3)
>>> vis = visualizer.Visualizer(code)
>>> vis.draw()  # doctest: +ELLIPSIS
Figure({...

The section :ref:`codes-guide` contains many examples of code visualizations.

If you also want to draw errors, syndrome data ond/or corrections, refer to
:meth:`Visualizer.draw` or :ref:`viz-guide`. Using such a
drawing, you can explore the relation between individual errors and triggered
syndrome bits as well as determine why a given correction succeeded or failed.

You can also visualise circuits that you generate from codes, using the
:class:`CircuitVisualizer`. This will use Qiskit under the hood to render the
circuit into a ``matplotlib`` figure.

.. important::

    When generating a circuit, you can provide error information to model
    hardware-relevant use-cases. These types of errors are usually represented
    as probabilistic gates, which are impossible to represent with standard
    quantum circuit symbols. This means that **circuits containing error
    instructions cannot be rendered**.
"""
import enum
import typing as t

import numpy as np
import plotly.graph_objects as go  # type: ignore
import qiskit
from qiskit import qasm3

from plaquette import circuit, codes, errors, pauli
from plaquette.circuit import openqasm


class VertexType(enum.Enum):
    """Types of nodes displayed on the visualizer."""

    Data = enum.auto()
    ErrorX = enum.auto()
    ErrorY = enum.auto()
    ErrorZ = enum.auto()
    Logical = enum.auto()
    CorrectionX = enum.auto()
    CorrectionY = enum.auto()
    CorrectionZ = enum.auto()
    Primal = enum.auto()
    PrimalToggled = enum.auto()
    Dual = enum.auto()
    DualToggled = enum.auto()


class Visualizer:
    """A simple 2D visualizer for ``plaquette`` :class:`.Code` objects.

    .. automethod:: __init__
    """

    frame_offsets = {
        VertexType.ErrorX: (0.15, -0.15),
        VertexType.ErrorY: (0, -0.15),
        VertexType.ErrorZ: (-0.15, -0.15),
        VertexType.CorrectionX: (0.15, 0.15),
        VertexType.CorrectionY: (0, 0.15),
        VertexType.CorrectionZ: (-0.15, 0.15),
    }
    """Offsets for plotting error/correction markers on data qubits."""
    vertex_kw = {
        VertexType.Data: dict(
            name="Data qubit", marker=dict(color="firebrick", symbol="circle", size=25)
        ),
        VertexType.Dual: dict(
            name="Primal stabilizer",
            marker=dict(color="midnightblue", symbol="x", size=10),
        ),
        VertexType.DualToggled: dict(
            name="Toggled primal stabilizer",
            marker=dict(color="deepskyblue", symbol="x", size=10),
        ),
        VertexType.Primal: dict(
            name="Dual stabilizer", marker=dict(color="green", symbol="cross", size=10)
        ),
        VertexType.PrimalToggled: dict(
            name="Toggled dual stabilizer",
            marker=dict(color="fuchsia", symbol="cross", size=10),
        ),
        VertexType.Logical: dict(
            name="Logical operator", marker=dict(color="orange", symbol="star", size=15)
        ),
        VertexType.ErrorX: dict(
            name="X error",
            marker=dict(color="red", symbol="x", size=7),
        ),
        VertexType.ErrorY: dict(
            name="Y error",
            marker=dict(color="red", symbol="asterisk-open", size=8),
        ),
        VertexType.ErrorZ: dict(
            name="Z error",
            marker=dict(color="red", symbol="cross", size=7),
        ),
        VertexType.CorrectionX: dict(
            name="X correction",
            marker=dict(color="limegreen", symbol="x", size=7),
        ),
        VertexType.CorrectionY: dict(
            name="Y correction",
            marker=dict(color="limegreen", symbol="asterisk-open", size=8),
        ),
        VertexType.CorrectionZ: dict(
            name="Z correction",
            marker=dict(color="limegreen", symbol="cross", size=7),
        ),
    }
    vertex_kw_grayed_out = {
        VertexType.Data: dict(
            name="Data qubit", marker=dict(color="lightgray", symbol="circle", size=25)
        ),
        VertexType.Primal: dict(
            name="Primal stabilizer",
            marker=dict(color="darkgray", symbol="x", size=10),
        ),
        VertexType.PrimalToggled: dict(
            name="Toggled primal stabilizer",
            marker=dict(color="deepskyblue", symbol="x", size=10),
        ),
        VertexType.Dual: dict(
            name="Dual stabilizer",
            marker=dict(color="darkgray", symbol="cross", size=10),
        ),
        VertexType.DualToggled: dict(
            name="Toggled dual stabilizer",
            marker=dict(color="fuchsia", symbol="cross", size=10),
        ),
        VertexType.Logical: dict(
            name="Logical operator", marker=dict(color="orange", symbol="star", size=15)
        ),
        VertexType.ErrorX: dict(
            name="X error",
            marker=dict(color="red", symbol="x", size=7),
        ),
        VertexType.ErrorZ: dict(
            name="Z error",
            marker=dict(color="red", symbol="cross", size=7),
        ),
        VertexType.CorrectionX: dict(
            name="X correction",
            marker=dict(color="limegreen", symbol="x", size=7),
        ),
        VertexType.CorrectionZ: dict(
            name="Z correction",
            marker=dict(color="limegreen", symbol="cross", size=7),
        ),
    }
    """Plot options for drawing nodes grayed out."""

    edge_kw = {
        pauli.Factor.X: dict(
            name="Pauli X", line=dict(color="cornflowerblue", dash="solid")
        ),
        pauli.Factor.Z: dict(
            name="Pauli Z", line=dict(color="yellowgreen", dash="5px 5px")
        ),
    }
    """Plot options for drawing edges."""
    edge_kw_grayed_out = {
        pauli.Factor.X: dict(
            name="Pauli X", line=dict(color="lightgray", dash="solid")
        ),
        pauli.Factor.Z: dict(
            name="Pauli Z", line=dict(color="lightgray", dash="5px 5px")
        ),
    }

    def __init__(
        self,
        code: codes.Code,
        error_data: errors.QubitErrorsDict | None = None,
        graph: t.Literal["tanner_graph", "orchestration_graph"] = "tanner_graph",
    ):
        """Create a visualizer.

        .. seealso:: :doc:`/advanced/viz/index`

        Args:
            code: code to be visualized. Each node in the underlying graph needs to be
                equipped with coordinates, or the visualizer will not work.
            error_data: error data associated with the various qubits.
            graph: Indication of which graph to draw.
                One of "tanner_graph" (default) or "orchestration_graph".
        """
        self.code = code
        """The QEC to visualize.

        .. important::

           Changing this after constructing the visualizer can lead to weird artefacts.
        """
        self.error_data = error_data
        """Error probabilities and mechanisms on the code.

        .. important::

           By their nature, gate and measurement errors cannot be visualized!
        """
        self.graph = (
            self.code.tanner_graph
            if graph == "tanner_graph"
            else self.code.orchestration_graph
        )

    def draw(
        self,
        syndrome: np.ndarray | None = None,
        error: pauli.Tableau | None = None,
        error_mechanism: t.Literal["x", "y", "z"] | None = None,
        correction: pauli.Tableau | None = None,
        grey: bool = False,
        draw_edges: bool = True,
        height: int = 600,
        margin: int = 20,
    ):
        """Draw the code and, if available, additional data.

        Args:
            syndrome: syndrome bits you want to visualize.
            error: an error operator to overlay on the data qubits.
            error_mechanism: a string (``"x"``, ``"y"``, ``"z"``) to choose which
                Pauli error probability to use to color the data qubits, if
                ``error_data`` was supplied when creating the visualizer.
            correction: a correction operator to overlay on the data qubits.
            grey: whether to grey-out everything except syndrome nodes,
                error, and correction operators. Useful to highlight what happened
                to the code after simulation.
            draw_edges: whether to draw edges representing the stabilizer factors.
            height: Height of the figure in pixels.
            margin: Margin of the figure in pixels.

        Example:
            See :ref:`viz-guide`.
        """
        """Internal drawing function (Plotly)."""
        fig = go.Figure()
        fig.update_layout(height=height, margin={k: margin for k in "lrtb"})
        fig.update_yaxes(scaleanchor="x", scaleratio=1.0)
        if draw_edges:
            # Place and draw all edges first, they need to appear below the nodes
            x = {pauli.Factor.X: [], pauli.Factor.Z: []}
            y = {pauli.Factor.X: [], pauli.Factor.Z: []}
            for edge in self.graph.edges:
                # The "None"s are to make sure that the edges do not "loop around",
                # since we are plotting everything as a single line
                x[pauli.Factor[edge.type]].append(self.graph.nodes[edge.a].pos.x)
                x[pauli.Factor[edge.type]].append(self.graph.nodes[edge.b].pos.x)
                x[pauli.Factor[edge.type]].append(None)
                y[pauli.Factor[edge.type]].append(self.graph.nodes[edge.a].pos.y)
                y[pauli.Factor[edge.type]].append(self.graph.nodes[edge.b].pos.y)
                y[pauli.Factor[edge.type]].append(None)

            edge_style = self.edge_kw_grayed_out if grey else self.edge_kw
            fig.add_trace(
                go.Scatter(
                    x=x[pauli.Factor.X],
                    y=y[pauli.Factor.X],
                    mode="lines",
                    **edge_style[pauli.Factor.X],
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x[pauli.Factor.Z],
                    y=y[pauli.Factor.Z],
                    mode="lines",
                    **edge_style[pauli.Factor.Z],
                )
            )

        fig.update_layout(coloraxis_colorbar_x=-0.1)

        # Draw logical operators as fat lines
        n_log = self.code.num_logical_qubits
        for i, op in enumerate(self.code.logical_ops):
            if i < n_log:
                color = "midnightblue"
                hovertext = f"Logical X{i}"
            else:
                color = "forestgreen"
                hovertext = f"Logical Z{i % n_log}"
            xcoords = list()
            ycoords = list()
            for qubit in pauli.pauli_to_dict(op).keys():
                pos = self.graph.nodes[qubit].pos
                xcoords.append(pos.x)
                ycoords.append(pos.y)

            fig.add_trace(
                go.Scatter(
                    x=xcoords,
                    y=ycoords,
                    mode="lines",
                    line=dict(color=color, width=15),
                    name=hovertext,
                    opacity=0.4,
                )
            )

        # Finally, draw all nodes

        # We assume that ALL possible nodes will be draw, so we prepare
        # a mapping of node type and their coordinates and hover text
        nodes = {
            VertexType.Data: {"x": [], "y": [], "hover": []},
            VertexType.Primal: {"x": [], "y": [], "hover": []},
            VertexType.PrimalToggled: {"x": [], "y": [], "hover": []},
            VertexType.Dual: {"x": [], "y": [], "hover": []},
            VertexType.DualToggled: {"x": [], "y": [], "hover": []},
            VertexType.ErrorX: {"x": [], "y": [], "hover": []},
            VertexType.ErrorY: {"x": [], "y": [], "hover": []},
            VertexType.ErrorZ: {"x": [], "y": [], "hover": []},
            VertexType.CorrectionX: {"x": [], "y": [], "hover": []},
            VertexType.CorrectionY: {"x": [], "y": [], "hover": []},
            VertexType.CorrectionZ: {"x": [], "y": [], "hover": []},
        }
        # Then we take care of the fact that errors and/or correction operators
        # were supplied and transform them into dictionaries so we can quickly
        # map indices to operators
        error_support = pauli.pauli_to_dict(error) if error is not None else {}
        correction_support = (
            pauli.pauli_to_dict(correction) if correction is not None else {}
        )
        # Now for each node, we check if we need to draw an ancilla (and of what type)
        # or a data qubit. These three nodes will ALWAYS be present.
        for i, node in enumerate(self.graph.nodes):
            if node.type == "data":
                vertex_type = VertexType.Data
                hover = f"Qubit #{i} - data"
                # For data qubits, we need to take into account possible error or
                # correction operators, and draw the necessary marker near the current
                # data qubit they "belong" to
                if i in error_support:
                    error_node = (
                        VertexType.ErrorX
                        if error_support[i] == pauli.Factor.X
                        else VertexType.ErrorY
                        if error_support[i] == pauli.Factor.Y
                        else VertexType.ErrorZ
                    )
                    x_offset, y_offset = self.frame_offsets[error_node]
                    nodes[error_node]["x"].append(node.pos.x + x_offset)
                    nodes[error_node]["y"].append(node.pos.y + y_offset)
                    nodes[error_node]["hover"].append(
                        "X-error"
                        if error_node == VertexType.ErrorX
                        else "Y-error"
                        if error_node == VertexType.ErrorY
                        else "Z-error"
                    )
                if i in correction_support:
                    corection_node = (
                        VertexType.CorrectionX
                        if correction_support[i] == pauli.Factor.X
                        else VertexType.CorrectionY
                        if correction_support[i] == pauli.Factor.Y
                        else VertexType.CorrectionZ
                    )
                    x_offset, y_offset = self.frame_offsets[corection_node]
                    nodes[corection_node]["x"].append(node.pos.x + x_offset)
                    nodes[corection_node]["y"].append(node.pos.y + y_offset)
                    nodes[corection_node]["hover"].append(
                        "X-correction"
                        if corection_node == VertexType.CorrectionX
                        else "Y-correction"
                        if corection_node == VertexType.CorrectionY
                        else "Z-correction"
                    )
            # For ancillas instead, we need to check whether they are toggled nodes
            elif (ancilla := i - self.code.num_data_qubits) in self.graph.primal:
                vertex_type = VertexType.Primal
                hover = f"Qubit #{i} - primal"
                if syndrome is not None and syndrome[ancilla]:
                    vertex_type = VertexType.PrimalToggled
                    hover += " toggled"
            elif ancilla in self.graph.dual:
                vertex_type = VertexType.Dual
                hover = f"Qubit #{i} - dual"
                if syndrome is not None and syndrome[ancilla]:
                    vertex_type = VertexType.DualToggled
                    hover += " toggled"
            else:
                raise ValueError(
                    f"Node #{i} is neither a data, primal, nor dual qubit."
                )
            nodes[vertex_type]["x"].append(node.pos.x)
            nodes[vertex_type]["y"].append(node.pos.y)
            nodes[vertex_type]["hover"].append(hover)

        if grey:
            styles = {
                VertexType.Data: self.vertex_kw_grayed_out[VertexType.Data],
                VertexType.Primal: self.vertex_kw_grayed_out[VertexType.Primal],
                VertexType.Dual: self.vertex_kw_grayed_out[VertexType.Dual],
            }
        else:
            styles = {
                VertexType.Data: self.vertex_kw[VertexType.Data],
                VertexType.Primal: self.vertex_kw[VertexType.Primal],
                VertexType.Dual: self.vertex_kw[VertexType.Dual],
            }
        for vertex_type in [
            VertexType.ErrorX,
            VertexType.ErrorY,
            VertexType.ErrorZ,
            VertexType.CorrectionX,
            VertexType.CorrectionY,
            VertexType.CorrectionZ,
            VertexType.PrimalToggled,
            VertexType.DualToggled,
        ]:
            styles[vertex_type] = self.vertex_kw[vertex_type]

        if self.error_data is not None and error_mechanism is not None:
            styles[VertexType.Data]["marker"] = dict(
                colorscale="Viridis",
                color=[
                    self.error_data["pauli"][i][error_mechanism]
                    for i in self.code.data_qubit_indices
                ],
                symbol="circle",
                size=15,
                colorbar=dict(thickness=20, title="Error Probs.", x=-0.2),
            )

        # Now actually add all the always-present nodes to the figure
        for node_type in [
            VertexType.Data,
            VertexType.Primal,
            VertexType.Dual,
        ]:
            fig.add_trace(
                go.Scatter(
                    x=nodes[node_type]["x"],
                    y=nodes[node_type]["y"],
                    mode="markers",
                    hovertext=nodes[node_type]["hover"],
                    **styles[node_type],
                )
            )

        # Finally, if any modifiers were present, draw them
        for modifier_type in [
            VertexType.ErrorX,
            VertexType.ErrorY,
            VertexType.ErrorZ,
            VertexType.CorrectionX,
            VertexType.CorrectionY,
            VertexType.CorrectionZ,
            VertexType.PrimalToggled,
            VertexType.DualToggled,
        ]:
            fig.add_trace(
                go.Scatter(
                    x=nodes[modifier_type]["x"],
                    y=nodes[modifier_type]["y"],
                    mode="markers",
                    hovertext=nodes[modifier_type]["hover"],
                    **styles[modifier_type],
                )
            )

        return fig


class CircuitVisualizer:
    """Visualiser for quant circuits.

    Notes:
        The circuit visualiser currently is a very thin wrapper around the
        ``'mpl'`` backend from ``qiskit``.
    """

    def __init__(self, circuit: circuit.Circuit):
        """Load a circuit for visualisation purposes.

        Notes:
            Qiskit can draw OpenQASM 3.0 circuits, but the header we use in our
            :func:`.convert_to_openqasm` is for OpenQASM 2.0. The visualiser
            automatically strips the 2.0 header and substitutes the 3.0 one,
            otherwise circuits would not render.

        Args:
            circuit: a :class:`~.circuit.Circuit` to draw.
        """
        qsm = openqasm.convert_to_openqasm(circuit).split("\n")
        qsm[0] = "OPENQASM 3.0;"
        qsm[1] = 'include "stdgates.inc";'
        qsm = "\n".join(qsm)
        self._circuit: qiskit.circuit.quantumcircuit.QuantumCircuit = qasm3.loads(qsm)

    def draw_circuit(self):
        """Draw a previously-loaded circuit with the Qiskit matplotlib drawer."""
        return self._circuit.draw("mpl")
