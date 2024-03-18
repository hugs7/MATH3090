# Author: Hugo Burton
# Date: 27/02/2024

import math
from typing import Dict
from colorama import Fore
import numpy as np
import sys
from IPython.display import display


import bond
import interest
import newtons
import display

QUARTLERLY = 4

EPS = 0.01


def q1():
    print("Question 1:")

    # Part a (3 marks)
    print("Part A:")
    print(
        "Suppose a company issues a zero coupon bond with face value $10,000 and which matures in 20 years. Calculate the price given:"
    )

    subquestions = {
        "i": "an 8% discount compound annual yield, compounded annually",
        "ii": "an 8% discount continuous annual yield, compounded semi-annually",
        "iii": "a nonconstant yield of y(t) = 0.06 + 0.2 t * exp(-t^2)",
    }

    face_value = 10_000
    years_to_maturity = 20

    # Question i
    q = "i"
    interest_rate = 0.08
    compounding_frequency_yr = 1

    price_i = bond.price_zero_coupon_bond_discrete(
        face_value, years_to_maturity, interest_rate, compounding_frequency_yr
    )

    display.display_question(q, subquestions[q])
    display.display_answer(price_i)

    # Question ii
    q = "ii"
    interest_rate = 0.08

    price_ii = bond.price_zero_coupon_bond_continuous(
        face_value, years_to_maturity, interest_rate
    )

    display.display_question(q, subquestions[q])
    display.display_answer(price_ii)

    # Question iii
    q = "iii"

    def yield_function(t):
        return 0.06 + 0.2 * t * math.exp(-(t**2))

    price_iii = bond.price_zero_coupon_bond_nonconstant_yield(
        face_value, years_to_maturity, yield_function
    )
    display.display_question(q, subquestions[q])
    display.display_answer(price_iii)

    # Part b (3 marks)
    print("Part B:")
    print(
        "A 10 year $10,000 government bond has a coupon rate of 5% payable quarterly and yields 7%. Calculate the price."
    )

    face_value = 10_000
    years_to_maturity = 10
    coupon_rate = 0.05
    interest_rate = 0.07
    compounding_frequency_yr = QUARTLERLY

    price_b = bond.price_coupon_bearing_bond_discrete(
        face_value,
        years_to_maturity,
        coupon_rate,
        interest_rate,
        compounding_frequency_yr,
    )

    display.display_answer(price_b)


def q2():
    print("Question 2:")
    print("Consider the cash flow C_0 = -3x, C_1 = 5, C_2 = x")
    print("(at periods 0, 1, 2 respectively) for some x > 0")

    # Part a (3 marks)
    print("Part A (3 marks):")
    print("Apply the discount process d(k) = (1 + r)^(-k) so that the present value is")
    print("P = sum_{k=0}^2 d(k) C_k")
    print("What is the range of x such that P > 0 when r = 5%?")

    r = 0.05

    def cash_flow(k, x):
        return -3 * x if k == 0 else (5 if k == 1 else x)

    def accept_condition(p):
        return p > 0

    # Function to calculate present value based on some value of x
    def present_value(x: float) -> float:
        present_value = 0

        for k in range(2 + 1):
            beta = interest.discrete_compound_interest_discounted(r, k, 1)
            undiscounted_cash_flow_year_k = cash_flow(k, x)
            discounted_cash_flow_year_k = undiscounted_cash_flow_year_k * beta

            present_value += discounted_cash_flow_year_k

        return present_value

    cash_flows_x: Dict[float, float] = {}
    x_min = -100.0
    x_max = 100.0
    x_step = 0.01
    accept_min_x = None
    accept_max_x = None

    # Loop over a wide range of x
    for x in np.arange(x_min, x_max, x_step):
        cash_flow_x = present_value(x)

        cash_flows_x[x] = cash_flow_x

        if accept_condition(cash_flow_x):
            # Min
            if not accept_min_x:
                accept_min_x = x
            elif x < accept_min_x:
                accept_min_x = x

            # Max
            if not accept_max_x:
                accept_max_x = x
            elif x > accept_max_x:
                accept_max_x = x

    if accept_min_x == x_min:
        accept_min_x = -math.inf

    if accept_max_x == x_max:
        accept_max_x = math.inf

    # Visualise cash flow on a graph
    # plot.plot_dictionary(cash_flows_x, "x", "P", "Present value of cash flow")

    print(
        f"Range of x such that P > 0 when r = {r * 100}%: {accept_min_x} < x < {accept_max_x}"
    )

    # Part b (3 marks)
    print("Part B (3 marks):")
    print(
        "The IRR (internal rate of return) is r such that P = 0. For what range of x will there be",
        "a unique strictly positive IRR?",
    )

    xr_grid = {}

    accept_xr = []

    for r in np.arange(0.0, 1.0, 0.01):
        for x in np.arange(x_min, x_max, x_step):
            p = present_value(x)

            # if p == 0:
            xr_grid[(x, r)] = p
            # print(f"{round(x, 3):<6}, {round(r, 3):<6}, {round(p, 3):<6}")

            if abs(p) < EPS:
                print(f"{round(p, 2):<6}, {round(x, 3):<6}, {round(r, 2):<6}")
                accept_xr.append((x, r))


