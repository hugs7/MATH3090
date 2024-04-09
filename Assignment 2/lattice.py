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
        if self.down and self.up:
            return f"({self.value:.4f}, {self.down.get_value():.4f}, {self.up.get_value():.4f})"
        else:
            return f"{self.value:.4f}"

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


class BinLattice:
    def __init__(self, head_node: BinNode) -> None:
        self.head_node = head_node

        self.depth = 1

        # generate dummy bin node to compute the length of it's string representation
        # to determine the spacing between nodes

        dummy_node = BinNode(1, 0, None, None, None)
        self.separator = " | "
        self.NODE_SPACE = len(dummy_node.__repr__()) + len(self.separator)

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
                down_child = node.get_down()
                up_child = node.get_up()

                if down_child is not None:
                    new_nodes.append(down_child)

                if up_child is not None:
                    new_nodes.append(up_child)

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
                down_value = parent_node.get_value() * down_factor
                up_value = parent_node.get_value() * up_factor

                down_node = BinNode(down_value, i + 1, parent_node, None, None)
                up_node = BinNode(up_value, i + 1, parent_node, None, None)

                parent_node.set_down(down_node)
                parent_node.set_up(up_node)

                next_level_nodes += [down_node, up_node]

            # Reset the current level nodes to the next level nodes
            current_level_nodes = next_level_nodes

    def check_path(self, path: list[str]) -> bool:
        """
        Checks a path of a list of strings of 'u' and 'd's.

        Returns:
            True if the path is valid, False otherwise
        """

        for step in path:
            if step not in ["u", "d"]:
                return False

        return True

    def get_forward_rate(self, path: list[str]) -> float:
        """
        Get the forward rate given a path (e.g. ['u', 'd', 'u']
        or ['u', 'u', 'd'], etc.)

        :param path: the path to the forward rate

        :return: the forward rate
        """

        # Check path
        if not self.check_path(path):
            print(f"{Fore.RED}Invalid path{Style.RESET_ALL}")
            return 0.0

        current_node = self.head_node

        for step in path:
            if step == "u":
                current_node = current_node.get_up()
            else:
                current_node = current_node.get_down()

        rate_value = current_node.get_value()

        return rate_value

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

            num_nodes_bottom = num_nodes_at_depth(tree_depth)
            num_nodes_current = num_nodes_at_depth(current_depth)

            bottom_width = self.NODE_SPACE * num_nodes_bottom
            current_width = self.NODE_SPACE * num_nodes_current

            return int((bottom_width - current_width) // 2)

        lattice_str = ""

        for level in range(self.depth):
            level_nodes = self.get_nodes_at_depth(level)
            if len(level_nodes) == 0:
                break
            left_padding = compute_left_padding(self.depth, level + 1)
            lattice_str += " " * left_padding
            lattice_str += self.separator
            for node in level_nodes:
                lattice_str += node.__repr__() + self.separator

            lattice_str += " " * left_padding
            if level < self.depth - 1:
                lattice_str += "\n"

        return lattice_str


def main():
    head_node = BinNode(1, 0, None, None, None)
    lattice = BinLattice(head_node)

    lattice.construct_bin_lattice(2, 0.5, 3)

    print(lattice)


if __name__ == "__main__":
    main()
