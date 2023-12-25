from common import *
import networkx


class Node:
    def __init__(
        self,
        name : str,
    ) -> None:
        self.name = name
        self.connections = set()

    def connect(
        self,
        node
    ) -> None:
        self.connections.add(node)
        return self

    def __repr__(
        self
    ) -> str:
        return f'<node : {self.name}>'


def __nodes(data : str) -> dict[str, Node]:
    nodes : dict[str, Node] = {}

    for line in data.splitlines():
        node, connections = line.split(': ')
        connections = connections.split(' ')

        if node in nodes:
            node = nodes[node]
        else:
            nodes[node] = node = Node(node)

        for connection in connections:
            if connection in nodes:
                connection = nodes[connection]
            else:
                nodes[connection] = connection =  Node(connection)

            node.connect(connection)
            connection.connect(node)

    return nodes


def __key(a : Node, b : Node) -> (Node, Node):
    return tuple(sorted([a, b], key=lambda n: n.name))


@challenge
def challenge_25_1(data : str) -> int:
    #
    # thinking:
    #
    # If I am being honest, I have _no_ clue how to solve this. Really
    # interesting problem, but no clue.
    #
    # My first inclination is to graph all of the conenctions then find
    # the two furthest nodes, marking those as left / right. From there
    # collect all of the nodes into either left or right (How? I'm not
    # sure), then check for nodes that have a single connection to the
    # other group, severing that conenction. This could possibly be
    # iterated from top to bottom for distance.
    #
    # Okay... Very clearly not. I decided to try this approach for the
    # actual input and it is taking quite a long time to even just
    # calculate the distances between nodes. I've been able to write
    # this entire paragraph out and it still hasn't stopped. It's still
    # going... Yup.... Taking a while. Managed to watch an explainer
    # video and still didn't finish.

    result : int = 0

    nodes : dict[str, Node] = __nodes(data)

    distances : dict[(Node, Node), int] = {}

    for node in nodes.values():
        for connection in node.connections:
            distances[__key(node, connection)] = 1

        distances[__key(node, node)] = 0

    for i in nodes.values():
        for j in nodes.values():
            for k in nodes.values():
                ij = distances.get(__key(i, j), math.inf)
                ik = distances.get(__key(i, k), math.inf)
                kj = distances.get(__key(k, j), math.inf)

                if ij > ik + kj:
                    distances[__key(i, j)] = ik + kj

    distances = sorted(
        [(*k, v) for k, v in distances.items()],
        key=lambda check: -check[-1],
    )

    print(*distances, sep='\n')

    return result


@challenge
def challenge_25_2(data : str) -> int:#
    result : int = 0

    return result
