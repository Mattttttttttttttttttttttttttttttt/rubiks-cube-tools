"""squan coding library. OBL heavy"""

import random
import re

POSSIBLE_OBL = [
    ["", "solved", "solved"],

    ["", "1c", "1c"],
    ["", "cadj", "cadj"],
    ["", "cadj", "copp"],
    ["", "copp", "copp"],
    ["", "3c", "3c"],
    ["", "4e", "4e"],
    ["", "3e", "3e"],
    ["", "line", "line"],
    ["", "L", "line"],
    ["", "L", "L"],
    ["", "1e", "1e"],
    ["good", "pair", "pair"],
    ["bad", "pair", "pair"],
    ["good", "arrow", "pair"],
    ["bad", "arrow", "pair"],
    ["good", "arrow", "arrow"],
    ["bad", "arrow", "arrow"],
    ["", "gem", "gem"],
    ["", "gem", "knight"],
    ["", "gem", "axe"],
    ["", "gem", "squid"],
    ["good", "knight", "knight"],
    ["bad", "knight", "knight"],
    ["good", "knight", "axe"],
    ["bad", "knight", "axe"],
    ["same", "axe", "axe"],
    ["diff", "axe", "axe"],
    ["", "squid", "knight"],
    ["", "squid", "axe"],
    ["", "squid", "squid"],
    ["good", "thumb", "thumb"],
    ["bad", "thumb", "thumb"],
    ["good", "thumb", "bunny"],
    ["bad", "thumb", "bunny"],
    ["good", "bunny", "bunny"],
    ["bad", "bunny", "bunny"],
    ["", "shell", "shell"],
    ["", "shell", "bird"],
    ["", "shell", "hazard"],
    ["", "yoshi", "shell"],
    ["good", "bird", "bird"],
    ["bad", "bird", "bird"],
    ["", "bird", "hazard"],
    ["", "hazard", "hazard"],
    ["good", "yoshi", "bird"],
    ["bad", "yoshi", "bird"],
    ["", "yoshi", "hazard"],
    ["same", "yoshi", "yoshi"],
    ["diff", "yoshi", "yoshi"],
    ["good", "kite", "kite"],
    ["bad", "kite", "kite"],
    ["good", "kite", "cut"],
    ["bad", "kite", "cut"],
    ["", "kite", "T"],
    ["good", "kite", "N"],
    ["bad", "kite", "N"],
    ["", "kite", "tie"],
    ["", "cut", "T"],
    ["good", "cut", "N"],
    ["bad", "cut", "N"],
    ["", "cut", "tie"],
    ["good", "cut", "cut"],
    ["bad", "cut", "cut"],
    ["good", "T", "T"],
    ["bad", "T", "T"],
    ["", "T", "N"],
    ["good", "T", "tie"],
    ["bad", "T", "tie"],
    ["good", "N", "N"],
    ["bad", "N", "N"],
    ["", "tie", "N"],
    ["good", "tie", "tie"],
    ["bad", "tie", "tie"]
]

