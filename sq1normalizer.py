"""normalizes/y2s squan algs"""

import re
from get_scramble import legal_move, optimize, INV_NORM, NORM
from get_scramble import replace_with_dict, changes_alignment
from helpers import check

GOOD = [
    "11", "-1-1", "22", "-2-2",
    "2-1", "-21", "1-2", "-12",
    "30", "-30", "03", "0-3", "33", "3-3", "-3-3", "-33",
    "41", "-4-1", "14", "-1-4",
    "2-4", "-24", "4-2", "-42",
    "5-1", "-51"
]

def ob_karn(a: str) -> bool:
    """checks whether alg is in karn by checking if letters are present

    Args:
        a (str): alg

    Returns:
        bool: verdict
    """
    l = list(a)
    l2 = [not i.isalpha() for i in l]
    return not all(l2)

def sep_index(a: str) -> int:
    """returns the index of of the split of a move, english counting

    Args:
        a (str): e.g. "6-3"

    Returns:
        int: e.g. 1
    """
    l = list(a)
    inx = 0
    for char in l:
        inx += 1
        if char.isdigit():
            break
    return inx


def compl(a: str) -> str:
    """returns the complement move

    Args:
        a (str): e.g. "6-3"

    Returns:
        str: e.g. "03"
    """
    inx = sep_index(a)
    l = [a[0:inx], a[inx:]]
    return "".join([str(legal_move(6+int(l[0]))), str(legal_move(6+int(l[1])))])

def l_f(a: str) -> str:
    """returns the layer-flipped move

    Args:
        a (str): e.g. "2-1", "63"

    Returns:
        str: e.g. "-12", "36"
    """
    inx = sep_index(a)
    return "".join([a[inx:], a[0:inx]])

def comma(a: str) -> str:
    """adds a comma for the moves

    Args:
        a (str): e.g. "6-3"

    Returns:
        str: e.g. "6,-3"
    """
    inx = sep_index(a)
    return ",".join([a[0:inx], a[inx:]])

def normalize(alg: str, l_fing: bool = False, k = None) -> str:
    """normalizes the alg

    Args:
        alg (str): alg to be normalized
        l_fing (bool): whether we are y2ing the alg, defaulted to no
        k (bool | None): whether to be in karn, defaulted to follow alg

    Returns:
        str: normalized alg
    """
    alg = re.sub(r"\[.*\]", "", alg).strip()
    k_i = ob_karn(alg) #whether the scram is in karn
    k = ob_karn(alg) if k is None else k # whether to put it in karn

    if k_i:
        # turn it into numbers
        alg = replace_with_dict(alg, NORM)
        # no slash, no paren, no comma
    else:
        # potential slash, potential paren, potential comma
        alg = re.sub(r"\(|\)", "", alg)
        # no paren now
        if "/" in list(alg):
            # slash present, can safely replace space
            alg = re.sub(r" ", "", alg) # X space
            alg = re.sub(r"\/", " ", alg) # slash to space
            alg = re.sub(r",", "", alg) # X comma
        else:
            # no slash, prob karn in numbers
            alg = re.sub(r" +", " ", alg) # X mutiple spaces
            alg = re.sub(r",", "", alg) # X comma

    # now alg in "10 5-1 -51 -10"

    facing_d = l_fing # whether we need to l_f this move
    alst = alg.split(" ")
    if alst[0].lower() != "a":
        alst[0] = "A" if changes_alignment(int(alst[0][0:sep_index(alst[0])])) else "a"
        alst[-1] = "A" if changes_alignment(int(alst[-1][0:sep_index(alst[-1])])) else "a"
    # now alg in "A 5-1 -51 A"
    for i in range(1, len(alst) -2): # avoid checking the last actual move also
        m = alst[i]
        m = l_f(m) if facing_d else m
        if m not in GOOD:
            m = compl(m)
            l_fing = not l_fing
        facing_d = not facing_d if l_fing else facing_d
        alst[i] = m
    # change the last move here
    alst[-2] = l_f(alst[-2]) if facing_d else alst[-2]
    alst[-2] = compl(alst[-2]) if not (l_fing == facing_d) else alst[-2]
    last_move = alst[-2]
    for i in range(1, len(alst)-1):
        alst[i] = comma(alst[i])
    alg = optimize("/".join(alst))

    # now we can do formatting
    if k:
        alg = re.sub(r"\/", " ", alg) # slash to space
        alg = re.sub(r",", "", alg) # X comma
        alg = replace_with_dict(alg, INV_NORM)
    comment = "" if last_move in [*GOOD, "-45", "-54", "63", "6-3"] else " (bad finish)"
    comment += "" if alg[0:1] == alg [-1:] else " (alignment changes)"
    return alg + comment

print("input alg (parentheses ok, comma ok, slash ok, karn ok): ")
u = []
try:
    for line in iter(input, ""):
        u.append(line)
except KeyboardInterrupt:
    exit()
layer_flip = check("return y2 alg? (yes/no): ",
             lambda ans: ans.lower().strip() in ["yes", "no"]).lower().strip()
layer_flipb = True if layer_flip == "yes" else False
karn = check("in karn? (yes/no, leave empty to follow alg formats): ",
             lambda ans: ans.lower().strip() in ["yes", "no"],
             True).lower().strip()
karnb = True if karn == "yes" else False if karn == "no" else None
print(*list({normalize(line,layer_flipb,karnb) for line in u}), sep="\n")
