"""
Helper for computing swap values in contracts / borrowing
"""

import interest


def fixed_payment_continuous_compounding(notional: float, rate: float) -> float:
    """
    Calculate the fixed payment for a swap with continuous compounding.

    Args:
        notional: float
            The notional amount.
        rate: float
            The interest rate.

    Returns:
        fixed_payment: float
            The fixed payment for the swap.
    """

    fixed_payment = notional * rate

    return fixed_payment


def floating_payment_continuous_compounding(notional: float, forward_rate: float, floating_spread: float, compounding_frequency_yr: int) -> float:
    """
    Calculate the floating payment for a swap with continuous compounding.

    Args:
        notional: float
            The notional amount.
        forward_rate: float
            The corresponding forward rate for that time interval.
        floating_spread: float
            The floating spread.
        compounding_frequency_yr: int
            The frequency at which the interest is compounded.

    Returns:
        floating_payment: float
            The floating payment for the swap.
    """

    floating_payment = notional * \
        (forward_rate + floating_spread) / compounding_frequency_yr

    return floating_payment


def fix_float_delta(fixed_payment: float, floating_payment: float) -> float:
    """
    Calculate the difference between the fixed payment and the floating payment.

    Args:
        fixed_payment: float
            The fixed payment for the swap.
        floating_payment: float

    Returns:
        delta: float
            The difference between the fixed payment and the floating payment.
    """

    delta = fixed_payment - floating_payment

    return delta


def swap_value_at_spot(fixed_payment: float, floating_payment: float, spot_rate: float, time_period: float) -> float:
    """
    Calculate the swap value.

    Args:
        fixed_payment: float
            The fixed payment for the swap.
        floating_payment: float
            The floating payment for the swap.
        time_period: float
            The time period.
        spot_rate: float
            The spot rate.

    Returns:
        swap_value: float
            The swap value.
    """

    discount_factor = interest.continuous_compound_interest_discounted(
        spot_rate, time_period)

    fix_float = fix_float_delta(fixed_payment, floating_payment)

    swap_value = fix_float * discount_factor

    return swap_value


def compute_swap_values(notional: float, maturity_periods: list[int], compounding_frequency_yr: int, spot_rates: list[float], forward_rates: list[float],
                        fixed_rate: float, floating_spread: float) -> list[float]:
    """
    Compute the swap values for a list of spot rates and forward rates as well as 
    fixed and floating rates.

    Args:
        notional: float
            The notional amount.
        maturity_periods: list[int]
            A list of the years to maturity for each bond
        compounding_frequency_yr: int
            The frequency at which the interest is compounded.
        spot_rates: list[float]
            The spot rates.
        forward_rates: list[float]
            The forward rates.
        fixed_rate: float
            The fixed rate.
        floating_spread: float
            The floating offset.

    Returns:
        swap_values: list[float]
            The swap values.
    """

    swap_values = []

    # Compute once as this doesn't change.
    fixed_payment = fixed_payment_continuous_compounding(notional, fixed_rate)

    for k, T in enumerate(maturity_periods):
        spot_rate = spot_rates[k]
        forward_rate = forward_rates[k]

        floating_payment = floating_payment_continuous_compounding(
            notional, forward_rate, floating_spread, compounding_frequency_yr)

        swap_value = swap_value_at_spot(
            fixed_payment, floating_payment, spot_rate, T)

        swap_values.append(swap_value)

    return swap_values
