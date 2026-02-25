"""this module calculates how many values of a csv (can have [] and + and DNF) 
(could be from cstimer) is sub a certain value"""
# this could also be used in conjunction with aox_list.py to calculate
# how many rolling average is sub a certain time

import sys
from helpers import num_part, no_brackets, minutes, ndnf, check, keep, no_multiphase

U = []
print("your average of ... (paste it in here (only times, no text, separated by \", \")): ")
try:
    for line in iter(input, "done"):
        U.append(line)
except KeyboardInterrupt:
    sys.exit()
U = "".join(U).strip() # e.g. "100: 6.969\n\nTime List:\n..."
time_list: list[str] = no_multiphase(no_brackets(U)).split(", ")
LENGTH: int = len(time_list) # e.g. 100
DECIMALS: int = max(len(num_part(i).split(".")[1]) if "." in i
                     else 0 for i in time_list)
r: list[float] = []  # refined list (DNF as 10000, in seconds, no "+") in float/int
for j in time_list:
    if ndnf(j):
        r.append(minutes(num_part(j)))
    else:
        r.append(sys.maxsize)

cut = float(check("cutoff: ", float))
print(str(len(keep(r, lambda a: a < cut))) + "/" + str(len(r)))
