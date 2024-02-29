"""
Implements Newton's method for approximating function roots
"""

def derivative(f: callable, x: float, tolerance: float) -> float:
    """
    Calculate the derivative of a function at a given point.

    Args:
        f: function
            The function to calculate the derivative of.
        x: float
            The point at which to calculate the derivative.
        tolerance: float
            The tolerance of the approximation.

    Returns:
        f_prime: float
            The derivative of the function at the given point.
    """

    f_prime = (f(x + tolerance) - f(x - tolerance)) / (2 * tolerance)

    return f_prime


def newtons(f: callable, x_0: float, tolerance: float, max_iterations: int) -> float:
    """
    Calculate the root of a function using Newton's method.

    Args:
        f: function
            The function to find the root of.
        x_0: float
            The initial guess of the root.
        tolerance: float
            The tolerance of the approximation.
        max_iterations: int
            The maximum number of iterations.

    Returns:
        x_n: float
            The approximation of the root.
    """

    # Compute the derivative of the function

    x_n = [x_0]

    for n in range(max_iterations):
        last_x_n = x_n[-1]
        f_prime = derivative(f, x_n, tolerance)
        x_n.append(last_x_n - f(x_n) / f_prime)

        x_diff = abs(x_n[-1] - x_n[-2])
        func_diff = abs(f(x_n))

        if min(x_diff, func_diff) < tolerance:
            # The approximation is within the tolerance
            break

    return x_n[-1]
