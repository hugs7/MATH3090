# Author: Hugo Burton
# Date: 18/04/2024


import math
import interest
from lattice import BinLattice

# ----- Zero Coupon Bonds -----


def price_zero_coupon_bond_discrete(
    face_value: int,
    years_to_maturity: int,
    interest_rate: float,
    compounding_frequency_yr: int,
):
    """
    Calculate the price of a zero coupon bond using discrete compound interest.

    Args:
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        interest_rate: float
            The yield rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        price: float
            The price of the bond.
    """

    beta = interest.discrete_compound_interest_discounted(
        interest_rate, years_to_maturity, compounding_frequency_yr
    )

    price = face_value * beta

    return price


def price_zero_coupon_bond_continuous(
    face_value: int, years_to_maturity: int, interest_rate: float
):
    """
    Calculate the price of a zero coupon bond using continuous compound interest.

    Args:
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        interest_rate: float
            The yield rate of the bond.

    Returns:
        price: float
            The price of the bond.
    """

    beta = interest.continuous_compound_interest_discounted(
        interest_rate, years_to_maturity
    )

    price = face_value * beta

    return price


def price_zero_coupon_bond_nonconstant_yield(
    face_value: int, years_to_maturity: int, yield_function
):
    """
    Calculate the price of a zero coupon bond with a nonconstant yield.

    Args:
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        yield_function: function
            A function that takes a single argument, the time to maturity, and returns the yield at that time.

    Returns:
        price: float
            The price of the bond.
    """

    price = face_value * interest.nonconstant_yield_discounted(
        yield_function, years_to_maturity
    )

    return price


# ----- Coupon Bearing Bonds -----


def price_coupon_bearing_bond_discrete(
    face_value: int,
    years_to_maturity: int,
    coupon_rate: float,
    interest_rate: float,
    compounding_frequency_yr: int,
):
    """
    Calculate the price of a coupon bearing bond using discrete compound interest.

    Args:
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        coupon_rate: float
            The annual coupon rate of the bond.
        interest_rate: float
            The yield rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        price: float
            The price of the bond.
    """

    # Define subfunction for computing the present value of the coupon payments
    def coupon_payment_present_value(
        coupon_rate_annual: float,
        interest_rate: float,
        compounding_frequency_yr: int,
        years_to_maturity: int,
    ):
        """
        Calculate the present value of the coupon payments of a bond.

        Args:
            coupon_rate_annual: float
                The annual coupon rate of the bond.
            face_value: int
                The face value of the bond.
            interest_rate: float
                The yield rate of the bond.
            compounding_frequency_yr: int
                The frequency at which the yield is compounded.
            years_to_maturity: int
                The number of years until the bond matures.

        Returns:
            payment_value: float
                The present value of the coupon payments of the bond.
        """

        coupon_rate_adjusted = coupon_rate_annual / compounding_frequency_yr

        numerator = 1 - interest.discrete_compound_interest_discounted(
            interest_rate, years_to_maturity, compounding_frequency_yr
        )

        denominator = interest_rate / compounding_frequency_yr

        payment_value = coupon_rate_adjusted * (numerator / denominator)

        return payment_value

    # Initialise the price
    price = 0

    # Calculate the annual coupon payment
    coupon_rate_annual = coupon_rate * face_value

    # Add the present value of the coupon payments
    coupon_value = coupon_payment_present_value(
        coupon_rate_annual, interest_rate, compounding_frequency_yr, years_to_maturity
    )
    price += coupon_value

    # Add the face value discounted to the present
    discounted_face_value = price_zero_coupon_bond_discrete(
        face_value, years_to_maturity, interest_rate, compounding_frequency_yr
    )
    price += discounted_face_value

    return price


def adjusted_coupon_rate(coupon_rate: float, compounding_frequency_yr: int) -> float:
    """
    Adjust the coupon rate to account for the compounding frequency.

    Args:
        coupon_rate: float
            The annual coupon rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        adjusted_coupon_rate: float
            The adjusted coupon rate.
    """

    adjusted_coupon_rate = coupon_rate / compounding_frequency_yr

    return adjusted_coupon_rate


def coupon_value(
    face_value: int, coupon_rate: float, compounding_frequency_yr: int
) -> float:
    """
    Calculate the value of a coupon payment.

    Args:
        face_value: int
            The face value of the bond.
        coupon_rate: float
            The annual coupon rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        coupon_value: float
            The value of the coupon payment.
    """

    adjusted_coup_rate = adjusted_coupon_rate(coupon_rate, compounding_frequency_yr)

    coupon_value = face_value * adjusted_coup_rate

    return coupon_value