OBL_TRANSLATION = {
    # no layer flips
    "solved/solved": ["solved/solved"],

    "1c/1c": ["1c/1c"],
    "cadj/cadj": ["cadj/cadj"],
    "cadj/copp": ["cadj/copp"],
    "copp/copp": ["copp/copp"],
    "3c/3c": ["3c/3c"],
    "4e/4e": ["4e/4e"],
    "3e/3e": ["3e/3e"],
    "line/line": ["line/line"],
    "L/line": ["L/line"],
    "L/L": ["L/L"],
    "1e/1e": ["1e/1e"],
    "good pair/pair": ["left pair/left pair", "right pair/right pair"],
    "bad pair/pair": ["left pair/right pair"],
    "good arrow/pair": ["left arrow/right pair", "right arrow/left pair"],
    "bad arrow/pair": ["left arrow/left pair", "right arrow/right pair"],
    "good arrow/arrow": ["left arrow/left arrow", "right arrow/right arrow"],
    "bad arrow/arrow": ["left arrow/right arrow"],
    "gem/gem": ["gem/gem"],
    "gem/knight": ["gem/left knight", "gem/right knight"],
    "gem/axe": ["gem/left axe", "gem/right axe"],
    "gem/squid": ["gem/squid"],
    "good knight/knight": ["left knight/right knight"],
    "bad knight/knight": ["left knight/left knight", "right knight/right knight"],
    "good knight/axe": ["left knight/left axe", "right knight/right axe"],
    "bad knight/axe": ["left knight/right axe", "right knight/left axe"],
    "same axe/axe": ["left axe/left axe", "right axe/right axe"],
    "diff axe/axe": ["left axe/right axe"],
    "squid/knight": ["squid/left knight", "squid/right knight"],
    "squid/axe": ["squid/left axe", "squid/right axe"],
    "squid/squid": ["squid/squid"],
    "good thumb/thumb": ["left thumb/left thumb", "right thumb/right thumb"],
    "bad thumb/thumb": ["left thumb/right thumb"],
    "good thumb/bunny": ["left thumb/right bunny", "right thumb/left bunny"],
    "bad thumb/bunny": ["left thumb/left bunny", "right thumb/right bunny"],
    "good bunny/bunny": ["left bunny/left bunny", "right bunny/right bunny"],
    "bad bunny/bunny": ["left bunny/right bunny"],
    "shell/shell": ["shell/shell"],
    "shell/bird": ["shell/left bird", "shell/right bird"],
    "shell/hazard": ["shell/hazard"],
    "yoshi/shell": ["left yoshi/shell", "right yoshi/shell"],
    "good bird/bird": ["left bird/right bird"],
    "bad bird/bird": ["left bird/left bird", "right bird/right bird"],
    "bird/hazard": ["left bird/hazard", "right bird/hazard"],
    "hazard/hazard": ["hazard/hazard"],
    "good yoshi/bird": ["left yoshi/left bird", "right yoshi/right bird"],
    "bad yoshi/bird": ["left yoshi/right bird", "right yoshi/left bird"],
    "yoshi/hazard": ["left yoshi/hazard", "right yoshi/hazard"],
    "same yoshi/yoshi": ["left yoshi/left yoshi", "right yoshi/right yoshi"],
    "diff yoshi/yoshi": ["left yoshi/right yoshi"],
    "good kite/kite": ["left kite/left kite", "right kite/right kite"],
    "bad kite/kite": ["left kite/right kite"],
    "good kite/cut": ["left kite/left cut", "right kite/right cut"],
    "bad kite/cut": ["left kite/right cut", "right kite/left cut"],
    "kite/T": ["left kite/black T", "left kite/white T",
                "right kite/black T", "right kite/white T"],
    "good kite/N": ["left kite/right N", "right kite/left N"],
    "bad kite/N": ["left kite/left N", "right kite/right N"],
    "kite/tie": ["left kite/black tie", "left kite/white tie",
                "right kite/black tie", "right kite/white tie"],
    "cut/T": ["left cut/black T", "left cut/white T",
                "right cut/black T", "right cut/white T"],
    "good cut/N": ["left cut/left N", "right cut/right N"],
    "bad cut/N": ["left cut/right N", "right cut/left N"],
    "cut/tie": ["left cut/black tie", "left cut/white tie",
                "right cut/black tie", "right cut/white tie"],
    "good cut/cut": ["left cut/left cut", "right cut/right cut"],
    "bad cut/cut": ["left cut/right cut"],
    "good T/T": ["black T/black T", "white T/white T"],
    "bad T/T": ["black T/white T"],
    "T/N": ["black T/left N", "black T/right N",
            "white T/left N", "white T/right N"],
    "good T/tie": ["black T/black tie", "white T/white tie"],
    "bad T/tie": ["black T/white tie", "white T/black tie"],
    "good N/N": ["left N/left N", "right N/right N"],
    "bad N/N": ["left N/right N"],
    "tie/N": ["black tie/left N", "black tie/right N",
            "white tie/left N", "white tie/right N"],
    "good tie/tie": ["black tie/black tie", "white tie/white tie"],
    "bad tie/tie": ["black tie/white tie"]
}

