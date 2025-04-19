"""generates correctly formatted average from multiple solves"""
from helpers import ndnf, num_part, find_all, seconds, minutes, avg, round_decimal

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
        solves (list[str]): the solves

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
            avg_val = round_decimal(solves, seconds(avg([minutes(i) for i in solves], num)))
            fastest_index = solves.index(min(solves, key=minutes))
            solves[fastest_index] = "**" + solves[fastest_index] + "**"
            return avg_val + " = " + ", ".join(solves)
    else: #avg
        delete = num // 20 + 1
        copy = list(solves)
        avg_val = round_decimal(solves, seconds(avg([str(minutes_dnf(i)) for i in solves], num)))
        for i in range(delete):
            add_parenthese(copy, solves)
        return avg_val + " = " + ", ".join(solves)




print('''\n"+" to +2 the previous solve,
"d" to dnf the previous solve,
"e" to reenter the previous time\n''')

length: int = 1
try:
    length = int(input("how many solves? "))
except KeyboardInterrupt:
    exit()
while length > 2:
    print("input your solves below:")
    average: list = []
    try:
        while len(average) < length:
            command = input()
            if command == "+":
                plus_two_solve(average)
                continue
            elif command == "d":
                dnf_solve(average)
                continue
            elif command == "e":
                del average[-1]
                continue
            average.append(command)
        print(avg_str(length, average))
    except KeyboardInterrupt:
        pass
    try:
        length = int(input("how many solves? "))
    except KeyboardInterrupt:
        exit()
