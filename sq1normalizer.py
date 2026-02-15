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

def normalize(alg: str, l_f_lst: list[int], k = None, leave: bool = True) -> str:
    """normalizes the alg

    Args:
        alg (str): alg to be normalized
        l_f_lst (list[int]): a list of all the positions to y2 at (e.g. [1] for y2 the whole alg)
        k (bool | None): whether to be in karn, defaulted to follow alg
        leave (bool): whether to leave the alg alone and not normalize

    Returns:
        str: normalized alg
    """
    alg = re.sub(r"\[.*\]", "", alg).strip()
    l_f_lst = [-1] if not l_f_lst else l_f_lst
    k_i = ob_karn(alg) #whether the scram is in karn
    k = k_i if k is None else k # whether to put it in karn

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
            alg = "/".join([f"{legal_move(int(i.split(",")[0]))},{legal_move(int(i.split(",")[1]))}"
                            for i in alg.split("/")]) # make moves legal
            alg = re.sub(r"\/", " ", alg) # slash to space
            alg = re.sub(r",", "", alg) # X comma
        else:
            # no slash, prob karn in numbers
            alg = re.sub(r" +", " ", alg) # X mutiple spaces
            alg = " ".join([f"{legal_move(int(i.split(",")[0]))},{legal_move(int(i.split(",")[1]))}"
                            for i in alg.split(" ")]) # make moves legal TODO
            alg = re.sub(r",", "", alg) # X comma

    # now alg in "10 5-1 -51 -10"
    alst = alg.split(" ")
    if l_f_lst != [""] and max(l_f_lst) > len(alst)-3:
        raise ValueError(f"You cannot modify the move after the {max(l_f_lst)}th slice!")
    if alst[0].lower() != "a":
        alst[0] = "A" if int(alst[0][-1]) % 3 == 0 else "a"
        alst[-1] = "A" if int(alst[-1][-1]) % 3 == 0 else "a"

    # now alg in "A 5-1 -51 A"
    l_fing = False
    facing_d = False # whether we need to l_f this move
    for i in range(1, len(alst) -2): # avoid checking the last actual move also
        m = alst[i]
        m = l_f(m) if facing_d else m
        if (not leave and m not in GOOD) or i in l_f_lst:
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

print("input alg (parentheses ok, comma ok, slash ok, karn ok, starts at no misaligns): ")
u = []
try:
    for line in iter(input, ""):
        u.append(line)
except KeyboardInterrupt:
    exit()
if len(u) > 1:
    # multiple algs
    layer_flip = check("return y2 alg? (yes/no): ",
                lambda ans: ans.lower().strip() in ["yes", "no"]).lower().strip()
    if layer_flip == "yes":
        l_f_pos_t = check("where? (leave empty to be at the start, " +
                        "else indicate after which slices, separated by comma no spaces): ",
                        lambda ans: all(ch.isdigit() for ch in ans.strip().split(",")),
                        True).strip().split(",")
        l_f_pos = [1] if l_f_pos_t == [""] else [int(ch) for ch in l_f_pos_t] # [2,3], etc.
    else:
        l_f_pos = []
    norm = check("perform normalization? (yes/no, leave empty to be yes): ",
                lambda ans: ans.lower().strip() in ["yes", "no"], True).lower().strip()
    normb = norm == "no"
    karn = check("in karn? (yes/no, leave empty to follow alg formats): ",
                lambda ans: ans.lower().strip() in ["yes", "no"],
                True).lower().strip()
    karnb = True if karn == "yes" else False if karn == "no" else None
    print(*list({normalize(line,l_f_pos,karnb,normb) for line in filter(
            lambda a: a[0:9] != "searching", u # get rid of the searching lines first
        )}), sep="\n")
else:
    # one alg, so we can do a recursion of modification
    line = u[0]
    while True:
        layer_flip = check("return y2 alg? (yes/no): ",
                    lambda ans: ans.lower().strip() in ["yes", "no"]).lower().strip()
        if layer_flip == "yes":
            l_f_pos_t = check("where? (leave empty to be at the start, " +
                            "else indicate after which slices, separated by comma no spaces): ",
                            lambda ans: all([ch.isdigit() for ch in ans.strip().split(",")]),
                            True).strip().split(",")
            l_f_pos = [1] if l_f_pos_t == [""] else [int(ch) for ch in l_f_pos_t] # [2,3], etc.
        else:
            l_f_pos = []
        norm = check("perform normalization? (yes/no): ",
                    lambda ans: ans.lower().strip() in ["yes", "no"], True).lower().strip()
        normb = norm == "no"
        karn = check("in karn? (yes/no, leave empty to follow alg formats): ",
                    lambda ans: ans.lower().strip() in ["yes", "no"],
                    True).lower().strip()
        karnb = True if karn == "yes" else False if karn == "no" else None
        line = normalize(line,l_f_pos,karnb,normb)
        print(line)