OBL_LEN = {
    "solved/solved": 0,

    "1c/1c": 5,
    "cadj/cadj": 4,
    "cadj/copp": 5,
    "copp/copp": 2,
    "3c/3c": 5,
    "4e/4e": 4,
    "3e/3e": 5,
    "line/line": 2,
    "L/line": 5,
    "L/L": 4,
    "1e/1e": 5,
    "good pair/pair": 2,
    "bad pair/pair": 4,
    "good arrow/pair": 3,
    "bad arrow/pair": 4,
    "good arrow/arrow": 3,
    "bad arrow/arrow": 4,
    "gem/gem": 4,
    "gem/knight": 4,
    "gem/axe": 3,
    "gem/squid": 4,
    "good knight/knight": 4,
    "bad knight/knight": 5,
    "good knight/axe": 3,
    "bad knight/axe": 4,
    "same axe/axe": 5,
    "diff axe/axe": 5,
    "squid/knight": 4,
    "squid/axe": 4,
    "squid/squid": 5,
    "good thumb/thumb": 2,
    "bad thumb/thumb": 5,
    "good thumb/bunny": 4,
    "bad thumb/bunny": 4,
    "good bunny/bunny": 3,
    "bad bunny/bunny": 5,
    "shell/shell": 4,
    "shell/bird": 4,
    "shell/hazard": 4,
    "yoshi/shell": 3,
    "good bird/bird": 4,
    "bad bird/bird": 5,
    "bird/hazard": 4,
    "hazard/hazard": 5,
    "good yoshi/bird": 3,
    "bad yoshi/bird": 4,
    "yoshi/hazard": 4,
    "same yoshi/yoshi": 5,
    "diff yoshi/yoshi": 5,
    "good kite/kite": 1,
    "bad kite/kite": 5,
    "good kite/cut": 3,
    "bad kite/cut": 6,
    "kite/T": 4,
    "good kite/N": 3,
    "bad kite/N": 4,
    "kite/tie": 4,
    "cut/T": 4,
    "good cut/N": 4,
    "bad cut/N": 5,
    "cut/tie": 4,
    "good cut/cut": 3,
    "bad cut/cut": 6,
    "good T/T": 3,
    "bad T/T": 4,
    "T/N": 5,
    "good T/tie": 3,
    "bad T/tie": 4,
    "good N/N": 2,
    "bad N/N": 4,
    "tie/N": 5,
    "good tie/tie": 3,
    "bad tie/tie": 4
}

def obl_name(obl: list[str]) -> str:
    """returns the name in english of this array

    Args:
        obl (list[str]): e.g. ["", "1c", "1c"]

    Returns:
        str: e.g. "1c/1c"
    """
    return f"{obl[0]} {obl[1]}/{obl[2]}" if obl[0] else f"{obl[1]}/{obl[2]}"

def get_non_spe(obl: str) -> str:
    """get the non specific case name of an OBL

    Args:
        obl (str): specific case name, e.g. left pair/right pair

    Returns:
        str: e.g. good pair/pair
    """
    obl_lst = obl.split("/") # len = 2
    u_obl = obl_lst[0].split(" ")[-1]
    d_obl = obl_lst[1].split(" ")[-1]
    candidates = [] # filled with obl arrays of 3
    for cand in POSSIBLE_OBL:
        if u_obl in cand and d_obl in cand:
            candidates.append(obl_name(cand))
    for cand in candidates:
        for spe_obl in OBL_TRANSLATION[cand]:
            if spe_obl == obl:
                return cand
            spe_obl = spe_obl.split("/")
            if spe_obl[1]+"/"+spe_obl[0] == obl:
                return layer_flip_name(cand) # layer flip
    raise ValueError("no non-specific OBL found for: "+obl)

def layer_flip_name(obl: str) -> str:
    """flips an obl name in english

    Args:
        obl (str): e.g. "good pair/arrow" or "L/line"

    Returns:
        str: e.g. "good arrow/pair" or "line/L"
    """
    obl = obl.replace("/", " ")
    obla = obl.split(" ")
    if len(obla) == 2:
        return obla[1] + "/" + obla[0]
    return obla[0] + " " + obla[2] + "/" + obla[1]

