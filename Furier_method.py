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

# a = 1  # constant from wave equation
l = 0.12  # length of the kernel
alpha = 1  # u(c,0)
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


def integral_square_of_norma(n):
    return integrate.quad(square_of_norma, 0, l, args=(n,))[0]


def function_to_integrate_in_a(x, n):
    return x ** 2 * beta_value(x, n)


def integral_for_a(n):
    summa = 0
    x_array = np.linspace(0, l, 1000)
    diff = x_array[1] - x_array[0]
    for x in x_array:
        summa += x ** 2 * beta_value(x, n) * diff
    return summa


def i1(x, n):
    arg = mu_value(n) / l * x
    first_bracket = ch(mu_value(n)) + cos(mu_value(n))
    return x ** 2 * first_bracket * sh(arg)


def i2(x, n):
    arg = mu_value(n) / l * x
    first_bracket = ch(mu_value(n)) + cos(mu_value(n))
    return x ** 2 * first_bracket * sin(arg)


def i3(x, n):
    arg = mu_value(n) / l * x
    third_bracket = sh(mu_value(n)) + sin(mu_value(n))
    return x ** 2 * third_bracket * ch(arg)


def i4(x, n):
    arg = mu_value(n) / l * x
    third_bracket = sh(mu_value(n)) + sin(mu_value(n))
    return x ** 2 * third_bracket * cos(arg)


def integral_of_four(n):
    return integrate.quad(i1, 0, l, args=(n,))[0] - integrate.quad(i2, 0, l, args=(n,))[0] - \
           integrate.quad(i3, 0, l, args=(n,))[0] + integrate.quad(i4, 0, l, args=(n,))[0]


def norma_with_summ(n):
    summa = 0
    x_array = np.linspace(0, l, 10000)
    diff = x_array[1] - x_array[0]
    for x in x_array:
        summa += beta_value(x, n) ** 2 * diff
    return summa


def a_coefficient(n):
    return alpha * integrate.quad(function_to_integrate_in_a, 0, l, args=(n,))[0] / integral_square_of_norma(n)


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
        n += 1
        # print(f'function {n} = {function}')
    # print(f'summ = {summa}')
    # print(f'{n} iterations for summ')
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


# get_figure(x=np.linspace(0, l, 100), t=np.linspace(0, 1, 2))
get_figure(x=np.linspace(0, l, 100), t=np.linspace(0, 1e-8, 100))
# j = 15
# print(integral_for_a(j))
# print(integrate.quad(function_to_integrate_in_a, 0, l, args=(j,))[0])
