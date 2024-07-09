"""generates correctly formatted average from multiple solves"""
import sys


def valid_num(num: int) -> str:
    """adds 0 before a one-digit number

    Args:
        num (int): number to be modified

    Returns:
        str: the resultant string
    """
    return str(num) if num >= 10 else "0" + str(num)


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


def ndnf(a)-> bool:
    """filters dnfs

    Args:
        a (str | any): the solve

    Returns:
        bool: whether it's a dnf
    """
    return not "DNF" in a if isinstance(a, str) else True


def num_part(time: str) -> str:
    """extracts the decimal part of a string

    Args:
        time (str): string to be extracted

    Returns:
        str: decimal in string, minutes converted to seconds
    """
    return "".join([i for i in list(time) if (i.isdigit() or i == "." or i == ":")])


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


def seconds(a: str | int) -> str:
    """converts a potential min:sec in string or integer back to a min:sec string

    Args:
        a (str/int): the string or integer to be converted (e.g. 60.67)

    Returns:
        str: a string of min:sec or the original float
    """
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


def avg(solves: list, num_solves: int, delete: int) -> float | str:
    """returns ao5

    Args:
        solves (list): solves (cannot be DNF average)
        num_solves (int): the length of the average
        delete (int): how many solves to trim

    Returns:
        float/str: average value
    """
    assert num_solves >= 2, "you cannot have an average with less than 2 solves"
    if num_solves == 3: #calculate mean
        return round(sum(solves) / num_solves, 3)
    # calculates average
    solves = [str(i) for i in solves]
    if len(keep(solves, ndnf)) >= num_solves - delete:
        for i in range(delete):
            trim(solves)
        solves = [float(i) for i in solves]
        return round(sum(solves) / (num_solves - 2), num_solves - 2 * delete)
    else:
        for i in range(delete):
            trim(solves)
        solves = [float(i) for i in solves]
        return round(sum(solves) / (num_solves - 2), num_solves - 2 * delete)


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


def add_parenthese(solves: list) -> list:
    """adds parentheses around the slowest and fastest solve once

    Args:
        solves (list): the original solves list

    Returns:
        list: the altered solves list
    """
    # referencing directly to solves because we need to directly alter it
    fastest_index = solves.index(min(solves, key=minutes))
    solves[fastest_index] = "(" + solves[fastest_index] + ")"
    slowest_index = solves.index(max(solves, key=minutes))
    solves[slowest_index] = "(" + solves[slowest_index] + ")"


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
        if dnfs > 1:
            for i in range(round(num/20) + 1):
                add_parenthese(solves)
            return "DNF = " + ", ".join(solves)
        else:
            delete = round(num/20) + 1
            avg_val = seconds(avg([minutes_dnf(i) for i in solves], num, delete))
            for i in range(delete):
                add_parenthese(solves)
            return avg_val + " = " + ", ".join(solves)


length: int = int(input("how many solves? "))
print("input your solves below:")
average: list = []
for j in range(length):
    average.append(input())
print(avg_str(length, average))
