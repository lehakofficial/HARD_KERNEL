###########
# Решение для простейшей задачи о колебании струны
# концы струны закреплены в точках x=0 и x=l
# в начальный момент времени в точке c=l/2 струну оттянули на h
# форма струны в начальной момент времени - парабола
###########

from math import pi
from math import cos
from math import sin
from math import sinh as sh
from math import cosh as ch
from scipy import integrate
import numpy as np
import plotly.graph_objs as go

a = 1  # constant from wave equation
l = 1  # length of the kernel
alpha = 0.01  # u(c,0)
accuracy = 1e-4

x_array = np.linspace(0, l, 1000)  # "x" array with 1000 elements from 0 to l


def mu_value(n):
    mu = np.array([1.875, 4.694, 7.854])
    if n < 4:
        n -= 1
        return mu[n]
    else:
        return pi / 2 * (2 * n - 1)


def hyperbolic_function(x, n):
    arg = mu_value(n) / l * x
    first_bracket = ch(mu_value(n)) + cos(mu_value(n))
    second_bracket = sh(arg) - sin(arg)
    third_bracket = sh(mu_value(n)) + sin(mu_value(n))
    fourth_bracket = ch(arg) - cos(arg)
    return alpha * x ** 2 * (first_bracket * second_bracket - third_bracket * fourth_bracket)


def a_coefficient(n):
    return 2 / l * integrate.quad(hyperbolic_function, 0, l, args=(n,))[0]


def b_coefficient(n):
    return 2 * l ** 2 / (a * mu_value(n) ** 2)


def answer(x, t, n):
    return hyperbolic_function(x, n) / (alpha * x ** 2) * (a_coefficient(n) * cos((mu_value(n) / l) ** 2 * a * t) +
                                                           b_coefficient(n) * cos((mu_value(n) / l) ** 2 * a * t))


def sum_of_n(x, t):
    """
    вычисляет сумму функции answer
    :return:
    """
    n = 1
    row_component = answer(x, t, n)
    # print(function)
    summa = 0
    while abs(row_component) > accuracy:
        summa += row_component
        n += 1
        row_component = answer(x, t, n)
        # print(f'function {n} = {function}')
    # print(f'summ = {summ}')
    # print(f'{n} iterations for summ')
    return summa


def u(x, t):
    """
    :param x: numppy array with x coordinateы
    :param t: time [s]
    :return: numpy array with u(x,t)
    """
    u_array = np.array([])
    for x_coordinate in x:
        u_array = np.append(u_array, sum_of_n(x_coordinate, t))
    return u_array


def get_figure(x, t):
    """

    :param x: numppy array with x coordinate
    :param t: time tuple
    :return:
    """
    fig = go.Figure()
    for time in t:
        fig.add_trace(go.Scatter(x=x, y=u(x, time), name=f't = {time} секунд'))
    fig.show()


get_figure(x=x_array, t=np.linspace(0, 1, 2))
# print(a_coefficient(3))
