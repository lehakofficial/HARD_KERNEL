import numpy as np
import plotly.graph_objs as go

a = 1
alpha = 1
length = 1  # length of the kernel
t = 0.1  # time for modeling
h = 0.1  # x-axis step of the mesh
tau = 0.01  # time step of the mesh
M = int(length / h) + 1  # amount of x-axis nodes of the mesh : 11 now
y = np.array([])  # array with y(n, i) values
N = int(t / tau) + 1  # amount of time nodes of the mesh : 11 now

# matrix coefficients
A = a ** 2 * tau ** 2 / h ** 4  # TODO: replace with 1 to avoid errors
B = - 4 * A
C = 1 + 6 * A
D = - 4 * A
E = A

# filling array with initial conditions y(0, x) = alpha * x ** 2
for i in range(M):  # M iterations for M nodes of the mesh
    y = np.append(y, alpha * (h * i) ** 2)  # TODO: replace "h * i" with array with calculated values
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
            f = 0
        else:
            f = 2 * y[n - 1, i] - y[n - 2, i]
        free_members_column = np.append(free_members_column, f)  # TODO: replace "f" with expression

    # fill SLAE matrix
    for i in range(M):
        matrix_row = np.zeros((1, M))
        if i == 0:  # using boundary condition
            slae_matrix[0, i] = 1
            continue
        elif i == 1:    # using boundary condition
            matrix_row[0, i] = 1
        elif 1 < i < M - 2:
            matrix_row[0, i - 2] = A
            matrix_row[0, i - 1] = B
            matrix_row[0, i] = C
            matrix_row[0, i + 1] = D
            matrix_row[0, i + 2] = E
        elif i == M - 2:    # using boundary condition
            matrix_row[0, i - 1] = 1
            matrix_row[0, i] = -2
            matrix_row[0, i + 1] = 1
        else:   # using boundary condition
            matrix_row[0, i - 3] = -1
            matrix_row[0, i - 2] = 3
            matrix_row[0, i - 1] = -3
            matrix_row[0, i] = 1
        slae_matrix = np.vstack((slae_matrix, matrix_row))
    solvation = np.linalg.solve(slae_matrix, free_members_column)
    y[n] = solvation

fig = go.Figure()
for n in range(N):
    fig.add_trace(go.Scatter(x=np.linspace(0, length, M), y=y[n], name=f't = {n * h} секунд'))
fig.show()
print()
