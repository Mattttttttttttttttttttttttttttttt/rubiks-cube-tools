"""this module calculates the stats of a cstimer average"""

import re
import statistics
from helpers import no_brackets, keep, ndnf, prths, minutes, num_part, seconds, no_paren, frwrd
from helpers import avg_compare, find_all, deepjoin, repeat, nprths, number, avg

# HELP
HELP = {"length": "this is the number on the second line of your cstimer average.\n"\
                "e.g. avg of 100",
        "decimals": "does your individual time have 2 decimals or 3 decimals? "\
                "does your cstimer display milliseconds?",
        "+2": "does your average have a decent amount of +2s, or "\
                "+2 is very significant for this average?\n"\
                    "by saying yes you would gain access to the statistics:"\
                        "total +2s, un+2ed avg, +2 to range 1, +2 to range 2. (ranges will be determined soon)",
        "cut1": "this is the first cut. "\
                "you will be able to view how many solves are between this and the next cut, "\
                    "and if you selected \"view +2\", "\
                        "you can see how many solves in this range are +2s."\
                            "if your cut is OVER A MINUTE, put it in seconds, "\
                                "i.e. if your cut is 1:03, input 63",
        "cut2": "this is the second cut. "\
                "you will be able to view how many solves are between the previous and this cut, "\
                    "as well as between this and the next cut. "\
                        "and if you selected \"view +2\", "\
                            "you can see how many solves in these two range are +2s."\
                                "if your cut is OVER A MINUTE, put it in seconds, "\
                                    "i.e. if your cut is 1:03, input 63",
        "cut3": "this is the final cut. "\
                "you will be able to view how many solves are between the previous and this cut, "\
                    "and if you selected \"view +2\", "\
                        "you can see how many solves in this range are +2s.\n"\
                            "you can see how many solves are over this cut."\
                                "if your cut is OVER A MINUTE, put it in seconds, "\
                                    "i.e. if your cut is 1:03, input 63",
        "avg1": "you will be able to see the best ao-whatever-you-input. "\
                "for most people this is 5, meaning the programs calculates best ao5",
        "avg2": "you will be able to see the best ao-whatever-you-input. "\
                "for most people this is 12, meaning the programs calculates best ao12",
        }


# HELPER FUNCTIONS
def check(var: str, inquiry: str, cond, accept_empty: bool=False):
    """keep input()ing the user until the input satisfies the condition

    Args:
        var (str): the variable in a text to provide to help()
        inquiry (str): the text to display on the input()
        cond (list/function): the list the inputted value has to be in, 
                              or the function that should work on the variable
        accept_empty (bool): whether None is accepted as a reply
        
    Returns:
        _type_: the value to be assigned to the variable
    """
    try:
        if isinstance(cond, list):
            result = input(inquiry)
            while result not in cond and not (accept_empty and result == ""):
                if result == "help":
                    print(HELP[var])
                    result = input(inquiry)
                else:
                    result = input("don't think that's what I asked for, try again: ")
        else: #cond is a function
            a = True
            result = input(inquiry)
            while a:
                if not (accept_empty and result == ""):
                    break
                try:
                    if result == "help":
                        print(HELP[var])
                        result = input(inquiry)
                        break
                    cond(result)
                    a = False
                except ValueError:
                    result = input("don't think that's what I asked for, try again: ")
    except KeyboardInterrupt:
        exit()
    return result

def integer(num) -> int:
    return int(num)

def three_plus(a: float):
    return a >= CUT3



# CODE
print("hi there!\nthis program only supports cstimer\n"\
    "type \"help\" at any point to get help on the question!\n")
# get DATA
u = []
print("your average of ... (paste it in here): ")
try:
    for line in iter(input, "done"):
        u.append(line)
except KeyboardInterrupt:
    exit()
