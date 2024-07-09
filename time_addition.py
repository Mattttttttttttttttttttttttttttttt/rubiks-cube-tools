"""this module adds time"""

# imports
def num_part(time: str) -> str:
    """extracts the decimal part of a string

    Args:
        time (str): string to be extracted

    Returns:
        str: decimal in string, minutes converted to seconds
    """
    return "".join([i for i in list(time) if (i.isdigit() or i == "." or i == ":")])

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

def seconds(a: float) -> str:
    """converts a potential min:sec in string or integer back to a min:sec string

    Args:
        a (float): the string or integer to be converted (e.g. 60.67)

    Returns:
        str: a string of min:sec or the original float
    """
    a = str(a)
    if a[-1] == "+":
        a = float(a[:-1])
        dec: int = len(str(a).split(".")[1])
        return str(a) + "+" if a < 60 else f"{int(a // 60)}:{valid_num(round(a % 60, dec))}+"
    else:
        a = float(a)
        dec: int = len(str(a).split(".")[1])
        return str(a) if a < 60 else f"{int(a // 60)}:{valid_num(round(a % 60, dec))}"

# code
data: list[str] = []
data.append(input())
while data[-1] != "":
    data.append(input())
del data[-1]
print(seconds(round(sum([minutes(i) for i in data]), 2)))