def present_value_coupon_bearing_bond_discrete(
    time_step: int,
    face_value: int,
    years_to_maturity: int,
    coupon_rate: float,
    interest_rate: float,
    compounding_frequency_yr: int,
) -> float:
    """
    Calculate the present value of the coupon payments of a bond at a specific time step.

    Args:
        time_step: int
            The time step at which to calculate the present value. Time steps should be in the range [1, years_to_maturity * compounding_frequency_yr]
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        coupon_rate: float
            The annual coupon rate of the bond.
        interest_rate: float
            The yield rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        present_value: float
            The present value of the coupon payments of the bond at the specified time step.
    """

    if time_step < 1:
        raise ValueError("Time step must be greater than or equal to 1.")

    num_time_steps = years_to_maturity * compounding_frequency_yr

    adjusted_coupon_value = coupon_value(
        face_value, coupon_rate, compounding_frequency_yr
    )

    beta = interest.discrete_compound_interest_discounted_bond(
        interest_rate, time_step, compounding_frequency_yr
    )

    if time_step < num_time_steps:
        return adjusted_coupon_value * beta
    else:
        return (adjusted_coupon_value + face_value) * beta


def present_values_coupon_bearing_bond_discrete(
    face_value: int,
    years_to_maturity: int,
    coupon_rate: float,
    interest_rate: float,
    compounding_frequency_yr: int,
) -> list[float]:
    """
    Calculate the present values of the coupon payments of a bond at each time step.

    Args:
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        coupon_rate: float
            The annual coupon rate of the bond.
        interest_rate: float
            The yield rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        present_values: list[float]
            The present values of the coupon payments of the bond at each time step.
    """

    num_time_steps = years_to_maturity * compounding_frequency_yr

    present_values = [
        present_value_coupon_bearing_bond_discrete(
            time_step,
            face_value,
            years_to_maturity,
            coupon_rate,
            interest_rate,
            compounding_frequency_yr,
        )
        for time_step in range(1, num_time_steps + 1)
    ]

    return present_values


def bond_duration_discrete(
    face_value: int,
    years_to_maturity: int,
    coupon_rate: float,
    interest_rate: float,
    compounding_frequency_yr: int,
) -> float:
    """
    Calculate the duration of a bond with discrete interest.

    Args:
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        coupon_rate: float
            The annual coupon rate of the bond.
        interest_rate: float
            The yield rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        duration: float
            The duration of the bond.
    """

    duration = 0

    num_time_steps = years_to_maturity * compounding_frequency_yr

    B = sum(
        present_values_coupon_bearing_bond_discrete(
            face_value,
            years_to_maturity,
            coupon_rate,
            interest_rate,
            compounding_frequency_yr,
        )
    )

    for time_step in range(1, num_time_steps + 1):
        year = time_step / compounding_frequency_yr

        present_value_t = present_value_coupon_bearing_bond_discrete(
            time_step,
            face_value,
            years_to_maturity,
            coupon_rate,
            interest_rate,
            compounding_frequency_yr,
        )

        duration += (year * present_value_t) / B

    return duration


def bond_value_at_time(
    bond_duration: float,
    face_value: int,
    years_to_maturity: int,
    coupon_rate: float,
    interest_rate: float,
    compounding_frequency_yr: int,
) -> float:
    """
    Calculates the value of a bond at a specific time.

    Args:
        bond_duration: float
            The duration of the bond.
        face_value: int
            The face value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        coupon_rate: float
            The annual coupon rate of the bond.
        interest_rate: float
            The yield rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        bond_value: float
            The value of the bond at the specified time.
    """

    if bond_duration < 0 or bond_duration > years_to_maturity:
        raise ValueError("Bond duration must be in the range [0, years_to_maturity].")

    if compounding_frequency_yr < 1:
        raise ValueError("Compounding frequency must be a positive integer.")

    if interest_rate < 0 or interest_rate > 1:
        raise ValueError("Interest rate must be in the range [0, 1].")

    num_time_steps = years_to_maturity * compounding_frequency_yr

    # interest_adjusted = 1 + interest_rate
    coup_val = coupon_value(face_value, coupon_rate, compounding_frequency_yr)
    bond_value = 0

    # Coupons

    reinvestments = []

    for time_step in range(1, num_time_steps + 1):
        year = time_step / compounding_frequency_yr

        # Length of time this coupon can be reinvested for
        reinvestment_time = bond_duration - year

        cashflow = coup_val
        if time_step == num_time_steps:
            # Last coupon includes face value
            cashflow += float(face_value)

        beta = interest.discrete_compound_interest_accumulated_bond(
            interest_rate, reinvestment_time, compounding_frequency_yr
        )
        coupon_reinvestment_val = cashflow * beta

        print(
            f"Time step {time_step:<1}, Year {year:<1}, Cashflow: {cashflow:>8}, Beta:"
            + f"{beta:>8.4f}, Reinvestment value {coupon_reinvestment_val:>9.4f}"
        )

        reinvestments.append(coupon_reinvestment_val)

    print("-" * 50)

    bond_value = sum(reinvestments)

    return bond_value


