import bond
import swap
from lattice import BinNode, BinLattice


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
    F = 100_000
    c = 0.04
    n = 1  # annual
    T = [k for k in range(1, num_bonds + 1)]

    spot_rates, forward_rates = bond.recursive_zero_coupon_yield_continuous(
        bond_prices, F, T, c, n
    )

    print(f"spot: {spot_rates}")
    print()
    print(f"forward: {forward_rates}")
    print()

    notional = 1_000_000
    fixed_rate = 0.065
    floating_spread = 0.01

    swap_values = swap.compute_swap_values(
        notional, T, n, spot_rates, forward_rates, fixed_rate, floating_spread
    )

    print(f"swap values: {swap_values}")
    print()

    sum_swap_values = sum(swap_values)

    print(f"sum of swap values: {sum_swap_values}")

    lb = 0.06
    ub = 0.07
    itv = 0.001

    eps = 10
    closest_sum_swap = None
    closest_fixed_rate = None

    while closest_sum_swap is None or closest_sum_swap > eps:
        fixed_rates = [lb + itv * k for k in range(int((ub - lb) / itv) + 1)]

        sum_swap_rates = []
        for fixed_rate in fixed_rates:
            swap_values = swap.compute_swap_values(
                notional, T, n, spot_rates, forward_rates, fixed_rate, floating_spread
            )
            sum_swap_values = sum(swap_values)

            sum_swap_rates.append(sum_swap_values)

        closest_index = -1
        for i, sum_swap in enumerate(sum_swap_rates):
            if closest_sum_swap is None or abs(sum_swap) < closest_sum_swap:
                closest_sum_swap = abs(sum_swap)
                closest_fixed_rate = fixed_rates[i]
                closest_index = i

        if closest_index >= 0:
            # if we didn't find a better rate, we need to make the interval more granular
            lb = fixed_rates[closest_index - 1]
            ub = fixed_rates[closest_index + 1]
        itv /= 2
        print(
            f"fixed rate: {closest_fixed_rate}, sum of swap values: {closest_sum_swap}"
        )

    print(
        f"FOUND: closest rate: {closest_fixed_rate}, sum of swap values: {closest_sum_swap}"
    )


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

    # Maturity (lattice / tree depth)
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

    print(forward_lattice)

    print("---")

    path = ["u", "u", "u"]

    rate_value = forward_lattice.get_node_by_path(path)
    print(f"Rate value at path {path}: {rate_value}")


def main():
    bonds()

    # strip_test()

    # swaps()

    # lattice()


if __name__ == "__main__":
    main()
