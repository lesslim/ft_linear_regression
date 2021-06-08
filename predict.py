import sys
from typing import Tuple


def estimatePrice(theta0: float, theta1: float, mileage: float) -> float:
    """
    Predict the price.
    """
    return theta0 + theta1 * mileage


def print_solution(mileage: float, theta0: float, theta1: float):
    """
    Calculate and print price.
    """
    price = estimatePrice(theta0, theta1, mileage)
    print("Prediction is:", price)
    if mileage < 0:
        print("But are you sure the car has driven negative kilometers?")


def read_thetas() -> Tuple[float, float]:
    """
    Reading thetas from the file.
    """
    try:
        with open("thetas", "r") as f:
            data = f.read().split("\n")
            theta0 = float(data[0])
            theta1 = float(data[1])
    except (FileNotFoundError, PermissionError, IndexError, ValueError):
        theta0 = 0.0
        theta1 = 0.0
    return theta0, theta1


if __name__ == '__main__':
    theta0, theta1 = read_thetas()
    args = sys.argv
    if len(args) == 1:
        print("Please enter mileage of the car:")
        try:
            mileage = float(input())
            print_solution(mileage, theta0, theta1)
        except ValueError:
            print("Doesn't look like a number of km.")
    elif len(args) == 2:
        try:
            mileage = float(args[1])
            print_solution(mileage, theta0, theta1)
        except ValueError:
            print("The argument must be a number of km.")
    else:
        print("Too many arguments.")
