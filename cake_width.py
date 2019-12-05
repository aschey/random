import math
from scipy.optimize import fsolve
def f(r, w, start):
    end = start + w
    return 2 * (math.sqrt(r**2 - end**2) * end + r**2 / 2 * math.asin(end/math.sqrt(r**2)))
def g(r, w, w_prev, start):
    return f(r, w, start) - f(r, w_prev, start - w_prev)

def h(r, w, w_prev, start, comp):
    return g(r, w, w_prev, start) - comp



radius = 100
w_start = 5
base = g(radius, w_start, 0, 0)
#print(base)
#print(g(radius, 0.25, 0.25, base))

w_prev = w_start
start = w_start
while True:
    try:
        w = fsolve((lambda test: h(radius, test, w_prev, start, base)), w_prev)
        start += w
        print("w=" + str(w))
        print("start=" + str(start))
        w_prev = w
    except ValueError:
        print(base)
        print(g(radius, radius - start, w_prev, start))
        break