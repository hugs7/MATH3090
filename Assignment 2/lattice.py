"""
Helper for computing stochastic lattices
for binomial interest rate model
"""

from typing import List, Union
from colorama import Fore, Style

import bond


class Node:
    """
    Defines a node in a lattice
    """

    def __init__(self, value: float, depth: int, children: list["Node"]) -> None:
        """
        Initialise a node with a value and children

        Args:
            value: the value of the node
            depth: the depth of the node indexed from 0
            children: the children of the node

        Returns:
            None
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
        Initialise a binomial node with a value and children

        Args:
            value: the value of the node
            depth: the depth of the node indexed from 0
            parent: the parent of the node
            up: the up child of the node
            down: the down child of the node

        Returns:
            None
        """

        children = [up, down]

        super().__init__(value, depth, children)

        self.parent = parent

        self.up = up
        self.down = down

        if up is not None:
            # Set the parent of the up node to be this node
            up.set_parent(self)

        if down is not None:
            # Set the parent of the down node to be this node
            down.set_parent(self)

    def __eq__(self, other: "BinNode") -> bool:
        if other is None:
            return False

        return self.value == other.value and self.depth == other.depth

    def __repr__(self) -> str:
        return f"{self.value:.5f}"

    def __copy__(self) -> "BinNode":
        node_value_copy = self.value
        node_depth_copy = self.depth
        node_up_copy = self.up.__copy__() if self.up is not None else None
        node_down_copy = self.down.__copy__() if self.down is not None else None

        node_copy = BinNode(
            node_value_copy, node_depth_copy, None, node_up_copy, node_down_copy)

        return node_copy

    def get_parent(self) -> Union["BinNode", None]:
        return self.parent

    def get_up(self) -> Union["BinNode", None]:
        return self.up

    def get_down(self) -> Union["BinNode", None]:
        return self.down

    def set_parent(self, parent: "BinNode") -> None:
        self.parent = parent

    def set_children(self, children: list["Node"]) -> None:
        super().set_children(children)

        # Also set the up and down children
        if len(children) == 2:
            self.up = children[0]
            self.down = children[1]

        else:
            self.up = None
            self.down = None

    def set_up(self, up: "BinNode") -> None:
        if self.up is not None:
            # Need to remove the old up node from the children

            try:
                self.children.remove(self.up)
            except ValueError:
                print(f"{Fore.RED}Error: up node not in children{Style.RESET_ALL}")

        self.up = up

        # Add the new up node to the children
        self.children.append(up)

    def set_down(self, down: "BinNode") -> None:
        if self.down is not None:
            # Need to remove the old down node from the children

            try:
                self.children.remove(self.down)
            except ValueError:
                print(f"{Fore.RED}Error: down node not in children{Style.RESET_ALL}")

        self.down = down

        # Add the new down node to the children
        self.children.append(down)


