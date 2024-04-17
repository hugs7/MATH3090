import bond
import swap
from lattice import BinNode, BinLattice
import table
import display as dsp
from IPython.display import Markdown, display, Latex
from colorama import Fore, Style


def bonds():
    T = 3
    n = 2
    y = 0.09
    c = 0.08
    F = 100_000

    present_values = bond.present_values_coupon_bearing_bond_discrete(
        F, T, c, y, n)

    print("Present values", present_values)

    print("The present value of the bond is: ", sum(present_values))

    print("Bond duration")

    bond_duration = bond.bond_duration_discrete(F, T, c, y, n)

    print("The bond duration is: ", bond_duration)

    # Bond value at |D|

    val_at_d = bond.bond_value_at_time(bond_duration, F, T, c, y, n)

    print("The bond value at |D| is: ", val_at_d)

    bond_prices = [
        99412,
        97339,
        94983,
        94801,
        94699,
        94454,
        93701,
        93674,
        93076,
        92814,
        91959,
        91664,
        87384,
        87329,
        86576,
        84697,
        82642,
        82350,
        82207,
        81725,
    ]

    num_bonds = 20
    assert (len(bond_prices) == num_bonds)
    F = 100_000
    c = 0.04
    n = 1  # annual
    T = [k for k in range(1, num_bonds + 1)]

    spot_rates, forward_rates = bond.recursive_zero_coupon_yield_continuous(
        bond_prices, F, T, c, n
    )

    table_data = []

    for i in range(len(T)):
        table_data.append([i, T[i], spot_rates[i], forward_rates[i]])

    # Yet to put this into nice table
    col_heads = ["Time Step", "Year", "Spot Rate", "Forward Rate"]
    col_spaces = [10, 6, 11, 14]
    col_decimals = [None, None, 5, 5]

    table_str = table.generate_table(
        col_heads, col_spaces, table_data, col_decimals)

    dsp.printmd(table_str)


def swaps():
    print("QUESTION 2b")
    bond_prices = [
        99412,
        97339,
        94983,
        94801,
        94699,
        94454,
        93701,
        93674,
        93076,
        92814,
        91959,
        91664,
        87384,
        87329,
        86576,
        84697,
        82642,
        82350,
        82207,
        81725,
    ]

    num_bonds = 20
    assert (len(bond_prices) == num_bonds)
    F = 100_000
    c = 0.04
    n = 1  # annual
    T = [k for k in range(1, num_bonds + 1)]

    spot_rates, forward_rates = bond.recursive_zero_coupon_yield_continuous(
        bond_prices, F, T, c, n
    )

    col_heads = ["Time Step", "Year", "Spot Rate", "Forward Rate"]
    col_spaces = [10, 6, 11, 14]
    col_decimals = [None, None, 5, 5]

    table_data = []

    for i in range(len(T)):
        table_data.append([i+1, T[i], spot_rates[i], forward_rates[i]])

    table_str = table.generate_table(
        col_heads, col_spaces, table_data, col_decimals)

    print("Spot rates")
    print(spot_rates)
    print("\n\nForward rates")
    print(forward_rates)


def strip_test():
    """
    Test of recursive zero coupon yield from book"""

    F = 100_000
    n = 2  # Semi annual

    maturity_periods = [0.5, 1, 1.5]
    bond_prices = [100961.54, 100_936.33, 100_272.84]
    c = 0.10
    expected_zero_yield_rates = [0.08, 0.09, 0.098]

    spot_rates, forward_rates = bond.recursive_zero_coupon_yield_continuous(
        bond_prices, F, maturity_periods, c, n
    )

    print(f"spot rates: {spot_rates}")
    print()
    print(f"forward rates: {forward_rates}")


def lattice():
    print("Question 3")

    # Maturity
    T = 3

    # zero spot yield rate for time step 0 to time step 1
    y_0_1 = 0.02

    # Probability of increase / decrease
    p = 0.6
    q = 1 - p

    # Increase / Decrease factors
    u = 1.3
    d = 0.9

    head_node = BinNode(y_0_1, 0, None, None, None)
    forward_lattice = BinLattice(head_node)

    forward_lattice.construct_bin_lattice(u, d, T)

    print(f"{Fore.GREEN}Forward lattice{Style.RESET_ALL}")
    print(forward_lattice)

    # Week 4 lecture 2
    path = ["u", "u"]

    rate_value = forward_lattice.get_node_by_path(path)
    print(f"Rate value at path {path}: {rate_value}")

    # Yield curve lattice
    print(f"{Fore.LIGHTMAGENTA_EX}Yield curve lattice{Style.RESET_ALL}")
    # y_{0, 2}
    T_y = 2
    yield_curve_lattice = forward_lattice.construct_zero_spot_lattice(
        T_y, p, q)

    print(f"{Fore.GREEN}y_{0, 2} yield curve lattice{Style.RESET_ALL}")
    print(yield_curve_lattice)
    # print(yield_curve_lattice.get_depth())
    print("----------------------------------")
    # y_{0, 3}
    # T_y = 3
    # yield_curve_lattice = forward_lattice.construct_zero_spot_lattice(
    #    T_y, p, q)

    # print(f"{Fore.GREEN}y_{0, 3} yield curve lattice{Style.RESET_ALL}")
    # print(yield_curve_lattice)


def main():
    bonds()

    # strip_test()

    # swaps()

    lattice()


if __name__ == "__main__":
    main()
