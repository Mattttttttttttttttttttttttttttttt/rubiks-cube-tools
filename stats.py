"""this module calculates the stats of a cstimer average"""

import re
import sys
import statistics

# HELP
HELP = {"length": "this is the number on the second line of your cstimer average.\n"\
                "e.g. avg of 100",
        "decimals": "does your individual time have 2 decimals or 3 decimals? "\
                "does your cstimer display milliseconds?",
        "+2": "does your average have a decent amount of +2s, or "\
                "+2 is very significant for this average?\n"\
                    "by saying yes you would gain access to the statistics:"\
                        "total +2s, +2 to range 1, +2 to range 2. (ranges will be determined soon)",
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
    return result

def integer(num) -> int:
    return int(num)

def find_all(parent: str | list, daughter: str) -> int:
    """count how many substrings is present in the parent string

    Args:
        parent (str/list): the parent string to search in
        daughter (str): the substring needing to be searched

    Returns:
        int: the count of how many substrings is present
    """
    count: int = 0
    if isinstance(parent, list):
        parent = list(parent)
        parent = deepjoin(parent, "")
    # while parent string contains daughter string
    while parent.find(daughter) != -1:
        # limit searching scope
        parent = parent[parent.find(daughter) + len(daughter):]
        count += 1
    return count

def deepjoin(lst: list, joiner: str) -> str:
    """returns a list joined with joiner

    Args:
        lst (list): the list to be joined
        joiner (str): the connector between elements

    Returns:
        str: the resultant string
    """
    lst = list(lst)
    for i, value in enumerate(lst):
        lst[i] = str(value)
    return joiner.join(lst)

def num_part(time: str) -> str:
    """extracts the decimal part of a string

    Args:
        time (str): string to be extracted

    Returns:
        str: decimal in string, minutes converted to seconds
    """
    return "".join([i for i in list(time) if (i.isdigit() or i == "." or i == ":")])

def no_brackets(time: str) -> str:
    """get rid of the bracket part in the input string

    Args:
        time (str): the string to be processed

    Returns:
        str: the resultant string without the bracket part
    """
    return re.compile(r"\[[a-zA-Z0-9 ]*\]").sub("", time)

def no_paren(time: str) -> str:
    """get rid of the parentheses part in the input string

    Args:
        time (str): the string to be processed

    Returns:
        str: the resultant string without the parentheses part
    """
    return re.compile(r"\(|\)").sub("", time)

def valid_num(num: int) -> str:
    """adds 0 before a one-digit number

    Args:
        num (int): number to be modified

    Returns:
        str: the resultant string
    """
    return str(num) if num >= 10 else "0" + str(num)

def minutes(a: str) -> float:
    """used for the min and max function to convert min:sec into seconds

    Args:
        a (str): the time in a string

    Returns:
        float: the converted time in seconds
    """
    a = num_part(a)
    if ":" in a:
        return float(a.split(":")[1]) + 60 * int(a.split(":", maxsplit=1)[0])
    else:
        return float(a)

def seconds(a: str | int) -> str:
    """converts a potential min:sec in string or integer back to a min:sec string

    Args:
        a (str/int): the string or integer to be converted (e.g. 60.67)

    Returns:
        str: a string of min:sec or the original float
    """
    if isinstance(a, int):
        return str(a) if a < 60 else f"{a // 60}:{valid_num(a % 60)}"
    if a[-1] == "+":
        a = float(a[:-1])
        dec: int = len(str(a).split(".")[1])
        return str(a) + "+" if a < 60 else f"{int(a // 60)}:{valid_num(round(a % 60, dec))}+"
    else:
        a = float(a)
        dec: int = len(str(a).split(".")[1])
        return str(a) if a < 60 else f"{int(a // 60)}:{valid_num(round(a % 60, dec))}"

def avg(solves: list, num_solves: int) -> float | str:
    """returns ao5

    Args:
        solves (list): solves
        num_solves (int): the length of the average

    Returns:
        float/str: average value
    """
    assert num_solves >= 3, "you cannot have an average with less than 3 solves"
    solves = keep(solves, ndnf)
    solves = [str(i) for i in solves]
    if len(solves) < num_solves - 1:
        return "DNF"
    elif len(solves) == num_solves - 1:
        solves.remove(min(solves, key=minutes))
        solves = [float(i) for i in solves]
        return round(sum(solves) / (num_solves - 2), DECIMALS)
    else:
        solves.remove(min(solves, key=minutes))
        solves.remove(max(solves, key=minutes))
        solves = [float(i) for i in solves]
        return round(sum(solves) / (num_solves - 2), DECIMALS)

def avg_compare(time: str | float) -> float:
    """compares averages

    Args:
        time (str/float): the avg

    Returns:
        float: the interpretation
    """
    return sys.maxsize if time == "DNF" else time

def frwrd(lst: list, start: int, value: int) -> list:
    """returns a list of *value* values frwrd in *lst* starting at *start* index

    Args:
        lst (list): list to be processed
        start (int): starting index
        value (int): number of values to go

    Returns:
        list: processed list
    """
    result = []
    for i in range(value):
        result.append(lst[start + i])
    return result

def repeat(lst: list) -> dict:
    """checks for any repeat in the list

    Args:
        lst (list): the list to be processed

    Returns:
        dict: a dictionary of repeat to the number of times it appeared
    """
    lst = sorted(keep(list(lst), ndnf))
    result: dict = {}
    count = 0
    for i, value in enumerate(lst):
        if i == len(lst) - 2:
            break
        if count != 0:
            count -= 1
            continue
        k = i
        while value == lst[k+1]:
            count += 1
            k += 1
        if count == 0:
            continue
        result[value] = count + 1
    return result

def keep(thing: str | list, funct) -> str | list:
    """keep the elements of thing that satisfy funct

    Args:
        thing (str/list): thing to filter from
        funct (function): filter function
        
    Returns:
        str/list: filtered thing
    """
    thing = list(thing)
    every = []
    for i in thing:
        if not funct(i):
            every.append(i)
    for i in every:
        thing.remove(i)
    return thing

def prths(a: str):
    return a[0] == "("

def nprths(a: str):
    return not a[0] == "("

def ndnf(a):
    return not "DNF" in a if isinstance(a, str) else True

def three_plus(a: float):
    return a >= CUT3

def number(a):
    return isinstance(a, float)



# CODE
print("hi there!\nthis program only supports cstimer\n"\
    "type \"help\" at any point to get help on the question!\n")
# get DATA
ao: str = input("your average of ... (paste as one line): ")
LENGTH: int = find_all(ao, ",") + 1
time_list: list[str] = [no_brackets(i) for i in ao.split("Time List:")[1].split(", ")]
parentheses: list[str] = [re.compile(r"\(|\)").sub("", i)
                          for i in keep(keep(time_list, ndnf), prths)]
r: list[float] = []  #refined list
for j in time_list:
    if ndnf(j):
        r.append(minutes(num_part(j)))
    else:
        r.append("DNF")
DECIMALS: int = len(num_part(time_list[0]).split(".")[1])

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
AVG1 = int(AVG1) if AVG1 else 5
AVG2: int = check("avg2", "length of second average you want to calculate (default 12): ",
                  [str(i) for i in (range(1, LENGTH + 1))], True)
AVG2 = int(AVG2) if AVG2 else 12


# HALF-CONSTANTS
p1 = {"**best single**:": "",
"**worst single**:": "",
"**best counting**:": "",
"**worst counting**:": "",
"**best ao5**:": "",
"**best ao12**:": "",
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
    f"**{CUT_1_TO_2}**:": 0,
    f"**{CUT_2_TO_3}**:": 0,
    f"**{CUT3}+s**:": 0}
repeats = {}


# p1
p1["**best single**:"] = min(parentheses, key=minutes)
p1["**worst single**:"] = no_paren(time_list[r.index(max(keep(r, ndnf)))])
#                                                   ^doesn't need minutes since r is list[float]
p1["**best counting**:"] = min(keep(time_list, nprths), key=minutes)
p1["**worst counting**:"] = max(keep(keep(time_list, nprths), ndnf), key=minutes)
p1["**best ao5**:"] = min([avg(frwrd(r, i, AVG1), AVG1) for i in range(LENGTH - AVG1)],
                          key = avg_compare)
p1["**best ao12**:"] = min([avg(frwrd(r, i, AVG2), AVG2) for i in range(LENGTH - AVG2)],
                           key = avg_compare)
p1["**standard deviation**:"] = round(statistics.stdev(keep(r, ndnf)), 2)


# p2
p2["**dnfs**:"] = find_all(time_list, "DNF")
p2["**didnt start timer dnfs**:"] = find_all(time_list, "DNF(0.001)"
                                             if DECIMALS == 3 else "DNF(0.01)")
if PLUS_TWO:
    p2["**+2s**:"] = find_all(time_list, "+")
DATA = deepjoin(time_list, "")
EXTRA = r"\d" if DECIMALS == 3 else ""
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
print("")
# p1
for key, val in p1.items():
    print(key, val)
# p2
print("## counts")
for key, val in p2.items():
    if val is not None:
        print(key, val)
# repeats

repeats = [f"{val + " " if val > 2 else ""}{key}{"s" if val > 2 else ""}"
           for key, val in repeat(r).items()]
print("\n**repeats:**", end = " ")
for j, val in enumerate(repeats):
    if j == len(repeats) - 1:
        print(val)
    else:
        print(val + ", ", end = "")
