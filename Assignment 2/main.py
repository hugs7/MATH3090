import bond


def main():
    T = 3
    n = 2
    y = 0.09
    c = 0.08
    F = 100_000

    present_values = bond.present_values_coupon_bearing_bond_discrete(F, T, c, y, n)

    print(present_values)

    print("The present value of the bond is: ", sum(present_values))

    print("Bond duration")

    bond_duration = bond.bond_duration_discrete(F, T, c, y, n)

    print("The bond duration is: ", bond_duration)

    # Bond value at |D|

    val_at_d = bond.bond_value_at_time(bond_duration, F, T, c, y, n)

    print("The bond value at |D| is: ", val_at_d)

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

    print(f"forward: {forward_rates}")


if __name__ == "__main__":
    main()
