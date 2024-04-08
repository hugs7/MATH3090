"""
Helper for computing swap values in contracts / borrowing
"""


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


def floating_payment_continuous_compounding(notional: float, forward_rate: float, floating_spread: float) -> float:
    """
    Calculate the floating payment for a swap with continuous compounding.

    Args:
        notional: float
            The notional amount.
        forward_rate: float
            The corresponding forward rate for that time interval.
        floating_spread: float
            The floating spread.

    Returns:
        floating_payment: float
            The floating payment for the swap.
    """

    floating_payment = notional * (forward_rate + floating_spread)

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


def swap_value_at_spot(fixed_payment: float, floating_payment: float, discount_factor: float) -> float:
    """
    Calculate the swap value.

    Args:
        fixed_payment: float
            The fixed payment for the swap.
        floating_payment: float
            The floating payment for the swap.
        discount_factor: float
            The discount factor.

    Returns:
        swap_value: float
            The swap value.
    """

    swap_value = fixed_payment - floating_payment * discount_factor

    return swap_value
