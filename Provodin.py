import datetime
from math import pi
from math import cos
from math import sin
from scipy import integrate
import numpy as np
from math import exp
import plotly.graph_objs as go

# a = 1  # constant from wave equation
l = 1  # length of the kernel
a = 0.1
T = 10


def fi(x):
    if x == 0:
        return 0
    elif x == l:
        return 0
    else:
        return T


def function_to_integrate(x, n):
    return fi(x) * sin(pi * n * x / l)


def answer(x, t, n):
    return 4 * fi(x) / (pi * (2 * n - 1)) * sin(pi * (2 * n - 1) * x / l) / exp(a**2 * t * (pi * (2 * n - 1) / l)**2)


def sum_of_n(x, t):
    """
    вычисляет сумму функции answer
    :return:
    """
    summa = 0
    # n = 1
    # ans = answer(x, t, n)
    # while ans > 1e-8:
    #     summa += ans
    #     ans = answer(x, t, n)
    #     n += 1
    # return summa

    for n in range(1, 1000):
        try:
            summa += answer(x, t, n)
        except OverflowError:
            break
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
integral = []
for i in range(1, 100):
    integral.append(integrate.quad(function_to_integrate, 0, l, args=(i,))[0])
get_figure(x=np.linspace(0, l, 1000), t=np.linspace(0, 30, 61))
print(datetime.datetime.now() - time_1)
