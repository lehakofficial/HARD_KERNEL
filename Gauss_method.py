import numpy as np
import plotly.graph_objs as go
l = 1
a = 1
alpha = 0.01
h = 0.01
tau = 0.0001
M = 101
N = 101
f = np.array([])
consts = np.array([0, 0, 0, 0, 0])
x_arr = np.linspace(0, l, M)




answers = np.array([1, 3])
coefs = np.array([[2, 5], [1, -10]])
print(np.linalg.solve(coefs, answers))