class BinLattice:
    def __init__(self, head_node: BinNode, depth: int = 0) -> None:
        self.head_node = head_node

        self.depth = depth

        # generate dummy bin node to compute the length of it's string representation
        # to determine the spacing between nodes

        dummy_up_child = BinNode(0, 1, None, None, None)
        dummy_down_child = BinNode(0, 1, None, None, None)
        dummy_node = BinNode(0, 0, None, dummy_up_child, dummy_down_child)

        self.separator = " | "
        self.NODE_SPACE = len(dummy_node.__repr__()) + len(self.separator)

        self.up_factor = None
        self.down_factor = None

    def get_head_node(self) -> BinNode:
        return self.head_node

    def get_depth(self) -> int:
        """
        Get the depth of the lattice

        Returns:
            The depth of the lattice
        """

        return self.depth

    def get_nodes_at_depth(self, depth: int) -> list[BinNode]:
        """
        Get all nodes at a certain depth

        Args:
            depth: the depth to get the nodes at, indexed from 0

        Returns:
            A list of nodes at the specified depth
        """

        nodes = [self.head_node]

        if depth == 0:
            return nodes

        for d in range(depth):
            new_nodes = []
            for node in nodes:
                down_child = node.get_down()
                up_child = node.get_up()

                if down_child is not None and down_child not in new_nodes:
                    new_nodes.append(down_child)

                if up_child is not None and up_child not in new_nodes:
                    new_nodes.append(up_child)

            nodes = new_nodes

        return nodes

    @staticmethod
    def get_num_nodes_at_depth(depth: int) -> int:
        """
        Get the number of nodes at a certain depth

        Args:
            depth: the depth to get the number of nodes at, indexed from 0

        Returns:
            The number of nodes at the specified depth
        """

        return 2 ** depth

    def construct_bin_lattice(
        self, up_factor: float, down_factor: float, depth: int
    ) -> None:
        """
        Construct a binomial lattice

        Args:
            up_factor: the factor to multiply the parent node value by to get the up child value
            down_factor: the factor to multiply the parent node value by to get the down child value
            depth: the depth of the lattice

        Returns:
            None
        """

        self.depth = depth
        self.up_factor = up_factor
        self.down_factor = down_factor

        current_level_nodes = [self.head_node]

        for i in range(depth + 1):
            if i == depth:
                # If we are at the last level, we don't need to create any children
                break

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

    def check_path(self, path: Union[str, list[str]]) -> bool:
        """
        Checks a path of a list of strings or string of 'u' and 'd's.

        Args:
            path: the path to check as a list of strings or a string

        Returns:
            True if the path is valid, False otherwise
        """

        for step in path:
            if step not in ["u", "d"]:
                return False

        return True

    def get_node_by_path(self, path: Union[str, list[str]]) -> BinNode:
        """
        Get the forward rate given a path (e.g. ['u', 'd', 'u']
        or "udu", etc.)

        Args:
            path: the path to check as a list of strings or a string

        Returns:
            The forward rate at the end of the path as BinNode
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

        return current_node

    def spot_rate_from_path(self, path: Union[str, list[str]]) -> float:
        """
        Computes the price, P of a zero coupon bond maturing at len(path) given a path

        Args:
            path: the path to check as a list of strings or a string

        Returns:
            The price of the zero coupon bond at the end of the path
        """

        node = self.get_node_by_path(path)

        return bond.price_zero_coupon_bond_leaf(node.get_value())

    def get_lattice_subtree(self, depth: int) -> "BinLattice":
        """
        Gets a subtree of the lattice with a certain depth

        Args:
            depth: the depth of the subtree indexed from 0

        Returns:
            A new lattice with the subtree
        """

        if depth < 0 or depth > self.depth:
            print(
                f"{Fore.RED}Invalid depth. Depth must be in the range [0, {self.depth}].{Style.RESET_ALL}")
            return None

        # Create copy of tree
        lattice_copy = BinLattice(self.head_node)

        # Recreate the lattice up to the specified depth
        lattice_copy.construct_bin_lattice(
            self.up_factor, self.down_factor, depth)

        return lattice_copy

    def construct_p_lattice(self, future_time_period: int, up_pr: float, down_pr: float) -> "BinLattice":
        """
        Constructs a new lattice such that the head node is P_{0, future_time_period} 
        with the forward rates given the current lattice of zero spot rates

        Args:
            future_time_period: int
                The upper bound / period to construct the zero spot lattice for. E.g.
                if 4 is passed, the head node of the newly constructed lattice
                will be y_{0, 4}
            up_pr: float
                The probability of an up move within the binomial model
            down_pr: float
                The probability of a down move within the binomial model

        Returns:
            A new lattice with P values
        """

        if future_time_period < 0 or future_time_period > self.depth:
            print(
                f"{Fore.RED}Invalid forward time period. Forward time period must be in the range [0, {self.depth}].{Style.RESET_ALL}")
            return None

        # Get subtree of the lattice up to the forward time period
        leaf = future_time_period - 1
        lattice_subtree = self.get_lattice_subtree(leaf)

        # Construct new lattice bottom up just by replacing the values of the nodes
        # as we go

        # First take a copy of the subtree
        p_lattice = lattice_subtree.__copy__()
        # At this stage the lattice is still the forward lattice and
        # below it will be converted to the p lattice

        depth = leaf

        while depth >= 0:
            if depth == leaf:
                # Leaf case
                # All 1s for the first level of the p lattice
                leaf_num_nodes = BinLattice.get_num_nodes_at_depth(depth+1)
                p_lattice_prev_level_nodes = [
                    BinNode(1, leaf, None, None, None) for _ in range(leaf_num_nodes)]
            else:
                # Recursive case
                # Get the previous level of the p lattice
                p_lattice_prev_level_nodes = p_lattice.get_nodes_at_depth(
                    depth + 1)

            # Get nodes at current level from forward lattice
            forward_lattice_nodes = lattice_subtree.get_nodes_at_depth(depth)

            for i, forward_node in enumerate(forward_lattice_nodes):
                forward_rate = forward_node.get_value()

                # zero coupon bond price is the expected value of the two child nodes
                p_down_node = p_lattice_prev_level_nodes[i]
                p_up_node = p_lattice_prev_level_nodes[i + 1]

                p_down_rate = p_down_node.get_value()
                p_up_rate = p_up_node.get_value()

                bond_price = bond.price_zero_coupon_bond(
                    forward_rate, p_up_rate, p_down_rate, up_pr, down_pr)

                new_node = BinNode(bond_price, depth, None,
                                   p_up_node, p_down_node)

                # Update the p lattice with the newly computed node (p value)
                p_lattice.set_node_at_depth_and_index(depth, i, new_node)

            # Move to the next level up in the lattice
            depth -= 1

        # At this point, new_nodes should contain only the head node
        # of the new lattice

        return p_lattice

    def set_node_at_depth_and_index(self, depth: int, index: int, node: BinNode) -> None:
        """
        Set a node at a certain depth and index

        Args:
            depth: the depth to set the node at, indexed from 0
            index: the index to set the node at, indexed from 0
            node: the node to set

        Returns:
            None
        """

        if depth < 0 or depth > self.depth:
            print(
                f"{Fore.RED}Invalid depth. Depth must be in the range [0, {self.depth}].{Style.RESET_ALL}")
            return

        if index < 0 or index >= BinLattice.get_num_nodes_at_depth(depth):
            print(
                f"{Fore.RED}Invalid index. Index must be in the range [0, {BinLattice.get_num_nodes_at_depth(depth)}).{Style.RESET_ALL}")
            return

        nodes = self.get_nodes_at_depth(depth)

        # Update this node's parent's children
        parent = nodes[index].get_parent()
        if parent is not None:
            # Determine if this node is the up or down child of the parent
            if parent.get_up() == nodes[index]:
                parent.set_up(node)
            else:
                parent.set_down(node)
        else:
            # We are updating the head node
            self.head_node = node

    def __copy__(self) -> "BinLattice":
        """
        Copy the lattice

        Returns:
            A copy of the lattice
        """

        head_node_copy = self.head_node.__copy__()

        lattice_copy = BinLattice(head_node_copy, depth=self.depth)

        return lattice_copy

    def __repr__(self) -> str:
        """
        Prints the lattice in a readable format
        """

        def num_nodes_at_depth(depth: int) -> int:
            """
            Compute the number of nodes at a certain depth

            Args:
                depth: the depth to compute the number of nodes at, indexed from 0
            """

            return depth + 1

        def compute_left_padding(tree_depth: int, current_depth: int) -> int:
            """
            Compute the left padding for a node at a certain depth
            """

            num_nodes_bottom = num_nodes_at_depth(tree_depth)
            num_nodes_current = num_nodes_at_depth(current_depth)

            bottom_width = self.NODE_SPACE * \
                num_nodes_bottom
            current_width = self.NODE_SPACE * \
                num_nodes_current

            diff = bottom_width - current_width
            half_diff = int(diff // 2)

            if current_depth == tree_depth:
                return half_diff
            else:
                return half_diff + len(self.separator)

        lattice_str = ""

        for level in range(self.depth + 1):
            level_nodes = self.get_nodes_at_depth(level)
            if len(level_nodes) == 0:
                break
            left_padding = compute_left_padding(self.depth, level)
            lattice_str += " " * left_padding
            lattice_str += self.separator
            for node in level_nodes:
                lattice_str += node.__repr__() + self.separator

            lattice_str += " " * left_padding
            lattice_str += "\n"

        return lattice_str


def main():
    p = 0.6
    q = 1 - p

    head_node = BinNode(1, 0, None, None, None)
    lattice = BinLattice(head_node)

    lattice.construct_bin_lattice(2, 0.5, 5)

    print(lattice)

    print("-"*100)

    zero_spot_lattice = lattice.construct_p_lattice(3, p, q)

    print("ZERO SPOT LATTICE")
    print(zero_spot_lattice)


if __name__ == "__main__":
    main()
