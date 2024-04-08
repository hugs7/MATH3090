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


if __name__ == "__main__":
    main()
