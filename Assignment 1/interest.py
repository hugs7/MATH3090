# Author: Hugo Burton
# Date: 27/02/2024

import math
from scipy import integrate


def discrete_compound_interest_accumuated(interest_rate: float, maturity_yrs: int, compounding_frequency_yr: int):
    """
    Calculate the accumulated ratio of a sum of money after a given number of years at a given interest rate.

    Args:
        interest_rate: float
            The interest rate.
        maturity_yrs: int
            The number of years the sum of money is invested for.
        compounding_frequency_yr: int
            The frequency at which the interest is compounded.

    Returns:
        alpha: float
            The accumulated ratio of the sum of money.
    """

    alpha = (1 + interest_rate / compounding_frequency_yr) ** (
        maturity_yrs * compounding_frequency_yr)

    return alpha


def discrete_compound_interest_discounted(interest_rate: float, maturity_yrs: int, compounding_frequency_yr: int):
    """
    Calculate the discounted ratio of a sum of money after a given number of years at a given interest rate.

    Args:
        interest_rate: float
            The interest rate.
        maturity_yrs: int
            The number of years the sum of money is invested for.
        compounding_frequency_yr: int
            The frequency at which the interest is compounded.

    Returns:
        beta: float
            The discounted ratio of the sum of money.
    """

    exponent = - maturity_yrs * compounding_frequency_yr

    beta = (1 + interest_rate / compounding_frequency_yr) ** exponent

    return beta


def continuous_compound_interest_accumulated(interest_rate: float, maturity_yrs: int):
    """
    Calculate the accumulated ratio of a sum of money after a given number of years at a given interest rate.

    Args:
        interest_rate: float
            The interest rate.
        maturity_yrs: int
            The number of years the sum of money is invested for.

    Returns:
        alpha: float
            The accumulated ratio of the sum of money.
    """

    alpha = math.exp(interest_rate * maturity_yrs)

    return alpha


def continuous_compound_interest_discounted(interest_rate: float, maturity_yrs: int):
    """
    Calculate the discounted ratio of a sum of money after a given number of years at a given interest rate.

    Args:
        interest_rate: float
            The interest rate.
        maturity_yrs: int
            The number of years the sum of money is invested for.

    Returns:
        beta: float
            The discounted ratio of the sum of money.
    """

    beta = math.exp(-interest_rate * maturity_yrs)

    return beta


def check_integration_error(error: float):
    """
    Check if the integration error is too high.

    Args:
        error: float
            The integration error.
    """

    if error > 1e-6:
        print(f"Warning: High integration error. Val: {error}")


def nonconstant_yield_accumulated(yield_function: callable, maturity_yrs: int):
    """
    Calculate the accumulated ratio of a sum of money after a given number of years at a given nonconstant yield.

    Args:
        yield_function: function
            The yield function.
        maturity_yrs: int
            The number of years the sum of money is invested for.

    Returns:
        alpha: float
            The accumulated ratio of the sum of money.
    """

    int_val, error = integrate.quad(yield_function, 0, maturity_yrs)
    check_integration_error(error)

    alpha = math.exp(int_val)

    return alpha


def nonconstant_yield_discounted(yield_function: callable, maturity_yrs: int):
    """
    Calculate the discounted ratio of a sum of money after a given number of years at a given nonconstant yield.

    Args:
        yield_function: function
            The yield function.
        maturity_yrs: int
            The number of years the sum of money is invested for.

    Returns:
        beta: float
            The discounted ratio of the sum of money.
    """

    int_val, error = integrate.quad(yield_function, 0, maturity_yrs)
    check_integration_error(error)

    beta = math.exp(-int_val)

    return beta
