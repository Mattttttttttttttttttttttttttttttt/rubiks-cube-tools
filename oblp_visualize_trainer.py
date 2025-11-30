"""this module provides valid oblp memo for visualization.
toggle the variables INVERSE and ONEFACE to switch modes."""

import random
import sys
import time
from get_scramble import layer_flip, shift, get_non_spe

OBL = {"BBwWWwWWwWWw": "1c",
       "BBwBBwWWwWWw": "cadj",
       "BBwWWwBBwWWw": "copp",
       "BBwBBwBBwWWw": "3c",
       "BBwBBwBBwBBw": "4e",
       "WWbWWbWWbWWw": "3e",
       "WWbWWwWWbWWw": "line",
       "WWbWWbWWwWWw": "L",
       "WWbWWwWWwWWw": "1e",
       "WWbBBwWWwWWw": "left pair",
       "BBbWWwWWwWWw": "right pair",
       "BBwWWwWWbWWw": "left arrow",
       "BBwWWbWWwWWw": "right arrow",
       "WWbBBbWWwWWw": "gem",
       "WWwWWbWWbBBw": "left knight",
       "BBbWWbWWwWWw": "right knight",
       "WWwWWbWWwBBb": "left axe",
       "BBwWWbWWwWWb": "right axe",
       "BBwWWbWWbWWw": "squid",
       "WWwWWbBBbWWb": "left thumb",
       "WWbBBbWWwWWb": "right thumb",
       "WWwBBbWWbWWb": "left bunny",
       "WWbWWbBBwWWb": "right bunny",
       "BBbBBwWWwWWw": "shell",
       "BBwWWwWWbBBw": "left bird",
       "BBwBBbWWwWWw": "right bird",
       "BBwWWbWWwBBw": "hazard",
       "BBbBBbWWwWWw": "left kite",
       "WWwWWbBBbBBw": "right kite",
       "BBwBBwWWbWWb": "left cut",
       "BBwBBbWWbWWw": "right cut",
       "BBbBBwWWbWWw": "black T",
       "WWwWWbBBwBBb": "white T",
       "WWbBBwWWbBBw": "left N",
       "WWwBBbWWwBBb": "right N",
       "WWbBBbWWwBBw": "black tie",
       "BBwWWwBBbWWb": "white tie",
       "BBbWWwBBwWWw": "left yoshi",
       "WWwBBwWWbBBw": "right yoshi"
}

GB = { # whether this case: same → good, or the other way; if not here: no good/bad
    "pair/pair": "same",
    "arrow/pair": "diff",
    "pair/arrow": "diff",
    "arrow/arrow": "same",
    "knight/knight": "diff",
    "knight/axe": "same",
    "axe/knight": "same",
    "axe/axe": "same",
    "thumb/thumb": "same",
    "thumb/bunny": "diff",
    "bunny/thumb": "diff",
    "bunny/bunny": "same",
    "bird/bird": "diff",
    "yoshi/bird": "same",
    "bird/yoshi": "same",
    "yoshi/yoshi": "same",
    "kite/kite": "same",
    "kite/cut": "same",
    "cut/kite": "same",
    "cut/cut": "same",
    "kite/N": "diff",
    "N/kite": "diff",
    "cut/N": "same",
    "N/cut": "same",
    "N/N": "same",
    "T/T": "same",
    "T/tie": "same",
    "tie/T": "same",
    "tie/tie": "same"
}

CORNERS = [[""], ["1", "3", "5", "7"],
          [ "13", "15", "17", "35", "37", "57"], ["135", "137", "157", "357"], ["1357"]]
TOTAL_CORNERS = ["", "1", "3", "5", "7",
           "13", "15", "17", "35", "37", "57", "135", "137", "157", "357", "1357"]
EDGES = [[""], ["2", "4", "6", "8"],
        [ "24", "26", "28", "46", "48", "68"], ["246", "248", "268", "468"], ["2468"]]
TOTAL_EDGES = ["", "2", "4", "6", "8",
         "24", "26", "28", "46", "48", "68", "246", "248", "268", "468", "2468"]
GROUPS = len(CORNERS)

def sort_oblp(seq: str) -> str:
    """sorts e.g. 157268 into 125678

    Args:
        seq (str): corner string and edge string joined together

    Returns:
        str: the joined string
    """
    a = list(seq)
    a.sort(key=int)
    return "".join(a)