def q3():
    print("Question 3")
    print(
        "In this question, consider a bond with the set of cashflows given in Table 1. Here, note that the face "
        + "value F is already included in the last cashflow. Let y be the yield to maturity, t_i, be the time of the "
        + "ith cashflow, C_i, and PV = 100 be the market price of the bond at t = 0. Assume continuous compounding. "
        + "Then, y solves PV = \sum_{i=1} C_i e^{-yt_i}."
    )

    # Part a (3 marks)
    print("Part a (3 marks)")
    print(
        "Write out the Newton iteration to compute y_{n+1} from y_{n}. Specifically, clearly indicate the "
        + "functions f(y) and f'(y)"
    )

    cashflows = [2.3, 2.9, 3.0, 3.2, 4.0, 3.8, 4.2, 4.8, 5.5, 105]
    # Market price of the bond at t = 0
    PV = 100

    def f(y):
        return (
            sum(
                cashflows[t - 1]
                * interest.continuous_compound_interest_discounted(y, t)
                for t in range(1, len(cashflows) + 1)
            )
            - PV
        )

    def f_prime(y):
        return -sum(
            ((t * cashflows[t]) / ((1 + y) ** (t + 1))) for t in range(len(cashflows))
        )

    # Part b (5 marks)
    print("Part b (5 marks)")
    print("Implement the above Newton iteration in code using the stopping criteria")
    print("|y_{n+1} - y_n| < 10^{-8})")

    eps = 1e-8

    # Set initial y value
    x_0 = 0.05

    # Solve y using Newton's method given f and PV as inputs

    approx, _, _ = newtons.newtons_method(f, f_prime, x_0, eps, 9999999)

    display.display_answer(approx, 5, False)

    # Part ii: Trying larger values of y_0
    print("Part ii: Trying with larger values of y_0")

    y_0_vals = [x for x in np.arange(0.05, 0.25, 0.01)]
    for y_0 in y_0_vals:
        print(
            f"{Fore.CYAN}y_0 = {Fore.LIGHTRED_EX}{round(y_0, 2)}{Fore.WHITE}", end=": "
        )
        approx, _, _ = newtons.newtons_method(f, f_prime, y_0, eps, 9999999, log=False)
        display.display_answer(approx, 10, False)


def q4():
    print("Question 4 (4 marks)")
    print("In the Constant Growth DDM model, the present value of the share is")

    print("PV = \sum_{t=1}^{\infty} \frac{D_t}{(1 + k)^t}")

    print(
        "where D_1, D_2,... are (non-random) dividends and k > 0 is the required rate of return."
    )
    print("Suppose D_0 > 0, k > 0 and g > 0.")
    print("Derive the formula for the present value (2) when")

    print("D_t = D_0 (1 + g)^{\ceil{t/2}}, t = 1, 2, ...")

    print(
        "where \ceil{x} is the ceiling function (i.e. the smallest integer greater than or equal to x)."
    )

    print(
        "What is the condition of g so that the PV is finite? To get full marks, you will need to write an explicit expression (without summation)."
    )


def main():
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        question_number = int(sys.argv[1])
        if question_number == 1:
            q1()
        elif question_number == 2:
            q2()
        elif question_number == 3:
            q3()
        else:
            print("Invalid question number")
    else:
        # Run all questions
        q1()
        q2()
        q3()

    return 0


if __name__ == "__main__":
    main()
