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


def price_coupon_bearing_bond_discrete(face_value: int, years_to_maturity: int, coupon_rate: float, interest_rate: float, compounding_frequency_yr: int):
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
    def coupon_payment_present_value(coupon_rate_annual: float, interest_rate: float, compounding_frequency_yr: int, years_to_maturity: int):
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

        numerator = (1 - ((1 + interest_rate / compounding_frequency_yr)
                          ** (-years_to_maturity * compounding_frequency_yr)))

        denominator = interest_rate / compounding_frequency_yr

        payment_value = coupon_rate_adjusted * (numerator / denominator)

        return payment_value

    # Initialise the price
    price = 0

    # Calculate the annual coupon payment
    coupon_rate_annual = coupon_rate * face_value

    # Add the present value of the coupon payments
    coupon_value = coupon_payment_present_value(
        coupon_rate_annual, interest_rate, compounding_frequency_yr, years_to_maturity)
    price += coupon_value

    # Add the face value discounted to the present
    discounted_face_value = price_zero_coupon_bond_discrete(
        face_value, years_to_maturity, interest_rate, compounding_frequency_yr)
    price += discounted_face_value

    return price
