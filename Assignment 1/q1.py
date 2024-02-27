# Author: Hugo Burton
# Date: 27/02/2024

import math
from colorama import Fore, Style
import bond

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

    print(f"{Fore.GREEN}Answer:{Style.RESET_ALL} ", end="")
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


def __main__():
    q1()

    return 0


if __name__ == "__main__":
    __main__()
