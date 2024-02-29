from typing import Dict
import matplotlib.pyplot  as plt


def plot_dictionary(dictionary: Dict[float, float], x_label: str, y_label: str, title: str):
    """
    Plot a dictionary.

    Args:
        dictionary: Dict[float, float]
            The dictionary to plot.
        x_label: str
            The label of the x-axis.
        y_label: str
            The label of the y-axis.
        title: str
            The title of the plot.
    """

    x_vals = list(dictionary.keys())
    y_vals = list(dictionary.values())

    plt.plot(x_vals, y_vals)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()