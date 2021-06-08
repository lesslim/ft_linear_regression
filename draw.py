import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
from typing import List, Tuple


def animate(n: int, x: List[float], y: List[float], plot):
    """
    Part of theta evolving animation.
    """
    plot.set_data(x[:n], y[:n])
    return plot,


def print_thetas(theta: Tuple[slice, int], flags: argparse.Namespace, n: str):
    """
    Print theta evolving.
    """
    fig = plt.figure(1, figsize=(12, 9))
    plt.title(f'θ{n} evolution')
    plt.xlabel("Number of iterations")
    plt.ylabel("Value")
    plot, = plt.plot(theta, "g.")
    x = np.linspace(0, flags.iterations, flags.iterations)
    anim.FuncAnimation(fig, animate, len(x), fargs=[x, theta, plot],
                       blit=True, interval=0, repeat=False)

    plt.show()


def animate_function(n: int, x: List[float], plot, thetas: List[List[float]]):
    """
    Part of linear function animation.
    """
    y = [thetas[:, 1][n] * i + thetas[:, 0][n] for i in x]
    plot.set_data(x, y)
    return plot,


def print_graph(mileage: List[float], price: List[float],
                thetas: List[List[float]], flags):
    """
    Print linear function in animation or static way.
    """

    fig = plt.figure(0, figsize=(12, 8))
    plt.title("The dependence of the price of the car on the mileage.")
    plt.xlabel("Mileage, km")
    plt.ylabel("Price")
    x, y = mileage, price
    plt.scatter(x, y)

    if flags.animation:
        y = price
        plot, = plt.plot(
            x, y, "-r",
            label=f"y = {thetas[-1][1]:.2f} x + {thetas[-1][0]:.2f}")
        anim.FuncAnimation(fig, animate_function, flags.iterations,
                           fargs=[x, plot, thetas], blit=True,
                           interval=0, repeat=False)

    else:
        y = [thetas[-1][1] * i + thetas[-1][0] for i in mileage]
        plt.plot(x, y, "-r",
                 label=f"y = {thetas[-1][1]:.2f} x + {thetas[-1][0]:.2f}")

    plt.legend(loc="lower left")
    plt.show()
