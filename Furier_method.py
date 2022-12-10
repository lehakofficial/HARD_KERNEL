import datetime
from math import pi
from math import cos
from math import sin
from math import sinh as sh
from math import cosh as ch
from scipy import integrate
import numpy as np
import plotly.graph_objs as go

# a = 1  # constant from wave equation
l = 0.12  # length of the kernel
alpha = 0.01  # u(c,0)
a = 2e11 * l ** 2 / (3 * 7800 * pi * 0.017)


def mu_value(n):
    mu = np.array([1.875, 4.694, 7.854])
    if n < 4:
        n -= 1
        return mu[n]
    else:
        return pi / 2 * (2 * n - 1)


def beta_value(x, n):
    arg = mu_value(n) / l * x
    first_bracket = ch(mu_value(n)) + cos(mu_value(n))
    second_bracket = sh(arg) - sin(arg)
    third_bracket = sh(mu_value(n)) + sin(mu_value(n))
    fourth_bracket = ch(arg) - cos(arg)
    return first_bracket * second_bracket - third_bracket * fourth_bracket


def square_of_norma(x, n):
    return beta_value(x, n) ** 2


def function_to_integrate_in_a(x, n):
    return x ** 2 * beta_value(x, n)


def a_coefficient(n):
    return alpha * integral[n-1] / integral_square_of_norma[n-1]


def answer(x, t, n):
    return beta_value(x, n) * a_coefficient(n) * cos((mu_value(n) / l) ** 2 * a * t)


def sum_of_n(x, t):
    """
    вычисляет сумму функции answer
    :return:
    """
    summa = 0
    for n in range(1, 8):
        summa += answer(x, t, n)
        # n += 1
    return summa


def u(x, t):
    """
    :param x: numppy array with x coordinateы
    :param t: time [s]
    :return: numpy array with u(x,t)
    """
    u_array = np.array([])
    n = 0
    for x_coordinate in x:
        u_array = np.append(u_array, sum_of_n(x_coordinate, t))
        n += 1
        print(n)
    return u_array


def get_figure(x, t):
    """

    :param x: numppy array with x coordinate
    :param t: iterable object with time values
    :return:
    """
    fig = go.Figure()
    for time in t:
        fig.add_trace(go.Scatter(x=x, y=u(x, time), name=f't = {time} секунд'))
    fig.show()


time_1 = datetime.datetime.now()
integral_square_of_norma = []
for i in range(1, 20):
    integral_square_of_norma.append(integrate.quad(square_of_norma, 0, l, args=(i,))[0])
integral = []
for i in range(1, 20):
    integral.append(integrate.quad(function_to_integrate_in_a, 0, l, args=(i,))[0])
get_figure(x=np.linspace(0, l, 100), t=np.linspace(0, 1, 10000))
print(datetime.datetime.now() - time_1)