OBL = {"solved": "BBbBBbBBbBBb",

       "1c": "BBwWWwWWwWWw",
       "cadj": "BBwBBwWWwWWw",
       "copp": "BBwWWwBBwWWw",
       "3c": "BBwBBwBBwWWw",
       "4e": "BBwBBwBBwBBw",
       "3e": "WWbWWbWWbWWw",
       "line": "WWbWWwWWbWWw",
       "L": "WWbWWbWWwWWw",
       "1e": "WWbWWwWWwWWw",

       "left pair": "WWbBBwWWwWWw",
       "right pair": "BBbWWwWWwWWw",
       "left arrow": "BBwWWwWWbWWw",
       "right arrow": "BBwWWbWWwWWw",
       "gem": "WWbBBbWWwWWw",
       "left knight": "WWwWWbWWbBBw",
       "right knight": "BBbWWbWWwWWw",
       "left axe": "WWwWWbWWwBBb",
       "right axe": "BBwWWbWWwWWb",
       "squid": "BBwWWbWWbWWw",
       "left thumb": "WWwWWbBBbWWb",
       "right thumb": "WWbBBbWWwWWb",
       "left bunny": "WWwBBbWWbWWb",
       "right bunny": "WWbWWbBBwWWb",

       "shell": "BBbBBwWWwWWw",
       "left bird": "BBwWWwWWbBBw",
       "right bird": "BBwBBbWWwWWw",
       "hazard": "BBwWWbWWwBBw",
       "left kite": "BBbBBbWWwWWw",
       "right kite": "WWwWWbBBbBBw",
       "left cut": "BBwBBwWWbWWb",
       "right cut": "BBwBBbWWbWWw",
       "black T": "BBbBBwWWbWWw",
       "white T": "WWwWWbBBwBBb",
       "left N": "WWbBBwWWbBBw",
       "right N": "WWwBBbWWwBBb",
       "black tie": "WWbBBbWWwBBw",
       "white tie": "BBwWWwBBbWWb",
       "left yoshi": "BBbWWwBBwWWw",
       "right yoshi": "WWwBBwWWbBBw"
}
# format is 24-character string, both corner first, STARTING FROM TOP RIGHT OF SLICE
CUBEL = 24
HALF_L = 6
LAYERL = 12
THREE_FOUR_L = 18
SOLVED_D = "BBbBBbBBbBBbWWwWWwWWwWWw"
SOLVED_U = "bBBbBBbBBbBBwWWwWWwWWwWW"
SLICE_D_PBL = "FF6GG7DD4AA1BB2CC3HH8EE5"
SLICE_D = "WWwWWwBBbBBbBBbBBbWWwWWw"
SLICE_U = "wWWwWWbBBbBBbBBbBBwWWwWW"
SLICE_U_PBL = "5FF6GG3DD4AA1BB2CC7HH8EE"
KARN = {
    "3,0":"U",
    "-3,0":"U'",
    "0,3":"D",
    "0,-3":"D'",
    "3,3":"e",
    "2,-1":"u",
    "-1,2":"d",
    "-4,-1":"F'",
    "-1,-4":"f'",
    "2,-4":"T",
    "2,2":"m",
    "-1,-1": "M'",
    "5,-1":"u2",
    "-2,1":"u'",
    "1,-2":"d'",
    "4,1":"F",
    "1,4":"f",
    "-2,4":"T'",
    "-2,-2":"m'",
    "1,1": "M",
    "-5,1": "u2'"
}
A_MOVES = [[3,0], [-3,0], [0,3], [0,-3], [3,3],
    [2,-1], [-1,2], [-4,-1], [-1,-4], [2,-4], [2,2], [-1,-1], [5,-1]]
a_MOVES = [[3,0], [-3,0], [0,3], [0,-3], [3,3],
    [-2,1], [1,-2], [4,1], [1,4], [-2,4], [-2,-2], [1,1], [-5,1]]
