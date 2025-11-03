"""this module is a helper module"""

import re
import sys


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
    """returns a list converted into strs and joined with joiner

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
    return re.sub(r"\[.*?\]", "", time)

def no_multiphase(time: str) -> str:
    """get rid of the equal sign part in the input string

    Args:
        time (str): the string to be processed

    Returns:
        str: the resultant string without the equal sign part
    """
    result = re.sub(r"=.*?\,", ",", time)
    return re.sub(r"=.*?$", "", result)

def no_paren(time: str) -> str:
    """get rid of the parentheses part in the input string

    Args:
        time (str): the string to be processed

    Returns:
        str: the resultant string without the parentheses part
    """
    return re.compile(r"\(|\)").sub("", time)

def valid_num(num: int | float) -> str:
    """adds 0 before a one-digit number

    Args:
        num (int/float): number to be modified

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
    if "DNF" in a:
        return sys.maxsize
    a = num_part(a)
    if ":" in a:
        return round(float(a.split(":")[1]) + 60 * int(a.split(":", maxsplit=1)[0]),
                     len(a.split(".")[1]))
    else:
        return float(a)

def seconds(a: str | float | int) -> str:
    """converts a potential min:sec in string or float back to a min:sec string

    Args:
        a (str/float/int): the string or integer to be converted (e.g. 60.67)

    Returns:
        str: a string of min:sec or the original float
    """
    if a == "DNF":
        return a # type: ignore
    if isinstance(a, int):
        return str(a) if a < 60 else f"{a // 60}:{valid_num(a % 60)}"
    a = str(a)
    if a[-1] == "+":
        a = float(a[:-1])
        dec: int = len(str(a).split(".")[1])
        return str(a) + "+" if a < 60 else f"{int(a // 60)}:{valid_num(round(a % 60, dec))}+"
    else:
        a = float(a)
        dec: int = len(str(a).split(".")[1])
        return str(a) if a < 60 else f"{int(a // 60)}:{valid_num(round(a % 60, dec))}"

def round_decimal(solves: list, avg_val: str) -> str:
    """rounds the avg of solves to the maximum decimal present in the solves

    Args:
        solves (list[str]): the list of solves
        avg_val (str): a string of the time of the average

    Returns:
        str: a rounded string of the time of the average
    """
    if avg_val == "DNF": # dont mess with decimals if its DNF
        return avg_val
    decimals_of_solves = []
    for i in solves:
        decimals_of_solves.append(len(num_part(i).split(".")[1]) if "." in i else 0)
    decimals = max(decimals_of_solves)
    if decimals == 0: # no decimals (FMC maybe)
        decimals = 2
    current_dec = len(avg_val.split(".")[1]) if "." in avg_val else 0
    if current_dec == decimals:
        return avg_val
    elif current_dec > decimals: # need to round
        # return avg_val[: decimals - current_dec]
        avg_val = seconds(round(minutes(avg_val), decimals))
    # potentially need to add 0s, not else: because round can truncate trailing 0s
    current_dec = len(avg_val.split(".")[1]) if "." in avg_val else 0
    if current_dec == 0: # need decimal point as well
        avg_val += "."
    return avg_val + "0" * (decimals - current_dec)

# def avg(solves: list, num_solves: int, decimals: int) -> float | str:
#     """returns ao5

#     Args:
#         solves (list[str]): solves
#         num_solves (int): the length of the average
#         decimals (int): the amount of decimals

#     Returns:
#         float/str: average value
#     """
#     assert num_solves >= 3, "you cannot have an average with less than 3 solves"
#     solves = keep(solves, ndnf)
#     if len(solves) < num_solves - 1: # more than 1 DNF
#         return "DNF"
#     elif len(solves) == num_solves - 1: # one DNF
#         solves.remove(min(solves, key=minutes))
#         solves = [float(i) for i in solves]
#         return round(sum(solves) / (num_solves - 2), decimals)
#     else: # no DNFs
#         solves.remove(min(solves, key=minutes))
#         solves.remove(max(solves, key=minutes))
#         solves = [float(i) for i in solves]
#         return round(sum(solves) / (num_solves - 2), decimals)

