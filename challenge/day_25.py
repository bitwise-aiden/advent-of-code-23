from common import *
import networkx


@challenge
def challenge_25_1(data : str) -> int:
    graph = networkx.Graph()

    for line in data.splitlines():
        node, conenctions = line.split(': ')

        for connection in conenctions.split(' '):
            graph.add_edge(node, connection)
            graph.add_edge(connection, node)

    edges = networkx.minimum_edge_cut(graph)
    graph.remove_edges_from(edges)

    return math.prod(
        len(c)
        for c in networkx.connected_components(graph)
    )


@challenge
def challenge_25_2(data : str) -> int:
    # Yay don't have to do anything for this one.
    return 0