KARNL = len(a_MOVES)
INV_NORM = {
    " U U' U U' ": " U4 ",
    " U' U U' U ": " U4' ",
    " D D' D D' ": " D4 ",
    " D' D D' D ": " D4' ",
    " u u' u u' ": " u4 ",
    " u' u u' u ": " u4' ",
    " d d' d d' ": " d4 ",
    " d' d d' d ": " d4' ",

    " U U' U ": " U3 ",
    " U' U U' ": " U3' ",
    " D D' D ": " D3 ",
    " D' D D' ": " D3' ",
    " u u' u ": " u3 ",
    " u' u u' ": " u3' ",
    " d d' d ": " d3 ",
    " d' d d' ": " d3' ",
    " F F' F ": " F3 ",
    " F' F F' ": " F3' ",
    " f f' f ": " f3 ",
    " f' f f' ": " f3' ",

    " U U' ": " W ",
    " U' U ": " W' ",
    " D D' ": " B ",
    " D' D ": " B' ",
    " u u' ": " w ",
    " u' u ": " w' ",
    " d d' ": " b ",
    " d' d ": " b' ",
    " F F' ": " F2 ",
    " F' F ": " F2' ",
    " f f' ": " f2 ",
    " f' f ": " f2' ",

    " U U ": " UU ",
    " U' U' ": " UU' ",
    " D D ": " DD ",
    " D' D' ": " DD' ",

    " 6,0 ": " U2 ",
    " 6,3 ": " U2D ",
    " 6,-3 ": " U2D' ",
    " 6,6 ": " U2D2 ",
    " 0,6 ": " D2 ",
    " 3,6 ": " UD2 ",
    " -3,6 ": " U'D2 ",

    " 3,0 ": " U ",
    " -3,0 ": " U' ",
    " 0,3 ": " D ",
    " 0,-3 ": " D' ",
    " 3,-3 ": " E ",
    " -3,3 ": " E' ",
    " 3,3 ": " e ",
    " -3,-3 ": " e' ",
    " 2,-1 ": " u ",
    " -1,2 ": " d ",
    " -4,-1 ": " F' ",
    " -1,-4 ": " f' ",
    " 2,-4 ": " T ",
    " -4,2 ": " t' ",
    " 2,2 ":" m ",
    " -1,-1 ": " M' ",
    " 5,-1 ":" u2 ",
    " -1,5 ": " d2 ",
    " -2,1 ":" u' ",
    " 1,-2 ":" d' ",
    " 4,1 ":" F ",
    " 1,4 ":" f ",
    " -2,4 ": " T' ",
    " 4,-2 ": " t ",
    " -2,-2 ":" m' ",
    " 1,1 ": " M ",
    " -5,1 ": " u2' ",
    " 1,-5 ": " d2' ",
    " -5,-2 ": " K' ",
    " 5,2 ": " K ",
    " 2,5 ": " k ",
    " -2,-5 ": " k' "
}
NORM = {v: k for k, v in INV_NORM.items()}
# if the following moves accur, replace them with optimized ones
# UPDATE THIS
OPTIM = {
    # longest first
    "/3,3/3,3/": "-3,-3/-3,-3",
    "/-3,-3/-3,-3/": "3,3/3,3",
    "/2,2/-2,-2/": "2,2/-2,-2",
    "/-2,-2/2,2/": "-2,-2/2,2",
    "/1,1/-1,-1/": "1,1/-1,-1",
    "/-1,-1/1,1/": "-1,-1/1,1"
}

OPTIM_KEYS = list(OPTIM.keys()) # array of keys

def dict_replace(s: str, d: dict) -> str:
    """Replace occurrences of keys of a dictionary in a string by the values.

    Args:
        s (str): the string to be replaced
        d (dict): the dictionary to pull from

    Returns:
        str: substituted string
    """
    keys = d.keys()
    pattern = re.compile("|".join(re.escape(k) for k in keys))
    while pattern.sub(lambda m: d[m.group(0)], s) != s:
        s = pattern.sub(lambda m: d[m.group(0)], s)
    return s

def do_moves(ms: str, s: str = "BBbBBbBBbBBbwWWwWWwWWwWW") -> str:
    """does the moves on a cube

    Args:
        m (str): moves to do. need to start exactly at the cube state
        s (str, optional): initial cube state. Defaults to a no misalign solved cube.
        
    Returns:
        str: the cube state afterwards
    """
    ml = ms.split("/")
    for m in ml:
        if m != "":
            [u, d] = m.split(",")
            s = move(s, int(u), int(d))
        s = do_slice(s)
    return do_slice(s) # undo the last slice

