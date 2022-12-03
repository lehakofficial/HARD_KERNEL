###########
# Решение для простейшей задачи о колебании струны
# концы струны закреплены в точках x=0 и x=l
# в начальный момент времени в точке c=l/2 струну оттянули на h
# форма струны в начальной момент времени - парабола
###########

from math import pi
from math import cos
from math import sin
import numpy as np
import plotly.graph_objs as go

a = 1   # constant from wave equation
l = 1   # length of the string
h = 0.01    # u(c,0)
accuracy = 1e-10

x_array = np.linspace(0, l, 1000)  # "x" array with 1000 elements from 0 to l


def cosinus(n, t):
    return cos(pi * (2 * n + 1) * a * t / l)


def sinus(n, x):
    return sin(pi * (2 * n + 1) * x / l)


def constant(n):
    return 32 * h / (pi * (2 * n + 1)) ** 3


def answer(x, t, n):
    return constant(n) * cosinus(n, t) * sinus(n, x)


def sum_of_n(x, t):
    """
    вычисляет сумму функции function
    :return:
    """
    n = 0
    function = answer(x, t, n)
    # print(function)
    summa = 0
    # TODO: check condition for function(n=0): вроде, работает
    while abs(function) > accuracy:
        summa += function
        n += 1
        function = answer(x, t, n)
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
    for i in x:
        u_array = np.append(u_array, sum_of_n(i, t))
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


get_figure(x=x_array, t=np.linspace(0, 1, 10))
