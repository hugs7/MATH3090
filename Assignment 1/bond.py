# Author: Hugo Burton
# Date: 27/02/2024


import interest


def price_zero_coupon_bond_discrete(face_value: int, years_to_maturity: int, interest_rate: float, compounding_frequency_yr: int):
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
        interest_rate, years_to_maturity, compounding_frequency_yr)

    price = face_value * beta

    return price


def price_zero_coupon_bond_continuous(face_value: int, years_to_maturity: int, interest_rate: float):
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
        interest_rate, years_to_maturity)

    price = face_value * beta

    return price


def price_zero_coupon_bond_nonconstant_yield(face_value: int, years_to_maturity: int, yield_function):
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

    price = face_value * \
        interest.nonconstant_yield_discounted(
            yield_function, years_to_maturity)

    return price