# ---- Yield Curves ----


def spot_zero_coupon_yield_curve_continuous(
    face_value: int,
    present_value: float,
    years_to_maturity: int,
    spot_rates: list[float],
    coupon_rate: float,
    compounding_frequency_yr: int,
    checks: bool = True,
) -> float:
    """
    Computes the spot yield curve for a zero coupon bond using continuous compound interest.

    Args:
        face_value: int
            The face value of the bond.
        present_value: float
            The present value of the bond.
        years_to_maturity: int
            The number of years until the bond matures.
        spot_rates: list[float]
            A list of the spot rates up to but not including the current time step.
        coupon_rate: float
            The annual coupon rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        spot_yield: float
            The spot yield curve for the bond.
    """

    # Checks
    if checks:
        if years_to_maturity < 0:
            raise ValueError("Years to maturity must be non-negative.")

        if compounding_frequency_yr < 1:
            raise ValueError("Compounding frequency must be a positive integer.")

        if any(rate < 0 for rate in spot_rates):
            raise ValueError("Spot rates must be non-negative.")

        if coupon_rate < 0 or coupon_rate > 1:
            raise ValueError("Coupon rate must be in the range [0, 1].")

        if present_value < 0:
            raise ValueError("Present value must be non-negative.")

        if face_value < 0:
            raise ValueError("Face value must be non-negative.")

    coup_val = coupon_value(face_value, coupon_rate, compounding_frequency_yr)

    num_time_steps = int(years_to_maturity * compounding_frequency_yr)
    c_f = coup_val + face_value
    k_1 = num_time_steps - 1

    discount_sum = 0
    for time_step in range(1, k_1 + 1):
        year = time_step / compounding_frequency_yr
        spot_rate = spot_rates[time_step - 1]

        discount_sum += interest.continuous_compound_interest_discounted(
            spot_rate, year
        )

    spot_yield = (compounding_frequency_yr / num_time_steps) * math.log(
        (c_f) / (present_value - coup_val * discount_sum)
    )

    return spot_yield


def forward_rate_continuous(
    time_j: float,
    time_k: float,
    spot_rate_0_j: float,
    spot_rate_0_k: float,
    checks: bool = True,
) -> float:
    """
    Calculate the forward rate between two time periods.

    Args:
        time_j: float
            The time period at which the forward rate starts.
        time_k: float
            The time period at which the forward rate ends.
        spot_rate_0_j: float
            The spot rate at time period j.
        spot_rate_0_k: float
            The spot rate at time period k.

    Returns:
        forward_rate: float
            The forward rate between time periods j and k: y_{j, k}.
    """

    if checks:
        if time_k < 0 or time_j < 0:
            raise ValueError("Time periods must be non-negative.")

        if time_j > time_k:
            raise ValueError("Time period j must be before time period k.")

        if spot_rate_0_j < 0 or spot_rate_0_k < 0:
            raise ValueError("Spot rates must be non-negative.")

        if spot_rate_0_j > spot_rate_0_k:
            raise ValueError(
                "Spot rate at time period j must be less than spot rate at time period k. "
                + "This would otherwise cause a negative forward rate!"
            )

    forward_rate = (spot_rate_0_k * time_k - spot_rate_0_j * time_j) / (time_k - time_j)

    return forward_rate


