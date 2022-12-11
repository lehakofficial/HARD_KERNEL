import numpy as np
import plotly.graph_objs as go
from math import pi

alpha = 0.01
length = 1  # length of the kernel
a = 1
t = 1  # time for modeling
h = 1e-2  # x-axis step of the mesh
tau = 1e-1  # time step of the mesh
M = int(length / h) + 1  # amount of x-axis nodes of the mesh : 11 now
y = np.array([])  # array with y(n, i) values
N = int(t / tau) + 1  # amount of time nodes of the mesh : 11 now

# matrix coefficients
A = a ** 2 * tau ** 2 / h ** 4  # TODO: replace with 1 to avoid errors
B = - 4 * A
C = 1 + 6 * A
D = - 4 * A
E = A
x_arr = np.linspace(0, length, M)

# filling array with initial conditions y(0, x) = alpha * x ** 2
for i in range(M):  # M iterations for M nodes of the mesh
    y = np.append(y, alpha * x_arr[i] ** 2)
y = np.vstack((y, y))
y[1, 1] = 0 # use initial condition for y(1,1)
y = np.vstack((y, np.zeros((N - 2, M))))  # array with initial conditions, boundary conditions and zeroes NxM now: 11x11

for n in range(2, N):
    # matrix creation
    slae_matrix = np.zeros((1, M))  # matrix of the system of the linear algebraic equations
    free_members_column = np.array([])  # column of the free members of the system of the linear algebraic equations
    # fill column of the free members
    for i in range(M):  # M unknown and M equations
        if i < 2 or i > M - 3:  # using the initial and boundary conditions
            free_members_column = np.append(free_members_column, 0)
        else:
            free_members_column = np.append(free_members_column, 2 * y[n - 1, i] - y[n - 2, i])

    # fill SLAE matrix
    for i in range(M):
        matrix_row = np.zeros((1, M))
        if i == 0:  # using boundary condition #1
            slae_matrix[0, i] = 1
            continue
        elif i == 1:    # using boundary condition #2
            matrix_row[0, i] = 1
        elif 1 < i < M - 2:
            matrix_row[0, i - 2] = A
            matrix_row[0, i - 1] = B
            matrix_row[0, i] = C
            matrix_row[0, i + 1] = D
            matrix_row[0, i + 2] = E
        elif i == M - 2:    # using boundary condition #3
            matrix_row[0, i - 1] = 1
            matrix_row[0, i] = -2
            matrix_row[0, i + 1] = 1
        else:   # using boundary condition #4
            matrix_row[0, i - 3] = -1
            matrix_row[0, i - 2] = 3
            matrix_row[0, i - 1] = -3
            matrix_row[0, i] = 1
        slae_matrix = np.vstack((slae_matrix, matrix_row))
    y[n] = np.linalg.solve(slae_matrix, free_members_column)
    print(f'{n} / {N}')

fig = go.Figure()
for n in range(N):
    fig.add_trace(go.Scatter(x=x_arr, y=y[n], name=f't = {n * tau} секунд'))
fig.show()