def is_obl(l: str, target: str) -> bool:
    """determines if m is the same obl as the target

    Args:
        l (str): BbWw
        target (str): target BbWw

    Returns:
        bool: verdict
    """
    target_obl = OBL[target]
    for m in range(4):
        if target == shift(l, 3*m):
            return True
    if target_obl.split(" ")[-1] not in ["T", "tie"]:
        # T and tie colors are specified
        l = layer_flip(l)
        for m in range(4):
            if target == shift(l, 3*m):
                return True
    return False

def to_layer_name(m: str) -> str:
    """converts 1-8 to BbWw and return the case name

    Args:
        m (str): 1-8 tracing of one face

    Returns:
        str: case name of the obl
    """
    bw = ["W", "W", "w"]*4
    for num in list(m):
        num = int(num)
        if num % 2 != 0:
            # corner
            bw[num//2*3] = "B"
            bw[num//2*3+1] = "B"
        else:
            # edge
            bw[num//2*3-1] = "b"
    obl = "".join(bw)
    for obl_case in OBL:
        if is_obl(obl, obl_case):
            break
    if not is_obl(obl, obl_case):
        raise ValueError("obl: "+obl+" is not in the dictionary")
    return OBL[obl_case]

def to_case_name(m: str) -> str:
    """converts two 1-8 tracing to a obl name e.g. "good bunny/thumb"

    Args:
        m (str): e.g. "12345 234"

    Returns:
        str: e.g. "good bunny/thumb
    """
    [u,d] = m.split(" ")
    u = to_layer_name(u)
    d = to_layer_name(d)
    return get_non_spe(u+"/"+d)

ONEFACE = False # toggle
INVERSE = True # toggle

if ONEFACE:
    try:
        while True:
            corner = random.choice(TOTAL_CORNERS)
            edge = random.choice(TOTAL_EDGES)
            if not corner+edge:
                continue
            MEMO = sort_oblp(corner+edge)
            print(MEMO, end="")
            start = time.time()
            input()
            print(f"{to_layer_name(MEMO)}: {round(time.time() - start, 3)}s", end="\n")
            input()
    except KeyboardInterrupt:
        sys.exit()
else:
    try:
        while True:
            corners1 = random.choice(TOTAL_CORNERS)
            edges1 = random.choice(TOTAL_EDGES)
            corners2 = (random.choice(CORNERS[len(corners1)])
                             if INVERSE and len(corners1) + len(edges1) < 4
                            else random.choice(CORNERS[GROUPS - 1 - len(corners1)]))
            edges2 = (random.choice(EDGES[len(edges1)])
                           if INVERSE and len(corners1) + len(edges1) < 4
                            else random.choice(EDGES[GROUPS - 1 - len(edges1)]))
            MEMO = sort_oblp(corners1+edges1) + " " + sort_oblp(corners2+edges2)
            inv = random.randint(0,1) == 0
            print(f"{MEMO}{" inverse" if inv else ""}", end="")
            start = time.time()
            input()
            print(f"{to_case_name(MEMO)}: {round(time.time() - start, 3)}s", end="\n")
            input()
    except KeyboardInterrupt:
        sys.exit()

# names_to_memo = {
#     "1c": [17, 215, 413, 611], # starting from <top left>, cw
#     "1e": [71, 512, 314, 116], # starting from <left>, ccw!!

#     "cadj": [1511, 41111, 21113, 1115], # starting from <left>, ccw
#     "L": [1151, 11114, 31112, 5111], # starting from <top left>, cw

#     "copp": [1313, 21311], # starting from <top left> = <\>
#     "line": [3131, 11312], # starting from <horizontal> = <->

#     "3c": [111311, 111113, 2111111, 131111], # starting from <top left>, cw
#     "3e": [113111, 311111, 1111112, 111131], # starting from <left>, ccw

#     "4e": [11111111],

#     "paira": [161, 125, 323, 521], # starting from <top left>, cw
#     "pairo": [26, 224, 422, 62], # starting from <top left>, cw

#     "arrowa": [1214, 21212, 4121, 11411], # starting from <top left>, cw
#     "arrowo": [1412, 2141, 11213, 31211], # starting from <top left>, cw

#     "gem": [251, 134, 332, 53], # starting from <top left>, cw
#     "shell": [152, 431, 233, 35], # starting from <left>, ccw

#     "knighta": [1241, 11123, 31121, 14111], # starting from <top>, cw
#     "birdo": [1421, 32111, 12113, 11141], # starting from <left>, ccw
#     "knighto": [2114, 22112, 4211, 1142], # starting from <top>, cw
#     "birda": [4112, 21122, 1124, 2411], # starting from <bottom>, ccw

#     "axa": [2312, 2231, 11222, 3122], # <top left>, cw
#     "yosho": [2132, 1322, 22211, 2213], # <bottom right> (upside down), ccw
#     "axo": [12131, 12212, 3221, 11321], # <top left>, cw
#     "yosha": [13121, 21221, 1223, 12311], # <top right> (upright), ccw

#     "squid": [121112, 212111, 112121, 1111211], # <top left>, cw
#     "hazard": [211121, 111212, 121211, 1121111], # <right>, ccw

#     "thumba": [21131, 13112, 3311, 1133], # <top left>, cw
#     "thumbo": [23111, 1331, 11132, 3113], # <top left>, cw

#     "bunna": [1211111, 122111, 111221, 1111121], # <top left>, cw
#     "bunno": [211112, 221111, 112211, 111122], # <top left>, cw

#     "kita": [341, 143], # <top>, cw; bw mark
#     "kito": [44, 242], # <top>, cw; bw mark

#     "cuta": [1112111, 121121], # <top>, cw; bw mark
#     "cuto": [112112, 211211], # <top>, cw; bw mark

#     "tie": [22121, 13211, 1232, 2123], # <top left>, cw; bw mark
#     "T": [12122, 11231, 2321, 3212], # <top>, ccw; bw mark

#     "Na": [12221], # bw mark
#     "No": [2222] # bw mark
# }

# groups = {
#     "1,2 party": [11111111,
#                   1111112, 1111121, 1111211, 1112111, 1121111, 1211111, 2111111,
#                   111122, 111221, 112211, 122111, 221111, 211112,
#                   111212, 112121, 121211, 212111, 121112, 211121,
#                   112112, 121121, 211211,
#                   11222, 12221, 22211, 22112, 21122,
#                   12122, 21221, 12212, 22121, 21212,
#                   2222],
#     "1,3 party": [111113, 111131, 111311, 113111, 131111, 311111,
#                   1133, 1331, 3311, 3113,
#                   1313, 3131],
#     "1,4 party": [11114, 11141, 11411, 14111, 41111],
#     "1,5 party": [1115, 1151, 1511, 5111],
#     "1,6 party": [116, 161, 611],
#     "complements": [17, 71, 35, 53, 26, 62, 44],
#     "len = 3": [125, 251, 512, 152, 521, 215,
#                 134, 341, 413, 143, 431, 314,
#                 224, 242, 422,
#                 233, 332, 323],
#     "1,2,3 party": [11123, 11231, 12311, 23111, 11132, 11321, 13211, 32111,
#                     11213, 12131, 21311, 11312, 13121, 31211,
#                     12113, 21131, 13112, 31121,
#                     31112, 21113,
#                     2231, 2312, 3122, 1322, 2213, 2132,
#                     1232, 2321, 3212, 2123,
#                     1223, 3221],
#     "1,2,4 party": [1241, 1421, 4211, 1124, 1142, 2411,
#                     1214, 1412, 4121, 2141,
#                     2114, 4112]
# }
# selector = [1,1,1,1,0,0,0,0,0] # 1 to select the group

# def search(a: int) -> str:
#     """search for the oblp naming in the names_to_memo dictionary

#     Args:
#         a (int): the name of the shape

#     Returns:
#         str: e.g. "hazard2"
#     """
#     for index, lst in enumerate(list(names_to_memo.values())):
#         for index2, num in enumerate(lst):
#             if a == num:
#                 return list(names_to_memo.keys())[index] + str(index2+1)
#     print(a, "not found")
#     return str(a)

# try:
#     all_names = []
#     for i, boolean in enumerate(selector):
#         if boolean:
#             for j in list(groups.values())[i]:
#                 all_names.append(j)
#     while True:
#         # i = random.choice(list(names_to_memo.keys()))
#         # j = random.randint(1, len(names_to_memo[i]))
#         # input(names_to_memo[i][j-1] + ": ")
#         # print(i+str(j))
#         name = random.choice(all_names)
#         input(str(name) + " ")
#         print(search(name))
# except KeyboardInterrupt:
#     exit()
