import argparse
import csv
import numpy as np
from typing import List, Tuple
from predict import read_thetas, estimatePrice
from draw import print_thetas, print_graph


def read_data(file: str) -> Tuple[List[float], List[float]]:
    """
    Reading data from a csv and creating feature/target arrays.
    """
    mileage = []
    price = []
    try:
        with open(file, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            try:
                next(data)
            except StopIteration:
                print_error("'data.csv' is empty.")
            for row in data:
                if len(row) > 2 or len(row) < 2:
                    print_error(
                        "There must be exactly 2 numbers per line in csv.")
                mileage.append(float(row[0]))
                price.append(float(row[1]))
    except (FileNotFoundError, PermissionError, ValueError) as e:
        if e == FileNotFoundError:
            print_error("No 'data.csv' file.")
        elif e == PermissionError:
            print_error("No access to file 'data.csv'.")
        else:
            print_error("The data should contain only numbers.")
    if len(mileage) == 0:
        print_error("No data in csv.")
    return mileage, price


def parse_flags() -> argparse.Namespace:
    """
    Parse flags from the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--animation', '-a',
                        action='store_true',
                        help='Animation of linear function evolving.')
    parser.add_argument('--thetas', '-t',
                        action='store_true',
                        help='Animation for thetas evolving.')
    parser.add_argument('--graph', '-g',
                        action='store_true',
                        help='If set, draws a graph of linear function.')
    parser.add_argument('--warmStart', '-w',
                        action='store_true',
                        help='Training with thetas from the file (if exists).')
    parser.add_argument('--iterations', '-i',
                        action="store",
                        type=int,
                        default=1000,
                        help='Set the number of iterations (default is 1000)')
    parser.add_argument('--learningRate', '-l',
                        action="store",
                        type=float,
                        default=0.1,
                        help='To set a number of iterations (default is 500)')
    return parser.parse_args()


def normilize_data(lst: List[float]) -> Tuple[List[float], float]:
    """
    Data normalization.
    """
    diff = max(max(lst), -min(lst))
    if diff:
        return [n / diff for n in lst], diff
    return [0] * len(lst), 0


def gradient_descent(mileage: List[float], price: List[float],
                     theta0: float, theta1: float,
                     flags: argparse.Namespace) -> Tuple[float, float]:
    """
    Train the model.
    """
    length = len(mileage)
    thetas = [[theta0, theta1]]
    for _ in range(flags.iterations):
        tmptheta0 = flags.learningRate * sum(
            [estimatePrice(theta0, theta1, mileage[i]) - price[i]
             for i in range(length)]) / length

        tmptheta1 = flags.learningRate * sum(
            [(estimatePrice(theta0, theta1, mileage[i]) - price[i]) *
             mileage[i] for i in range(length)]) / length

        theta0 -= tmptheta0
        theta1 -= tmptheta1
        thetas.append([theta0, theta1])

    return np.array(thetas)


def save_thetas(theta0: float, theta1: float):
    """
    Save thetas to the file.
    """
    try:
        with open('thetas', 'w') as f:
            f.write(f'{theta0}\n{theta1}\n')
    except PermissionError:
        print("Can't write thetas to file.")


def print_error(error: str):
    """
    Print error.
    """
    print(error)
    exit(1)


def denorm_thetas(thetas: List[List[float]],
                  coeff1: float, coeff0: float) -> List[float]:
    """
    Thetas denormalization.
    """
    if coeff1 == 0:
        coeff1 = 1
    return [[thetas[i][0] * coeff0, thetas[i][1] * coeff0 / coeff1]
            for i in range(len(thetas))]


if __name__ == '__main__':
    flags = parse_flags()

    if flags.learningRate <= 0 or flags.learningRate >= 1:
        print_error("Learning rate should be in range between 0.0 and 1.0.")

    if flags.iterations <= 1:
        print_error("Number of itertions must be > 1.")

    mileage, price = read_data('data.csv')
    mileage_norm, coeff1 = normilize_data(mileage)
    price_norm, coeff0 = normilize_data(price)
    theta0 = 0.0
    theta1 = 0.0
    if flags.warmStart and coeff0 != 0:
        theta0, theta1 = read_thetas()
        theta0 /= coeff0
        theta1 *= coeff1 / coeff0

    thetas = gradient_descent(mileage_norm, price_norm, theta0, theta1, flags)
    thetas = np.array(denorm_thetas(thetas, coeff1, coeff0))
    save_thetas(thetas[-1][0], thetas[-1][1])
    if flags.thetas:
        print_thetas(thetas[:, 0], flags, "₀")
        print_thetas(thetas[:, 1], flags, "₁")
    if flags.graph or flags.animation:
        print_graph(mileage, price, thetas, flags)