def recursive_zero_coupon_yield_continuous(
    coupon_bond_prices: list[float],
    face_value: int,
    maturity_periods: list[int],
    coupon_rate: float,
    compounding_frequency_yr: int,
    checks: bool = True,
) -> tuple[list[float], list[float]]:
    """
    Calculates the one-period forward rates (recursively) given prices of coupon bearing bonds.

    Args:
        coupon_bond_prices: list[float]
            The prices of the coupon bearing bonds.
        face_value: int
            The face value of the bond.
        maturity_periods: list[int]
            The number of periods until the bond matures.
        coupon_rate: float
            The annual coupon rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        spot_rates: list[float]
            The spot rates of the bonds.
        forward_rates: list[float]
            The forward rates of the bonds.
    """

    if checks:
        # Check lengths of input lists
        if len(coupon_bond_prices) != len(maturity_periods):
            raise ValueError(
                "The number of bond prices must equal the number of maturity periods."
            )

        if compounding_frequency_yr < 1:
            raise ValueError("Compounding frequency must be a positive integer.")

        if any(price < 0 for price in coupon_bond_prices):
            raise ValueError("Bond prices must be non-negative.")

        if face_value < 0:
            raise ValueError("Face value must be non-negative.")

    # Bond 1 can be seen as a zero-coupon bond with face value F + C
    # Since it has no coupons, it's yield is the same as the spot rate.
    # For the remaining bonds, we can calculate the spot rate and forward rate
    # with the current and previous bonds' spot rates.

    forward_rates = []
    spot_rates = []

    for k, bond_price in enumerate(coupon_bond_prices, start=1):
        years_to_maturity = maturity_periods[k - 1]
        prev_period = maturity_periods[k - 2] if k > 1 else 0

        # Calculate the spot rate for the bond
        y_0_k = spot_zero_coupon_yield_curve_continuous(
            face_value,
            bond_price,
            years_to_maturity,
            spot_rates,
            coupon_rate,
            compounding_frequency_yr,
        )

        spot_rates.append(y_0_k)

        if k > 1:
            # Calculate the forward rate for the bond
            prev_spot_rate = spot_rates[-2]
            current_spot_rate = spot_rates[-1]
            y_k_1_k = forward_rate_continuous(
                prev_period,
                years_to_maturity,
                prev_spot_rate,
                current_spot_rate,
                checks=False,
            )

            forward_rates.append(y_k_1_k)
        else:
            # Forward rate equals the spot rate for the first bond
            forward_rates.append(y_0_k)

    return spot_rates, forward_rates


def price_zero_coupon_bond(
    forward_rate: float, up_rate: float, down_rate: float, up_pr: float, down_pr: float
) -> float:
    """
    Computes the price of a zero coupon bond with F = $1
    given a forward rate assuming a binomial model where the forward rate
    can move up or down as specified with probabilities p and q.

    Args:
        forward_rate: float
            The forward rate.
        up_rate: float
            The forward rate if it moves up.
        down_rate: float
            The forward rate if it moves down.
        up_pr: float
            The probability of the forward rate moving up.
        down_pr: float
            The probability of the forward rate moving down.

    Returns:
        zero_coupon_yield: float
            The zero coupon yield, i.e. p{.,.}.
    """

    p_factor_price = 1 / (1 + forward_rate)
    # print("p factor price", p_factor_price)
    expectation = up_pr * up_rate + down_pr * down_rate
    # print(
    #     f"Expectation: {up_pr} * {up_rate} + {down_pr} * {down_rate} = {expectation}")
    p_price = p_factor_price * expectation
    # print("p price", p_price)

    return p_price


def spot_rate_from_present_rate(present_rate: float, end_time: float) -> float:
    """
    Computes the spot rate from the present rate, P_{0,n}

    Args:
        present_rate: float
            The present rate.
        end_time: float
            The end time, n.

    Returns:
        spot_rate: float
            The spot rate, y_{0,n}.
    """

    if present_rate <= 0:
        raise ValueError("Present rate must be strictly positive.")

    if end_time <= 0:
        raise ValueError("End time must be strictly positive.")

    fraction = 1 / present_rate

    return fraction ** (1 / end_time) - 1


def spot_rate_from_p_lattice(p_lattice: BinLattice) -> float:
    """
    Computes the spot rate from a P lattice.

    Args:
        p_lattice: BinLattice
            The P lattice.

    Returns:
        spot_rate: float
            The spot rate.
    """

    head_node = p_lattice.get_head_node()
    p_value = head_node.get_value()

    # Add 1 to depth as (e.g. a) tree depth of 1 would be P_{0,2}
    maturity = p_lattice.get_depth() + 1
    return spot_rate_from_present_rate(p_value, maturity)
