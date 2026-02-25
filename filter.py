"""this module filters out cube explorer raw algs by certain moves"""

import itertools

def deasteriskize_str(original: str) -> list:
    """expand asterisk notation

    Args:
        original (str): one filter to be expanded

    Returns:
        list: the expanded list
    """
    # this function is generated with ChatGPT

    # Find the positions of all asterisks
    asterisk_positions = [j for j, char in enumerate(original) if char == '*']
    num_asterisks = len(asterisk_positions)

    # Define the possible replacements
    replacements = ["", "'", "2"]

    # Generate all combinations of replacements for the asterisks
    combinations = list(itertools.product(replacements, repeat=num_asterisks))

    # Build the resulting strings
    results = []
    for combo in combinations:
        result = list(original)
        combo_index = 0
        for j, character  in enumerate(result):
            if character == '*':
                result[j] = combo[combo_index]
                combo_index += 1
        results.append(''.join(result))

    return results

# helpers
def deasteriskize(lst: list) -> list:
    """expand asterisk notation

    Args:
        lst (list): the list of filters to be expanded

    Returns:
        list: the expanded list
    """
    result = list(lst)
    while "*" in "".join(result):
        for item in list(result):
            if "*" in item:
                result.remove(item)
                expanded: list[str] = deasteriskize_str(item)
                for j in expanded:
                    result.append(j)
    return result

def deslash(lst: list) -> list:
    """expand slash notation

    Args:
        lst (list): the list of filters to be expanded, maybe having some a/b formatted filters

    Returns:
        list: the expanded list
    """
    result = list(lst)
    while "/" in "".join(result):
        for item in list(result):
            if "/" in item:
                result.remove(item)
                splited = item.split("/")
                result.append(splited[0] + " " + splited[1])
                result.append(splited[1] + " " + splited[0])
                break
    return result

def contain(lst: list, parent: str) -> bool:
    """check whether all of the list components are in the parent string

    Args:
        lst (list): the list containing the components
        parent (str): the parent string

    Returns:
        bool: the result
    """
    result = True
    for component in lst:
        if component not in parent:
            result = False
    return result

# get algs
print('paste your algs here: ("done" when done)')
algs = []
try:
    for line in iter(input, "done"):
        algs.append(line)
except KeyboardInterrupt:
    exit()

# filter out non algs content
for i in list(algs):
    if i == "" or i[0:15] == "Searching depth":
        algs.remove(i)

# get filters for as long as the user wants
print('''\nput your filters here:\n(available symbols: & * / .) (no spaces) ("done" when done)''')
try:
    while True:
        filters = []
        for line in iter(input, "done"):
            filters.append(line)
        filters = deslash(filters)
        filters = deasteriskize(filters)

        # filter
        for alg in list(algs):
            for f in filters:
                if "&" in f:
                    if contain(f.split("&"), alg):
                        algs.remove(alg)
                        break
                elif f[0] == ".":
                    if alg[: len(f) - 1] == f[1:]:
                        algs.remove(alg)
                        break
                elif f[-1] == ".":
                    if alg.split("(")[0].strip()[-1 * len(f):] == f[:-1]:
                        algs.remove(alg)
                        break
                elif f in alg:
                    algs.remove(alg)
                    break
        # output
        print("\n".join(algs))

        # reinput
        print('''\nreinput your filters here:
(available symbols: & * / .) (no spaces) ("done" when done''')
except KeyboardInterrupt:
    exit()
