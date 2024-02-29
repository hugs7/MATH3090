"""
Helper for dislaying things on the screen
"""


from colorama import Fore, Style

BREAK_WIDTH = 100

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
