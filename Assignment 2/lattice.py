"""
Helper for computing stochastic lattices
for binomial interest rate model
"""

from typing import Union

from colorama import Fore, Style


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

    def set_value(self, value: float) -> None:
        self.value = value

    def set_children(self, children: list["Node"]) -> None:
        self.children = children

    def add_child(self, child: "Node") -> None:
        self.children.append(child)


class BinNode(Node):
    def __init__(
        self,
        value: float,
        depth: int,
        parent: Union["BinNode", None],
        up: Union["BinNode", None],
        down: Union["BinNode", None],
    ) -> None:
        """
        Initialize a binomial node with a value and children

        :param value: the value of the node
        :param up: the value of the up child
        :param down: the value of the down child

        :return: None
        """

        children = [up, down]

        super().__init__(value, depth, children)

        self.parent = parent

        self.up = up
        self.down = down

    def __repr__(self) -> str:
        return f"BinNode({self.value:.2f}, {self.depth})"

    def get_parent(self) -> Union["BinNode", None]:
        return self.parent

    def get_up(self) -> Union["BinNode", None]:
        return self.up

    def get_down(self) -> Union["BinNode", None]:
        return self.down

    def set_up(self, up: "BinNode") -> None:
        if self.up is not None:
            # Need to remove the old up node from the children

            try:
                self.children.remove(self.up)
            except ValueError:
                print(f"{Fore.RED}Error: up node not in children{Style.RESET_ALL}")

        self.up = up

    def set_down(self, down: "BinNode") -> None:
        if self.down is not None:
            # Need to remove the old down node from the children

            try:
                self.children.remove(self.down)
            except ValueError:
                print(f"{Fore.RED}Error: down node not in children{Style.RESET_ALL}")

        self.down = down


class Lattice:
    def __init__(self, head_node: BinNode) -> None:
        self.head_node = head_node

        self.depth = 1

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
                up_child = node.get_up()
                down_child = node.get_down()

                if up_child is not None:
                    new_nodes.append(up_child)

                if down_child is not None:
                    new_nodes.append(down_child)

            nodes = new_nodes

        return nodes

    def construct_bin_lattice(
        self, up_factor: float, down_factor: float, depth: int
    ) -> None:
        """
        Construct a binomial lattice

        :param up_factor: the factor to multiply by for an up move
        :param down_factor: the factor to multiply by for a down move
        :param depth: the depth of the lattice

        :return: None
        """

        self.depth = depth

        current_level_nodes = [self.head_node]

        for i in range(depth):
            next_level_nodes = []

            for parent_node in current_level_nodes:
                up_value = parent_node.get_value() * up_factor
                down_value = parent_node.get_value() * down_factor

                up_node = BinNode(up_value, i + 1, parent_node, None, None)
                down_node = BinNode(down_value, i + 1, parent_node, None, None)

                parent_node.set_up(up_node)
                parent_node.set_down(down_node)

                next_level_nodes += [up_node, down_node]

            # Reset the current level nodes to the next level nodes
            current_level_nodes = next_level_nodes

    def __repr__(self) -> str:
        """
        Prints the lattice in a readable format
        """

        def num_nodes_at_depth(depth: int) -> int:
            """
            Compute the number of nodes at a certain depth
            """

            return 2 ** (depth - 1)

        def compute_left_padding(tree_depth: int, current_depth: int) -> int:
            """
            Compute the left padding for a node at a certain depth
            """

            NODE_SPACE = 17 + 2 * (2 + 1) - 2
            num_nodes_bottom = num_nodes_at_depth(tree_depth)
            num_nodes_current = num_nodes_at_depth(current_depth)

            bottom_width = NODE_SPACE * num_nodes_bottom
            current_width = NODE_SPACE * num_nodes_current

            return int((bottom_width - current_width) // 2)

        lattice_str = ""

        for level in range(self.depth):
            level_nodes = self.get_nodes_at_depth(level)
            if len(level_nodes) == 0:
                break
            left_padding = compute_left_padding(self.depth, level + 1)
            lattice_str += " " * left_padding
            lattice_str += "| "
            for node in level_nodes:
                lattice_str += node.__repr__() + " | "

            lattice_str += " " * left_padding
            if level < self.depth - 1:
                lattice_str += "\n"

        return lattice_str


def main():
    head_node = BinNode(1, 0, None, None, None)
    lattice = Lattice(head_node)

    lattice.construct_bin_lattice(2, 0.5, 3)

    print(lattice)


if __name__ == "__main__":
    main()
