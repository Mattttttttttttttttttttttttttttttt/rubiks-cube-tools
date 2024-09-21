"""generates correctly formatted average from multiple solves"""
import sys
from helpers import ndnf, num_part, keep, find_all, seconds


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
        return float(a.split(":")[1]) + 60 * int(a.split(":", maxsplit=1)[0])
    else:
        return float(a)


def minutes_dnf(a: str) -> float | str:
    """used for the min and max function to convert min:sec into seconds

    Args:
        a (str): the time in a string

    Returns:
        float | str: the converted time in seconds or the original DNF
    """
    if "DNF" in a:
        return a
    a = num_part(a)
    if ":" in a:
        return float(a.split(":")[1]) + 60 * int(a.split(":", maxsplit=1)[0])
    else:
        return float(a)

def plus_two_solve(lst: list) -> None:
    """plus two the last solve in the list

    Args:
        lst (list): list of solves
    """
    if not ndnf(lst[-1]):
        lst[-1] = seconds(minutes(num_part(lst[-1])) + 2) + "+"
    elif lst[-1][-1] == "+":
        pass
    else:
        lst[-1] = seconds(minutes(lst[-1]) + 2) + "+"

def dnf_solve(lst: list) -> None:
    """dnf the last solve in the list

    Args:
        lst (list): list of solves
    """
    if not ndnf(lst[-1]):
        pass
    elif lst[-1][-1] == "+":
        lst[-1] = "DNF(" + seconds(minutes(num_part(lst[-1])) - 2) + ")"
    else:
        lst[-1] = "DNF(" + lst[-1] + ")"

def avg(solves: list, num_solves: int, delete: int) -> float | str:
    """returns ao5

    Args:
        solves (list): solves (cannot be DNF average)
        num_solves (int): the length of the average
        delete (int): how many solves to trim

    Returns:
        float/str: average value
    """
    assert num_solves > 2, "you cannot have an average with less than 3 solves"
    if num_solves == 3: #calculate mean
        return round(sum(solves) / num_solves, 3)
    # calculates average
    solves = [str(i) for i in solves]
    if len(keep(solves, ndnf)) >= num_solves - delete:
        for i in range(delete):
            trim(solves)
        solves = [float(i) for i in solves]
        return round(sum(solves) / (num_solves - 2 * delete), 3)
    else:
        for i in range(delete):
            trim(solves)
        solves = [float(i) for i in solves]
        return round(sum(solves) / (num_solves - 2 * delete), 3)


def trim(solves: list) -> list:
    """trims the slowest and fastest solve once

    Args:
        solves (list): the original solves list

    Returns:
        list: the trimmed solves list
    """
    # referencing directly to solves because we need to directly alter it
    solves.remove(min(solves, key=minutes))
    solves.remove(max(solves, key=minutes))


def add_parenthese(copy: list, solves: list) -> list:
    """adds parentheses around the slowest and fastest solve once

    Args:
        copy (list): a copy of the list
        solves (list): the original solves list

    Returns:
        list: the altered solves list
    """
    # referencing directly to solves because we need to directly alter it
    fastest = copy.pop(copy.index(min(copy, key=minutes)))
    solves[solves.index(fastest)] = "(" + solves[solves.index(fastest)] + ")"
    slowest = copy.pop(copy.index(max(copy, key=minutes)))
    solves[solves.index(slowest)] = "(" + solves[solves.index(slowest)] + ")"


def avg_str(num: int, solves: list) -> str:
    """generates correctly formatted aoxxx from xxx solves

    Args:
        num (int): the number of solves
        solves (list): the solves

    Returns:
        str: the formatted avg
    """
    dnfs = find_all("".join(solves), "DNF")
    if num == 3: #mean
        if dnfs > 0:
            if dnfs != 3:
                fastest_index = solves.index(min(solves, key=minutes))
                solves[fastest_index] = "**" + solves[fastest_index] + "**"
            return "DNF = " + ", ".join(solves)
        else: #no dnf
            avg_val = seconds(avg([minutes(i) for i in solves], num, 0))
            fastest_index = solves.index(min(solves, key=minutes))
            solves[fastest_index] = "**" + solves[fastest_index] + "**"
            return avg_val + " = " + ", ".join(solves)
    else: #avg
        delete = num // 20 + 1
        if dnfs > 1:
            copy = list(solves)
            for i in range(delete):
                add_parenthese(copy, solves)
            return "DNF = " + ", ".join(solves)
        else:
            copy = list(solves)
            avg_val = seconds(avg([minutes_dnf(i) for i in solves], num, delete))
            for i in range(delete):
                add_parenthese(copy, solves)
            return avg_val + " = " + ", ".join(solves)
length: int = 1
try:
    length = int(input("how many solves? "))
except KeyboardInterrupt:
    exit()
while length > 2:
    print("input your solves below:")
    average: list = []
    try:
        j = 0
        while j < length:
            command = input()
            if command == "+":
                plus_two_solve(average)
                continue
            elif command == "d":
                dnf_solve(average)
                continue
            average.append(command)
            j += 1
        print(avg_str(length, average))
    except KeyboardInterrupt:
        pass
    try:
        length = int(input("how many solves? "))
    except KeyboardInterrupt:
        exit()
