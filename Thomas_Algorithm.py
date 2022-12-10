import numpy as np
import plotly.graph_objs as go
from math import pi

alpha = 0.01
a = 1
h = 1e-4
tau = 1e-8
l = 0.12
t = 1e-4
N = int(t / tau + 1)
M = int(l / h + 1)
t_arr = np.linspace(0, t, N)
x_arr = np.linspace(0, l, M)

y = np.zeros((N, M))

# c = 1
c = 0.01
# c = a ** 2 * tau ** 2 / h ** 4
# Filling the 0th and 1st row using initial conditions

for i in range(M):
    y[0:2, i] = alpha * x_arr[i] ** 2
# Filling the 0th and 1st column using boundary conditions
# i = 0
# for t in t_arr:
#     y[i, 0:2] = 0
#     i += 1

for n in range(N-2):
    for i in range(2, M-1):
        if i == M-2:
            y[n+2, i] = 2 * y[n+2, i-1] - y[n+2, i-2]
            y[n+2, i+1] = 3 * y[n+2, i-1] - 2 * y[n+2, i-2]
        else:
            y[n+2, i] = 2 * y[n+1, i] - (6 * c + 1) * y[n, i] + c * (4 * y[n, i+1] + 4 * y[n, i-1] - y[n, i-2] - y[n, i+2])
print('cringe')
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_arr, y=y[200], name=f't = {2} секунд'))
fig.add_trace(go.Scatter(x=x_arr, y=y[0], name=f't = {2} секунд'))
fig.show()