def avg(solves: list, num_solves: int, decimals: int = 0) -> float | str:
    """returns average of num_solves

    Args:
        solves (list[str]): solves in seconds with DNFs as DNFs
        num_solves (int): the length of the average
        decimals (int): the amount of decimals, if not provided, no rounding will be done

    Returns:
        float/str: average value
    """
    delete = num_solves // 20 + 1
    assert num_solves > 2, "you cannot have an average with less than 3 solves"
    if num_solves == 3: #calculate mean
        if "DNF" in solves:
            return sys.maxsize
        copy = [float(i) for i in solves] # solves in float
        if decimals:
            return round(sum(copy) / num_solves, decimals)
        else: # no rounding
            return sum(copy) / num_solves
    # calculates average
    # solves = [str(i) for i in solves]
    if len(keep(solves, ndnf)) >= num_solves - delete:
        copy = list(solves)
        for i in range(delete):
            trim(copy)
        copy = [float(i) for i in copy] # solves in float
        if decimals:
            return round(sum(copy) / (num_solves - 2 * delete), decimals)
        else: # no rounding
            return sum(copy) / (num_solves - 2 * delete)
    else:
        return "DNF"

def avg_compare(time: str | float) -> float:
    """compares averages

    Args:
        time (str/float): the avg

    Returns:
        float: the interpretation
    """
    return sys.maxsize if time == "DNF" else time # type: ignore

def trim(solves: list) -> None:
    """trims the slowest and fastest solve once

    Args:
        solves (list): the original solves list, trimmed directly
    """
    # referencing directly to solves because we need to directly alter it
    solves.remove(min(solves, key=minutes))
    solves.remove(max(solves, key=minutes))

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

def check(inquiry: str, cond, accept_empty: bool=False):
    """keep input()ing the user until the input satisfies the condition

    Args:
        inquiry (str): the text to display on the input()
        cond (list/function): the list the inputted value has to be in, 
                              or the function that should work on the variable
        accept_empty (bool): whether None is accepted as a reply
        
    Returns:
        the value to be assigned to the variable
    """
    try:
        if isinstance(cond, list):
            result = input(inquiry)
            while result not in cond and not (accept_empty and result == ""):
                result = input("don't think that's what I asked for, try again: ")
        else: #cond is a function
            a = True
            result = input(inquiry)
            while a:
                if not (accept_empty and result == ""):
                    break
                try:
                    cond(result)
                    a = False
                except ValueError:
                    result = input("don't think that's what I asked for, try again: ")
    except KeyboardInterrupt:
        exit()
    return result

def keep(thing: list, funct) -> list:
    """keep the elements of thing that satisfy funct

    Args:
        thing (str/list): thing to filter from
        funct (function): filter function
        
    Returns:
        str/list: filtered thing
    """
    return list(filter(funct, thing))

def prths(a: str)-> bool:
    """used for the keep function to keep all solves with parentheses

    Args:
        a (str): the string to be analyzed

    Returns:
        bool: whether a starts with a parenthese
    """
    return a[0] == "("

def nprths(a: str)-> bool:
    """used for the keep function to keep all solves without parentheses

    Args:
        a (str): the string to be analyzed

    Returns:
        bool: whether a starts without a parenthese
    """
    return not a[0] == "("

def ndnf(a)-> bool:
    """filters out dnfs

    Args:
        a (str | any): the solve

    Returns:
        bool: whether it's a dnf
    """
    return not "DNF" in a if isinstance(a, str) else True

def ydnf(a) -> bool:
    """filters out non-dnfs

    Args:
        a (str | any): the solve

    Returns:
        bool: whether it's a non-dnf
    """
    return "DNF" in a if isinstance(a, str) else False
