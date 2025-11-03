"""this module takes an aoxx and return a list of aoxs in the aoxx"""
# this could also be used in conjunction with less_than_x.py to calculate
# how many rolling average is sub a certain time
import sys
from helpers import avg, no_brackets, minutes, num_part, ndnf, check, frwrd, no_multiphase

# HELPER FUNCTIONS
def no_dnf_max(lst: list) -> float:
    """returns a list's maximum, skipping over strings

    Args:
        lst (list: float | str): list of floats and strings

    Returns:
        float: maximum of the floats
    """
    maximum: float = lst[0]
    for time in lst:
        if isinstance(time, float) and time > maximum:
            maximum = time
    return maximum

# code
u = []
print("your full average of ... (just paste it in here, \"done\" once done): ")
try:
    for line in iter(input, "done"):
        u.append(line)
except KeyboardInterrupt:
    exit()
u = "".join(u).strip().split("avg of ")[1] # e.g. "100: 6.969\n\nTime List:\n..."
ao: str = u.split("Time List:")[1]
time_list: list[str] = no_multiphase(no_brackets(ao)).split(", ")
LENGTH: int = len(time_list) # e.g. 100
DECIMALS: int = max([len(num_part(i).split(".")[1]) for i in time_list])
r: list[str] = []  # refined list (DNF as "DNF", in seconds, no "+") in str
for j in time_list:
    if ndnf(j):
        val = minutes(num_part(j))
        r.append(str(val))
    else:
        r.append("DNF")

AVG = int(check("how long of an avg to split: ", int))
avg_list: list = [avg(frwrd(r, i, AVG), AVG, DECIMALS) for i in range(LENGTH - AVG)]
for i, val in enumerate(avg_list): # undo avg()'s sys.maxsize to means
    if val == sys.maxsize:
        avg_list[i] = "DNF"

print(avg_list)
