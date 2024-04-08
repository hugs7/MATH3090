# Author: Hugo Burton
# Date: 27/02/2024


import math
import interest

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

    beta = interest.discrete_interest_bond(
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
    t_1 = num_time_steps - 1

    interest_adjusted = 1 + interest_rate
    coup_val = coupon_value(face_value, coupon_rate, compounding_frequency_yr)
    bond_value = 0

    # Coupons

    reinvestments = []

    for time_step in range(1, t_1 + 1):
        year = time_step / compounding_frequency_yr

        # Length of time this coupon can be reinvested for
        reinvestment_time = bond_duration - year
        print(
            f"Time step {time_step}, year {year}, reinvestment time {reinvestment_time}, coupon value {coup_val}"
        )
        coupon_reinvestment_val = coup_val * interest_adjusted**reinvestment_time

        reinvestments.append(coupon_reinvestment_val)

    # Last coupon (including face value)

    # B
    last_coupon_reinvestment_val = (face_value + coup_val) / (
        interest_adjusted ** (years_to_maturity - bond_duration)
    )

    reinvestments.append(last_coupon_reinvestment_val)
    print(reinvestments)
    bond_value = sum(reinvestments)

    return bond_value


# ---- Yield Curves ----


def spot_zero_coupon_yield_curve_continuous(
    face_value: int,
    present_value: float,
    years_to_maturity: int,
    interest_rate: float,
    coupon_rate: float,
    compounding_frequency_yr: int,
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
        interest_rate: float
            The yield rate of the bond.
        coupon_rate: float
            The annual coupon rate of the bond.
        compounding_frequency_yr: int
            The frequency at which the yield is compounded.

    Returns:
        spot_yield_curve: list[float]
            The spot yield curve for the bond.
    """

    # Checks
    if True:
        if years_to_maturity < 0:
            raise ValueError("Years to maturity must be non-negative.")

        if compounding_frequency_yr < 1:
            raise ValueError("Compounding frequency must be a positive integer.")

        if interest_rate < 0 or interest_rate > 1:
            raise ValueError("Interest rate must be in the range [0, 1].")

        if coupon_rate < 0 or coupon_rate > 1:
            raise ValueError("Coupon rate must be in the range [0, 1].")

        if present_value < 0:
            raise ValueError("Present value must be non-negative.")

        if face_value < 0:
            raise ValueError("Face value must be non-negative.")

        if present_value > face_value:
            raise ValueError("Present value must be less than or equal to face value.")

    coup_val = coupon_value(face_value, coupon_rate, compounding_frequency_yr)

    num_time_steps = years_to_maturity * compounding_frequency_yr
    c_f = coup_val + face_value
    k_1 = num_time_steps - 1

    discount_sum = 0
    for time_step in range(1, k_1 + 1):
        year = time_step / compounding_frequency_yr

        discount_sum += interest.continuous_compound_interest_accumulated(
            interest_rate, year
        )

    return (1 / num_time_steps) * math.log(
        (c_f) / (present_value - coup_val * discount_sum)
    )
