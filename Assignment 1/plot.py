from typing import Dict
import matplotlib.pyplot  as plt
from mpl_toolkits.mplot3d import Axes3D


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


def plot_3d_dictionary(dictionary: Dict[float, float], x_label: str, y_label: str, z_label: str, title: str):
    """
    Plot a dictionary in 3D.

    Args:
        dictionary: Dict[float, float]
            The dictionary to plot.
        x_label: str
            The label of the x-axis.
        y_label: str
            The label of the y-axis.
        z_label: str
            The label of the z-axis.
        title: str
            The title of the plot.
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_vals = list(dictionary.keys())
    y_vals = [0] * len(x_vals)  # Y-values set to 0 for simplicity in a 3D plot
    z_vals = list(dictionary.values())

    ax.plot(x_vals, y_vals, z_vals)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_title(title)

    plt.show()
