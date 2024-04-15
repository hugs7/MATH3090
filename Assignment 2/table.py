
from typing import List, Tuple, Union


def generate_table_header(col_heads: List[str], col_spaces: List[int]) -> Tuple[str, str]:
    """
    Generate a table header.

    Args:
        col_heads: List[str]
            The column headers.
        col_spaces: List[int]
            The column spaces.

    Returns:
        header_row: str
            The header row.
        format_row: str
            The format row.
    """

    header_row = ""
    format_row = ""

    for i, col_head in enumerate(col_heads):
        space = col_spaces[i]
        part = f"|{col_head:^{space}}"
        header_row += part
        middle = '-'*(max(1, len(part) - 2 - 2))
        format_row += f"| :{middle}: "

    header_row += "|"
    format_row += "|"

    return header_row, format_row


def generate_table_row(row_data: List[str], col_spaces: List[int], col_decimals: Union[None, List[None | int]]) -> str:
    """
    Generate a table row.

    Args:
        row_data: List[str]
            The data for the row.
        col_spaces: List[int]
            The column spaces.
        col_decimals: Union[None, List[None | int]]
            The number of decimal places for each column. Should be None 
            for a given column if column contains strings.

    Returns:
        row: str
            The row.
    """

    # Check if the number of columns is correct
    if len(row_data) != len(col_spaces):
        raise ValueError(
            "Number of columns does not match number of column spaces")

    if col_decimals is not None and len(row_data) != len(col_decimals):
        raise ValueError(
            "Number of columns does not match number of column decimals")

    row = ""

    for i, data in enumerate(row_data):
        space = col_spaces[i]
        decimals = col_decimals[i]

        if decimals is not None:
            data = f"{float(data):.{decimals}f}"

        row += f"|{data:^{space}}"

    row += "|"

    return row


def generate_table(
    col_heads: List[str], col_spaces: List[int], data: List[List[str]], col_decimals: List[None | int]
) -> str:
    """
    Generate a table.

    Args:
        col_heads: List[str]
            The column headers.
        col_spaces: List[int]
            The column spaces.
        data: List[List[str]]
            The data for the table.
        col_decimals: List[None | int]
            The number of decimal places for each column.

    Returns:
        table: str
            The table.
    """

    header_row, format_row = generate_table_header(col_heads, col_spaces)

    table = header_row + "\n" + format_row + "\n"

    for row_data in data:
        table += generate_table_row(row_data, col_spaces, col_decimals) + "\n"

    return table
