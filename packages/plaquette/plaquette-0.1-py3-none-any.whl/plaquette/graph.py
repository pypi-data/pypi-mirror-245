"""Pydantic models for the visualizer objects.

The visualizer is based on Web technologies, and as such it uses a
huge amount of JSON for data interchange. This data needs to match
what the JS side of things expect and to do this we use Pydantic
to make proper JSON Schema documents to ease development.

In a future in which plaquette can be driven via API calls to a remote
service, this would also help data exchange between a client and a
server running plaquette.
"""
import typing as t

import numpy as np
import pydantic


class Position(pydantic.BaseModel):
    """Qubit position in 3D space.

    For foliated codes, ``Z`` is the "time" direction.
    """

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other):
        """Add two vectors component-wise."""
        if not isinstance(other, Position):
            raise TypeError("only Position objects can be added")
        return Position(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __mul__(self, other):
        """Multiply a vector with a scalar."""
        return Position(x=self.x * other, y=self.y * other, z=self.z * other)

    def __sub__(self, other):
        """Subtract two vectors component-wise."""
        if not isinstance(other, Position):
            raise TypeError("only Position objects can be subtracted")
        return Position(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __truediv__(self, other):
        """Divide a vector with by scalar."""
        return Position(x=self.x / other, y=self.y / other, z=self.z / other)

    def __iter__(self):
        """Support unpacking vector components."""
        return iter((self.x, self.y, self.z))

    def unit(self):
        """Normalise a vector.

        Raises:
            ValueError: if you try to normalise the null-vector.
        """
        if norm := np.sqrt(self.x**2 + self.y**2 + self.z**2):
            return self / norm
        raise ValueError("null-vector cannot be normalised")


class Node(pydantic.BaseModel):
    """Node properties."""

    pos: t.Optional[Position]
    """Position w.r.t. the origin of the graph."""
    type: str
    """Type of node, for styling purposes.

    This is a free-form "tag", which can be used to select/filter a
    group of nodes out of a graph.
    """


class Edge(pydantic.BaseModel):
    """An edge between nodes."""

    a: int
    """The index of the first node in the list of the graph nodes."""
    b: int
    """The index of the second node in the list of the graph nodes."""
    type: str
    """Type of edge, for styling purposes.

    This is a free-form "tag", which can be used to select/filter a
    group of edges out of a graph.
    """

    def __iter__(self):
        """Support unpacking edge nodes."""
        return iter((self.a, self.b))


class BaseGraph(pydantic.BaseModel):
    """Dictionary schema to serialize a graph."""

    nodes: list[Node]
    """All nodes making up this graph."""
    edges: list[Edge]
    """All edges making up this graph."""
    _adjacency_matrix: np.ndarray
    """Adjacency matrix of the graph."""
    _incidence_matrix: np.ndarray
    """Incidence matrix of the graph."""

    def __init__(self, nodes: t.Sequence[Node], edges: t.Sequence[Edge], **kwargs):
        """Build a basic graph from just its ``nodes`` and ``edges``.

        .. important::

            **Do not** edit the :attr:`nodes` and :attr:`edges` attributes after
            instantiating a class instance. Internally, this class keeps an adjacency
            and incidence matrices, which are not updated if you change those
            attributes manually.
        """
        super().__init__(nodes=nodes, edges=edges, **kwargs)
        n_nodes = len(nodes)
        n_edges = len(edges)
        adjmat = np.zeros((n_nodes, n_nodes))
        incmat = np.zeros((n_edges, n_nodes))
        for i, edge in enumerate(self.edges):
            adjmat[edge.a][edge.b] = 1
            adjmat[edge.b][edge.a] = 1
            incmat[i][edge.a] = 1
            incmat[i][edge.b] = 1
        self._adjacency_matrix = adjmat
        self._incidence_matrix = incmat

    @property
    def n_nodes(self):
        """Get the number of nodes in the graph."""
        return len(self.nodes)

    @property
    def n_edges(self):
        """Get the number of edges in the graph."""
        return len(self.edges)

    def neighbours_of(self, node: int) -> t.Sequence[int]:
        """Returns the indices of the neighbouring nodes of ``node``.

        Args:
            node: the node whose neighbours you want.
        """
        return np.flatnonzero(self._adjacency_matrix[node])

    def nodes_connected_by(self, edge: int) -> t.Sequence[int]:
        """Indices of the nodes connected by the edge of index ``edge``.

        You can achieve the same with
        ``(BaseGraph.edges[edge].a, BaseGraph.edges[edge].b)``.
        """
        return np.flatnonzero(self._incidence_matrix[edge])

    def edges_incident_on(self, node: int) -> t.Sequence[int]:
        """All edges touching/incident on ``node``."""
        return np.flatnonzero(self._incidence_matrix[:, node])


class TannerGraph(BaseGraph):
    """The graph linking checks/ancillas and data qubits in a QEC code."""

    checks: list[list[int]] | None
    """List of edges forming a single "check".

    The outer list is the list of all checks. Each check is defined
    by a list of integers referring to edges connecting the ancilla
    of the check and the related data qubits.
    """
    primal: list[int] | None
    """List of checks belonging to the primal component of the graph."""
    dual: list[int] | None
    """List of checks belonging to the dual component of the graph."""


class CodeGraph(TannerGraph):
    """A graph of a QEC code."""

    logical_surfaces: list[list[int]] | None
    """List of nodes making up a "logical surface".

    A logical surface is a line in a 2D code or a real surface in a 3D
    graph that has a particular meaning in the represented graph.
    Usually this is the logical operator(s) in a 2D code graph or the
    correlation surface(s) in a FBQC graph.

    In general, these can be "interesting" sets of nodes that for some
    reason one would want to highlight.
    """


class DecodingGraph(BaseGraph):
    """A decoding graph."""

    selection: list[int]
    """The edges being selected from a decoder."""
    faults: list[int]
    """The nodes that have been "flipped" by errors."""
    virtual_nodes: list[int]
    """Indices of those nodes which have been artificially added for parity.

    The indices in this list should refer to the list of :attr:`~.BaseGraph.nodes`.
    """
    weights: list[float]
    """The weight of each node in a decoding algorithm.

    This can in principle be any valid float value, but not all decoders
    support all values, and conversion might be done by specific decoder
    classes.

    Each list item is the weight of the edge with corresponding index.
    """
    logical_surfaces: list[list[int]] | None
    """List of nodes making up a "logical surface".

    A logical surface is a line in a 2D code or a real surface in a 3D
    graph that has a particular meaning in the represented graph.
    Usually this is the logical operator(s) in a 2D code graph or the
    correlation surface(s) in a FBQC graph.

    In general, these can be "interesting" sets of nodes that for some
    reason one would want to highlight.
    """

    syndrome: list[int] | None
    """List of nodes which make the last decoded syndrome."""

    erasure: list[int] | None
    """List of edge indices which have been marked as erased."""


def center_of_mass(
    points: t.Sequence[Position], masses: t.Sequence[int] | None = None
) -> Position:
    """Calculate the center of mass among the given points.

    Args:
        points: the position where the objects are.
        masses: mass of each object. If ``None``, it will assume a mass
            of 1 for each object. Should be integers.
    """
    if masses is None:
        masses = np.ones(len(points), dtype=int)
    if len(masses) != len(points):
        raise ValueError("Points and masses arrays must be of same length")

    return np.sum(np.array(points) * np.array(masses)) / np.sum(masses)
