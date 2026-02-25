"""generates correctly formatted mean from multiple solves"""
import statistics
from helpers import ndnf, keep, num_part

u = []
try:
    for line in iter(input, ""):
        u.append(line)
except KeyboardInterrupt:
    exit()
times = ", ".join(u)
if len(keep(u, ndnf)) == len(u):
    u = [float(num_part(i)) for i in u]
    print(round(statistics.mean(u), 3), "=", times)
else:
    print("DNF =", times)