u = "".join(u).strip().split("avg of ")[1] # e.g. "100: 6.969\n\nTime List:\n..."
AVG_VAL: int | str = u.split(": ")[1].split("\n")[0] # e.g. 6.969 
ao: str = u.split("Time List:")[1]
time_list: list[str] = no_brackets(ao).split(", ")
LENGTH: int = len(time_list) # e.g. 100
parentheses: list[str] = [re.compile(r"\(|\)").sub("", i)
                          for i in keep(keep(time_list, ndnf), prths)]
first_un_paren: float = float(keep(time_list, nprths)[0])
            # first counted value in the avg, used as an inbetween
def smaller_than_first_un_paren(a: str) -> bool:
    return float(num_part(a)) < first_un_paren
BETTER_TRIM: int = len(keep(parentheses, smaller_than_first_un_paren))
WORSE_TRIM: int = len(keep(time_list, prths)) - BETTER_TRIM
r: list[float] = []  # refined list (DNF as "DNF", in seconds, no "+")
r_str: list[str] = []  # refined list but in str
for j in time_list:
    if ndnf(j):
        val = minutes(num_part(j))
        r.append(val)
        r_str.append(str(val))
    else:
        r.append("DNF")
        r_str.append("DNF")
DECIMALS: int = max([len(num_part(i).split(".")[1]) for i in time_list])

# get SETTINGS
print("")
PLUS_TWO: bool = True if check("+2", "yes or no: calculate +2s? ",
                               ["yes", "no"]) == "yes" else False
print(f"now put in an INTEGER for the questions below except for the ao{LENGTH}")
CUT1: int = int(minutes(check("cut1", "first cut: ", int)))
CUT2: int = int(minutes(check("cut2", "second cut: ", int)))
CUT3: int = int(minutes(check("cut3", "last cut (i.e. really bad times): ", int)))
AVG1: int = check("avg1", "length of first average you want to calculate (default 5): ",
                  [str(i) for i in (range(1, LENGTH + 1))], True)
if AVG1:
    AVG1 = int(AVG1)
elif LENGTH >= 5:
    AVG1 = 5
else:
    AVG1 = None
AVG2: int = check("avg2", "length of second average you want to calculate (default 12): ",
                  [str(i) for i in (range(1, LENGTH + 1))], True)
if AVG2:
    AVG2 = int(AVG2)
elif LENGTH >= 12:
    AVG2 = 12
else:
    AVG2 = None


# HALF-CONSTANTS
p1 = {"**best single**:": "",
"**worst single**:": "",
"**best counting**:": "",
"**worst counting**:": "",
f"**best ao{AVG1}**:": AVG1, #so this doesn't print if avg1 is None
f"**best ao{AVG2}**:": AVG2,
"**standard deviation**:": ""}
CUT1_min: float = seconds(str(CUT1))
CUT2_min: float = seconds(str(CUT2))
CUT3_min: float = seconds(str(CUT3))
# ^these are CUT's in seconds()
CUT_1_TO_2 = f"{CUT1_min}s" if CUT2 - CUT1 == 1 else f"{CUT1_min}-{CUT2_min}"
CUT_1_TO_2 = f"+2 to {CUT_1_TO_2}" if PLUS_TWO else CUT_1_TO_2
CUT_2_TO_3 = f"{CUT2_min}s" if CUT3 - CUT2 == 1 else f"{CUT2_min}-{CUT3_min}"
CUT_2_TO_3 = f"+2 to {CUT_2_TO_3}" if PLUS_TWO else CUT_2_TO_3
p2 = {"**dnfs**:": 0,
    "**didnt start timer dnfs**:": 0,
    "**+2s**:": None,
    f"**un+2ed ao{LENGTH}**:": None,
    f"**{CUT_1_TO_2}**:": 0,
    f"**{CUT_2_TO_3}**:": 0,
    f"**{CUT3}+s**:": 0}
repeats = {}