def is_obl(layer: str, obl: str) -> bool:
    """determines if the layer is an obl

    Args:
        layer (str): 12-char string w/ BbWw, in cs
        obl (str): a key of OBL dict

    Returns:
        bool: the verdict
    """
    target = OBL[obl]
    # if it's top misalign, change to bottom misalign
    if layer[0].upper() != layer[0]:
        layer = shift(layer,-1)
    for m in range(4):
        if target == shift(layer, 3*m):
            return True
    if obl.split(" ")[-1] not in ["T", "tie"]:
        # T and tie colors are specified
        layer = layer_flip(layer)
        for m in range(4):
            if target == shift(layer, 3*m):
                return True
    return False

def is_pbl(layer: str, target: str) -> bool:
    """determinesif the layer is the end pbl

    Args:
        layer (str): 12-char string with A1B2, in cs
        target (str): 12-char string with A1B2 of the PBL

    Returns:
        bool: the verdict
    """
    # if it's top misalign, change to bottom misalign
    if layer[0].isdigit():
        layer = shift(layer,-1)
    for i in range(4):
        layer = pbl_shift(layer)
        for m in range(4):
            if target == shift(layer, 3*m):
                return True
    return False

def rand_tm_move():
    """return element of A_MOVES"""
    return list(A_MOVES)[random.randint(0,KARNL-1)]

def rand_bm_move():
    """return element of a_MOVES"""
    return list(a_MOVES)[random.randint(0,KARNL-1)]

def layer_flip(state):
    """flips "w" to "b" and vice versa in the given state

    Args:
        state (str): the state (e.g. "BBbBBbWWwWWw")
        
    Returns:
        str: the flipped state (e.g. "WWwWWwBBbBBb")
    """
    return_val = []
    for c in list(state):
        match c:
            case "b":
                return_val.append("w")
            case "B":
                return_val.append("W")
            case "w":
                return_val.append("b")
            case "W":
                return_val.append("B")
            case _:
                print(c, ": from: layer_flip(): unrecognized piece")
    return "".join(return_val)

def shift(a: str, amount: int) -> str:
    """shift "ABC" to "CAB" aka cw move, assuming amount <= a.length 
        (although if it's equal it makes no impact)

    Args:
        a (str): layer, presumably
        amount (int): the move

    Returns:
        str: shifted string
    """
    amount *= -1
    if amount < 0:
        amount += len(a)
    return a[amount:] + a[0:amount]

def pbl_shift(a: str) -> str:
    """shift a PBL layer into one of the four other colors

    Args:
        a (str): the PBL layer

    Returns:
        str: shifted PBL layer
    """
    lst = list(a)
    ret = []
    for char in lst:
        if char.isdigit():
            ret.append(str(pbl_mini_shift(int(char))))
        else:
            ret.append(chr(pbl_mini_shift(ord(char) - ord("A") + 1)-1 + ord("A")))
    return "".join(ret)

def pbl_mini_shift(n: int) -> int:
    """perform a 1-4 and a 5-8 mapping on one number

    Args:
        n (int): 1-8 number

    Raises:
        ValueError: if n not in 1-8

    Returns:
        int: mapped int
    """
    if 1 <= n <= 4:
        return (n % 4) + 1
    elif 5 <= n <= 8:
        return ((n - 5) % 4) + 5
    else:
        raise ValueError("Input must be in the range 1 to 8")

def move(cube: str, u: int, d: int) -> str:
    """does a move on the cube

    Args:
        cube (str): the original state
        u (int): the U move
        d (int): the D move

    Returns:
        str: the state after the move is performed
    """
    # u,d in int
    return (shift(cube[0:LAYERL], u) +
            shift(cube[LAYERL:], d))

def do_slice(cube: str) -> str:
    """does a slice on the cube

    Args:
        cube (str): the original state

    Returns:
        str: the state after a slice
    """
    return  (cube[LAYERL: THREE_FOUR_L] + # bottom sliced up
            cube[HALF_L: LAYERL] +
            cube[0: HALF_L] +
            cube[THREE_FOUR_L: CUBEL])

