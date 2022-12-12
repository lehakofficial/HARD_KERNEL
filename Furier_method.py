import datetime
from math import pi
from math import cos
from math import sin
from math import sinh as sh
from math import cosh as ch
from scipy import integrate
import numpy as np
import plotly.graph_objs as go

alpha = 0.01
length = 1  # length of the kernel
a = 1
time = 1  # time for modeling
h = 1e-2  # x-axis step of the mesh
tau = 1e-2  # time step of the mesh
M = int(length / h) + 1  # amount of x-axis nodes of the mesh : 11 now
N = int(time / tau) + 1  # amount of time nodes of the mesh : 11 now

integral_square_of_norma = []
integral = []


def mu_value(n):
    """
    Function for calculation mu with n number

    :param n: number of mu
    :return: mu n
    """
    mu = np.array([1.875, 4.694, 7.854])
    if n < 4:
        n -= 1
        return mu[n]
    else:
        return pi / 2 * (2 * n - 1)


def beta_value(x, n):
    """
    Function for calculation beta with n number in spot x

    :param x: x-coordinate
    :param n: number of beta
    :return: beta n
    """
    arg = mu_value(n) / length * x
    first_bracket = ch(mu_value(n)) + cos(mu_value(n))
    second_bracket = sh(arg) - sin(arg)
    third_bracket = sh(mu_value(n)) + sin(mu_value(n))
    fourth_bracket = ch(arg) - cos(arg)
    return first_bracket * second_bracket - third_bracket * fourth_bracket


def square_of_norma(x, n):
    """
    Function to be integrated in square of norma

    :param x: x-coordinate
    :param n: number of beta
    :return: value of integrated function in spot x and number n
    """
    return beta_value(x, n) ** 2


def function_to_integrate_in_a(x, n):
    """
    Function to be integrated in A coefficient

    :param x: x-coordinate
    :param n: number of beta
    :return: value of integrated function in spot x and number n
    """
    return x ** 2 * beta_value(x, n)


def sum_of_n(x, t):
    """
    Function for calculation of the row

    :param x: x-coordinate
    :param t: time value [s]
    :return: value of the row
    """
    summa = 0
    for n in range(1, 10):
        a_coefficient = alpha * integral[n-1] / integral_square_of_norma[n-1]
        summa += beta_value(x, n) * a_coefficient * cos((mu_value(n) / length) ** 2 * a * t)
    return summa


def u(x, t):
    """
    Function for calculation of the u(x, t)

    :param x: numpy array with x-coordinates
    :param t: time [s]
    :return: numpy array with u(x,t)
    """
    u_array = np.array([])
    n = 0
    for x_coordinate in x:
        u_array = np.append(u_array, sum_of_n(x_coordinate, t))
        n += 1
        print(f'{n} / {N}')
    return u_array


def get_figure(x, t):
    """
    Function for getting plotly plot

    :param x: numpy array with x-coordinates
    :param t: numpy array with time values
    """

    fig = go.Figure()
    for time_value in t:
        fig.add_trace(go.Scatter(x=x, y=u(x, time_value), name=f't = {time_value} секунд'))
    fig.update_layout(title="Аналитическое решение",
                      xaxis_title="x, м",
                      yaxis_title="y, м",
                      margin=dict(l=0, r=30, t=30, b=0))
    fig.show()


def calculate_integrals(square_of_norma_list, integral_list):
    """
    Function for calculation integrals

    :param square_of_norma_list: list for square of norma values
    :param integral_list: list of integral values
    """

    for i in range(1, 20):
        integral_square_of_norma.append(integrate.quad(square_of_norma, 0, length, args=(i,))[0])
    for i in range(1, 20):
        integral.append(integrate.quad(function_to_integrate_in_a, 0, length, args=(i,))[0])


time_1 = datetime.datetime.now()
calculate_integrals(integral_square_of_norma, integral)
get_figure(x=np.linspace(0, length, M), t=np.linspace(0, time, N))
print(datetime.datetime.now() - time_1)