# p1
p1["**best single**:"] = no_paren(min(time_list, key=minutes))
p1["**worst single**:"] = no_paren(time_list[r.index(max(keep(r, ndnf)))])
#                                                   ^doesn't need minutes since r is list[float]
p1["**best counting**:"] = min(keep(keep(time_list, nprths), ndnf), key=minutes)
p1["**worst counting**:"] = max(keep(keep(time_list, nprths), ndnf), key=minutes)
if AVG1:
    p1[f"**best ao{AVG1}**:"] = min([avg(frwrd(r_str, i, AVG1), AVG1, DECIMALS)
                                     for i in range(LENGTH - AVG1)],
                              key = avg_compare)
if AVG2:
    p1[f"**best ao{AVG2}**:"] = min([avg(frwrd(r_str, i, AVG2), AVG2, DECIMALS)
                                     for i in range(LENGTH - AVG2)],
                               key = avg_compare)
p1["**standard deviation**:"] = seconds(str(round(statistics.stdev(keep(r, ndnf)), 2)))


# p2
p2["**dnfs**:"] = find_all(time_list, "DNF")
p2["**didnt start timer dnfs**:"] = find_all(time_list, "DNF(0.001)"
                                             if DECIMALS == 3 else "DNF(0.01)")
if PLUS_TWO:
    p2["**+2s**:"] = find_all(time_list, "+")
    if AVG_VAL == "DNF":
        p2[f"**un+2ed ao{LENGTH}**:"] = "DNF"
    else:
        unplus_2 = [] # DNFs as "DNF", +2s un+2ed, in seconds
        for i in time_list:
            if "DNF" in i:
                unplus_2.append("DNF")
            elif "+" in i:
                unplus_2.append(str(minutes(no_paren(i)[:-1]) - 2)) # un +2
            else: # a normal time
                unplus_2.append(str(minutes(no_paren(i))))
        unplus_2.sort(key=minutes)
        unplus_2 = unplus_2[BETTER_TRIM: len(unplus_2) - WORSE_TRIM]
        unplus_2 = [float(i) for i in unplus_2]
        p2[f"**un+2ed ao{LENGTH}**:"] = round(float(seconds(sum(unplus_2) / len(unplus_2))), DECIMALS)

DATA = deepjoin(time_list, "")
def keep_cut_1_2(a) -> bool:
    if a == "DNF":
        return False
    return CUT1 < a < CUT2
def keep_cut_2_3(a) -> bool:
    if a == "DNF":
        return False
    return CUT2 < a < CUT3
def keep_plus_cut_1_2(a) -> bool:
    if "+" in a:
        return CUT1 < float(minutes(num_part(a))) < CUT2
def keep_plus_cut_2_3(a) -> bool:
    if "+" in a:
        return CUT2 < float(minutes(num_part(a))) < CUT3
ONE_POINT = str(len(keep(r, keep_cut_1_2)))
TWO_POINT = str(len(keep(r, keep_cut_2_3)))
if PLUS_TWO:
    ONE_PLUS = str(len(keep(time_list, keep_plus_cut_1_2)))
    p2[f"**{CUT_1_TO_2}**:"] = ONE_PLUS + "/" + ONE_POINT
    TWO_PLUS = str(len(keep(time_list, keep_plus_cut_2_3)))
    p2[f"**{CUT_2_TO_3}**:"] = TWO_PLUS + "/" + TWO_POINT
else:
    p2[f"**{CUT_1_TO_2}**:"] = ONE_POINT
    p2[f"**{CUT_2_TO_3}**:"] = TWO_POINT
p2[f"**{CUT3}+s**:"] = len(keep(keep(r, number), three_plus))

# OUTPUT
print("\n## stats:\n**comments**: ")
# p1
for key, val in p1.items():
    print(key, val)
# p2
print("## counts")
for key, val in p2.items():
    if val is not None:
        print(key, val)
# repeats

repeats = [(str(val) + " " if val > 2 else "") + str(key) + ("s" if val > 2 else "")
           for key, val in repeat(r).items()]
print("\n**repeats:**", end = " ")
for j, val in enumerate(repeats):
    if j == len(repeats) - 1:
        print(val)
    else:
        print(val + ", ", end = "")