def inverse(ms: str) -> str:
    """inverses a sequence of squan moves

    Args:
        m (str): e.g. "/3,0/1,2/2,0"

    Returns:
        str: e.g. "-2,0/-1,-2/-3,0/"
    """
    ml = ms.split("/")
    ret = []
    for m in ml:
        if m == "":
            ret.insert(0, m)
        else:
            [u,d] = m.split(",")
            ret.insert(0, f"{-1*int(u)},{-1*int(d)}")
    return "/".join(ret)

def changes_alignment(m: int) -> bool:
    """determines if the given move changes alignment

    Args:
        m (int): e.g. 4

    Returns:
        bool: whether it changes alignment, e.g. True
    """
    # m in int, returns boolean
    return m % 3 != 0

def karnify(scramble: str) -> str:
    """karnifies the scramble

    Args:
        scramble (str): the scramble, 
                    e.g. "A/-3,0/-1,2/1,-2/-1,2/3,3/-2,-2/3,3/-3,0/-1,2/3,3/3,3/-2,4/A"

    Returns:
        str: after karnifying, e.g. "A U' d3 e m' e U' d e e T' A"
    """
    moves = scramble.split("/")
    # first level karnify skip the A and a
    for [i, m] in enumerate(moves):
        moves[i] = KARN[m] if m in KARN else m.replace(",", "")
    # second level karnify
    scramble = " ".join(moves)
    scramble = dict_replace(scramble, INV_NORM)
    return scramble

def unkarnify(scramble: str) -> str:
    """unkarnifies the scramble

    Args:
        scramble (str): the scramble, e.g. "A U' d3 e m' e U' d e e T' A"

    Returns:
        str: before karnifying, e.g. "A/-3,0/-1,2/1,-2/-1,2/3,3/-2,-2/3,3/-3,0/-1,2/3,3/3,3/-2,4/A"
    """
    # incomplete, has to decompose moves like 6-3, which I'm too lazy to do rn.
    return add_commas(" / ".join(
        filter(lambda a: a,dict_replace(dict_replace(scramble, NORM), NORM).split(" "))))

def add_commas(scramble: str) -> str:
    """adds commas to the scramble (part of unkarnifier)

    Args:
        scramble (str): e.g. "10/-30/-12/1-2/-12/33/-2-2/33/-30/-12/33/33/-24/-10"

    Returns:
        str: "1,0/-3,0/-1,2/1,-2/-1,2/3,3/-2,-2/3,3/-3,0/-1,2/3,3/3,3/-2,4/-1,0"
    """
    # slice separator
    sep = " / " if " / " in scramble else "/" if "/" in scramble else " "

    ret = scramble.split(sep)
    for i, m in enumerate(ret):
        if "," in m or m.lower() == "a":
            continue
        match len(m):
            case 2:
                ret[i] = m[0] + "," + m[1]
            case 3:
                ret[i] = m[0:2] + "," + m[2] if m[0] == "-" else m[0] + "," + m[1:]
            case 4:
                ret[i] = m[0:2] + "," + m[2:]
            case _:
                raise ValueError("this move is not valid: " + m)
    return sep.join(ret)

def legal_move(m: int) -> int:
    """makes the move legal

    Args:
        m (int): -10 ~ 12 (i think)

    Returns:
        int: -5 ~ 6
    """
    if m < -5:
        return m + 12
    elif m > 6:
        return m - 12
    return m

def add_moves(move1: str, move2: str) -> str:
    """adds two moves

    Args:
        move1 (str): e.g. "3,-3"
        move2 (str): e.g. "3,-3"

    Returns:
        str: e.g. "6,6"
    """
    # move1/2: "3,-3"
    m1 = move1.split(",")
    m2 = move2.split(",")
    result = [str(legal_move(int(m1[0]) + int(m2[0]))),
                str(legal_move(int(m1[1]) + int(m2[1])))]
    return ",".join(result)

