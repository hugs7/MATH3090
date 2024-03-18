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


def newtons_method(
    f: callable,
    f_prime: callable,
    x_0: float,
    tolerance: float,
    max_iterations: int,
    generate_table: bool = False,
    log: bool = True,
    col_spaces: list = [],
    precision: int = 6,
) -> tuple[float, list, int]:
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
        log: bool
            Whether to log the iterations.

    Returns:
        x_n: float
            The approximation of the root.
        md_table_rows: list
            The rows of the table in markdown format.
        num_iterations: int
            The number of iterations.
    """

    x_n = [x_0]

    md_table_rows = []
    num_iterations = 0

    for n in range(max_iterations):
        last_x_n = x_n[-1]

        derivative = f_prime(last_x_n)
        if derivative == 0:
            raise Exception("Derivative is zero")

        x_n.append(last_x_n - f(last_x_n) / derivative)

        this_x_n = x_n[-1]
        last_x_n = x_n[-2]

        diff = abs(this_x_n - last_x_n)

        if log or generate_table:
            a, b, c = col_spaces

            table_row = f"|{n:^{a}}|{round(this_x_n, precision):^{b}}|{round(diff, precision):^{c}}|"

            if log:
                print(table_row)

            if generate_table:
                md_table_rows.append(table_row)

        x_diff = abs(this_x_n - last_x_n)
        func_diff = abs(f(this_x_n))
        if min(x_diff, func_diff) < tolerance:
            # The approximation is within the tolerance
            break

        num_iterations += 1

    return x_n[-1], md_table_rows, num_iterations
