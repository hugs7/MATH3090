"""
Helper for computing stochastic lattices
for binomial interest rate model
"""


class Node:
    """
    Defines a node in a lattice
    """

    def __init__(self, value: float, depth: int, children: list["Node"]) -> None:
        """
        Initialize a node with a value and children

        :param value: the value of the node
        :param children: the children of the node

        :return: None
        """

        self.value = value
        self.depth = depth

        self.children = children

    def get_value(self) -> float:
        return self.value

    def get_children(self) -> list["Node"]:
        return self.children


class BinNode(Node):
    def __init__(self, value: float, depth: int, up: float, down: float) -> None:
        """
        Initialize a binomial node with a value and children

        :param value: the value of the node
        :param up: the value of the up child
        :param down: the value of the down child

        :return: None
        """

        children = [up, down]

        super().__init__(value, depth, children)

        self.up = up
        self.down = down

    def get_up(self) -> Node:
        return self.up

    def get_down(self) -> Node:
        return self.down


class Lattice:
    def __init__(self, head_node: BinNode) -> None:
        self.head_node = head_node

    def get_head_node(self) -> Node:
        return self.head_node

    def get_nodes_at_depth(self, depth: int) -> list[Node]:
        """
        Get all nodes at a certain depth

        :param depth: the depth to get nodes at

        :return: list of nodes at that depth
        """

        nodes = [self.head_node]

        for _ in range(depth):
            new_nodes = []
            for node in nodes:
                new_nodes += node.get_children()

            nodes = new_nodes

        return nodes