def optimize(scramble: str) -> str:
    """optimizes a scramble by replacing optimizable sequences

    Args:
        scramble (str): e.g. "A/-3,-3/0,3/0,-3/-1,-4/-3,0/3,0/0,-3/0,3/a"

    Returns:
        str: a similarly-formatted optimizes scramble
    """
    while dict_replace(scramble, OPTIM) != scramble:
        # optimize needed
        moves = scramble.split("/")
        # moves now in ["A","3,-3", "3,0", "a"]
        at_slice = 0 # the index of the next move in "moves"
        cycle_completed = False
        for [i, char] in enumerate(scramble):
            # going over every character of scramble
            if cycle_completed:
                break
            if char != "/":
                continue
            at_slice += 1
            for optimable in OPTIM_KEYS:
                # avoid getting the last "a" also
                if len(scramble) - 1 - i < len(optimable):
                    continue
                if scramble[i: i+len(optimable)] == optimable:
                    # match!!
                    optimable_l = len(optimable.split("/"))
                    optim_to = OPTIM[optimable].split("/") # no slice at beginning/end
                    del_slice_num = optimable_l - len(optim_to)
                    if at_slice == 1:
                        # we at the beginning not at the end
                        if changes_alignment(int(optim_to.pop(0).split(",")[0])):
                            moves[0] = "A" if moves[0] == "a" else "a"
                        # else no change
                        # now we add the end move to the next move
                        moves[at_slice+optimable_l-2] = add_moves(moves[at_slice+optimable_l-2],
                                                                          optim_to.pop())
                    elif at_slice + optimable_l - 1 == len(moves):
                        # -1 cuz it starts&ends with slice
                        # we at the end not at the beginning
                        if changes_alignment(int(optim_to.pop().split(",")[0])):
                            moves.append("A" if moves.pop() == "a" else "a")
                        # else no change
                        # now we add the first move to the previous move
                        moves[at_slice-1] = add_moves(moves[at_slice-1], optim_to.pop(0))
                    else:
                        moves[at_slice-1] = add_moves(moves[at_slice-1], optim_to.pop(0))
                        moves[at_slice+optimable_l-2] = add_moves(moves[at_slice+optimable_l-2],
                                                                          optim_to.pop())
                    # now optim_to has the two merged moves removed
                    moves[at_slice: at_slice + del_slice_num] = optim_to
                    scramble = "/".join(moves)
                    cycle_completed = True
                    break

    return scramble

def get_scramble(end_state: str, obl: bool, invert_l: bool = True, max_slice: int = 20) -> list:
    """get a scramble for the obl or a state

    Args:
        end_state (str): either the end state, or the obl name
        obl (bool): whether it's an obl, if not, its a PBL, and end_state is a state
        invert_l (bool, optional): whether to count layer inverses as matches. Defaults to True.
        max_slice (int, optional): max slices to search. Defaults to 20.

    Returns:
        list: _description_
    """
    moves = ""
    if obl:
        [u, d] = end_state.split("/") # u: "left gem" and d: "knight"
        funct = is_obl
    else:
        [u, d] = [end_state[0:LAYERL], end_state[LAYERL:]]
        funct = is_pbl
    while True:
        if random.randint(0,1) == 0:
            # A start
            moves += "A/"
            top_a = True # bool: top misalign?
            state = SLICE_U if obl else SLICE_U_PBL
        else:
            # a start
            moves += "a/"
            top_a = False
            state = SLICE_D if obl else SLICE_D_PBL

        for i in range(max_slice-1):
            abf = rand_tm_move() if top_a else rand_bm_move()
            state = do_slice(move(state, abf[0], abf[1]))
            moves += f"{abf[0]},{abf[1]}/"
            if changes_alignment(abf[0]):
                top_a = not top_a
            # print(abf, state, moves, top_a)
            # if i == 1:
            #     sys.exit()
            if ((funct(state[0:LAYERL], u) and
                funct(state[LAYERL:], d)) or
                (invert_l and funct(state[0:LAYERL], d) and
                funct(state[LAYERL:], u))):
                current_a = "A" if top_a else "a"
                moves += current_a
                moves = optimize(moves)
                print(state)
                return [moves, karnify(moves)]
        moves = ""

# print(get_scramble("AA4BB3DD2CC1HH5FF7GG8EE6", False, max_slice=7))
# AA3BB2CC1DD4EE7FF6GG5HH8: oppopp
