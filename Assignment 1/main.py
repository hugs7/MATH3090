# Author: Hugo Burton
# Date: 27/02/2024

import math
from typing import Dict
from colorama import Fore, Style

import bond
import interest
import plot
import numpy as np

BREAK_WIDTH = 100

QUARTLERLY = 4


def display_question(question_number: int, question_text: str):
    """
    Display a question.

    Args:
        question_number: int
            The number of the question.
        question_text: str
            The text of the question.
    """

    print("-"*BREAK_WIDTH)
    print(f"{Fore.BLUE}Question {question_number}:{Style.RESET_ALL}")
    print(question_text)


def display_answer(answer_value: float, decimal_places: int = 2):
    """
    Display an answer.

    Args:
        answer_value: float
            The value of the answer.
    """

    print(f"{Fore.GREEN}Answer:{Style.RESET_ALL}", end="")
    print(f"${round(answer_value, decimal_places)}")
    print("-"*BREAK_WIDTH)


def q1():
    print("Question 1:")

    # Part a (3 marks)
    print("Part A:")
    print("Suppose a company issues a zero coupon bond with face value $10,000 and which matures in 20 years. Calculate the price given:")

    subquestions = {
        "i":   "an 8% discount compound annual yield, compounded annually",
        "ii":  "an 8% discount continuous annual yield, compounded semi-annually",
        "iii": "a nonconstant yield of y(t) = 0.06 + 0.2 t * exp(-t^2)"
    }

    face_value = 10_000
    years_to_maturity = 20

    # Question i
    q = "i"
    interest_rate = 0.08
    compounding_frequency_yr = 1

    price_i = bond.price_zero_coupon_bond_discrete(
        face_value, years_to_maturity, interest_rate, compounding_frequency_yr)

    display_question(q, subquestions[q])
    display_answer(price_i)
    # Question ii
    q = "ii"
    interest_rate = 0.08

    price_ii = bond.price_zero_coupon_bond_continuous(
        face_value, years_to_maturity, interest_rate)

    display_question(q, subquestions[q])
    display_answer(price_ii)

    # Question iii
    q = "iii"
    def yield_function(t): return 0.06 + 0.2 * t * math.exp(-t**2)

    price_iii = bond.price_zero_coupon_bond_nonconstant_yield(
        face_value, years_to_maturity, yield_function)
    display_question(q, subquestions[q])
    display_answer(price_iii)

    # Part b (3 marks)
    print("Part B:")
    print("A 10 year $10,000 government bond has a coupon rate of 5% payable quarterly and yields 7%. Calculate the price.")

    face_value = 10_000
    years_to_maturity = 10
    coupon_rate = 0.05
    interest_rate = 0.07
    compounding_frequency_yr = QUARTLERLY

    price_b = bond.price_coupon_bearing_bond_discrete(
        face_value, years_to_maturity, coupon_rate, interest_rate, compounding_frequency_yr)

    display_answer(price_b)


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
    cash_flow = lambda k, x: -3*x if k == 0 else (5 if k == 1 else x)

    accept_condition = lambda p: p > 0

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

    print(f"Range of x such that P > 0 when r = 5%: {accept_min_x} < x < {accept_max_x}")


    # Part b (3 marks)
    print("Part B (3 marks):")
    print("The IRR (internal rate of return) is r such that P = 0. For what range of x will there be", 
          "a unique strictly positive IRR?")
    
    xr_grid = {}

    for r in np.arange(0.0, 1.0, 0.01):
        for x in np.arange(x_min, x_max, x_step):
            p = present_value(x)

            # if p == 0:
            xr_grid[(x, r)] = p
            # print(f"{round(x, 3):<6}, {round(r, 3):<6}, {round(p, 3):<6}")
    


    # Print a 3d grid of x and r
    plot.plot_3d_dictionary(xr_grid, "x", "r", "P", "Present value of cash flow")




def __main__():
    q1()

    q2()

    return 0


if __name__ == "__main__":
    __main__()
