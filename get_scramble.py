"""generates random obl scrambles"""

import random
import re

OBL = {"1c": "BBwWWwWWwWWw",
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
# format is 24-character string, both corner first
CUBEL = 24
HALF_L = 6
LAYERL = 12
THREE_FOUR_L = 18
SOLVED_a = "BBbBBbBBbBBbWWwWWwWWwWWw"
SOLVED_A = "bBBbBBbBBbBBwWWwWWwWWwWW"
SLICE_a_PBL = "FF6GG7DD4AA1BB2CC3HH8EE5"
SLICE_a = "WWwWWwBBbBBbBBbBBbWWwWWw"
SLICE_A = "wWWwWWbBBbBBbBBbBBwWWwWW"
SLICE_A_PBL = "5FF6GG3DD4AA1BB2CC7HH8EE"
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
# TODO: add more moves?
KARNL = len(a_MOVES)
HIGHKARN = {
    # add spaces for de-ambiguity
    "U U' U U' ": "U4 ",
    "U' U U' U ": "U4' ",
    "D D' D D' ": "D4 ",
    "D' D D' D ": "D4' ",
    "u u' u u' ": "u4 ",
    "u' u u' u ": "u4' ",
    "d d' d d' ": "d4 ",
    "d' d d' d ": "d4' ",

    "U U' U ": "U3 ",
    "U' U U' ": "U3' ",
    "D D' D ": "D3 ",
    "D' D D' ": "D3' ",
    "u u' u ": "u3 ",
    "u' u u' ": "u3' ",
    "d d' d ": "d3 ",
    "d' d d' ": "d3' ",
    "F F' F ": "F3 ",
    "F' F F' ": "F3' ",
    "f f' f ": "f3 ",
    "f' f f' ": "f3' ",

    "U U' ": "W ",
    "U' U ": "W' ",
    "D D' ": "B ",
    "D' D ": "B' ",
    "u u' ": "w ",
    "u' u ": "w' ",
    "d d' ": "b ",
    "d' d ": "b' ",
    "F F' ": "F2 ",
    "F' F ": "F2' ",
    "f f' ": "f2 ",
    "f' f ": "f2' ",

    "U U ": "UU ",
    "U' U' ": "UU' ",
    "D D ": "DD ",
    "D' D' ": "DD' ",

    "60 ": "U2 ",
    "63 ": "U2D ",
    "6-3 ": "U2D' ",
    "66 ": "U2D2 ",
    "06 ": "D2 ",
    "36 ": "UD2",
    "-36 ": "U'D2"
}
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

    " 60 ": " U2 ",
    " 63 ": " U2D ",
    " 6-3 ": " U2D' ",
    " 66 ": " U2D2 ",
    " 06 ": " D2 ",
    " 36 ": " UD2",
    " -36 ": " U'D2",

    " 30 ": " U ",
    " -30 ": " U' ",
    " 03 ": " D ",
    " 0-3 ": " D' ",
    " 3-3 ": " E ",
    " -33 ": " E' ",
    " 33 ": " e ",
    " -3-3 ": " e' ",
    " 2-1 ": " u ",
    " -12 ": " d ",
    " -4-1 ": " F' ",
    " -1-4 ": " f' ",
    " 2-4 ": " T ",
    " -42 ": " t' ",
    " 22 ":" m ",
    " -1-1 ": " M' ",
    " 5-1 ":" u2 ",
    " -15 ": " d2 ",
    " -21 ":" u' ",
    " 1-2 ":" d' ",
    " 41 ":" F ",
    " 13 ":" f ",
    " -23 ": " T' ",
    " 4-2 ": " t ",
    " -2-2 ":" m' ",
    " 11 ": " M ",
    " -51 ": " u2' ",
    " 1-5 ": " d2' ",
    " -5-2 ": " K' ",
    " 52 ": " K ",
    " 25 ": " k ",
    " -2-5 ": " k' "
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

def replace_with_dict(s: str, d: dict) -> str:
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

def isOBL(layer: str, obl: str) -> bool:
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

def isPBL(layer: str, target: str) -> bool:
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
        layer = PBL_shift(layer)
        for m in range(4):
            if target == shift(layer, 3*m):
                return True
    return False

def randAMove():
    """return element of A_MOVES"""
    return list(A_MOVES)[random.randint(0,KARNL-1)]

def randaMove():
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
        if c == "b":
            return_val.append("w")
        elif c == "B":
            return_val.append("W")
        elif c == "w":
            return_val.append("b")
        elif c == "W":
            return_val.append("B")
        else:
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

def PBL_shift(a: str) -> str:
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
            ret.append(str(PBL_mini_shift(int(char))))
        else:
            ret.append(chr(PBL_mini_shift(ord(char) - ord("A") + 1)-1 + ord("A")))
    return "".join(ret)

def PBL_mini_shift(n: int) -> int:
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

def slice(cube: str) -> str:
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
    scramble = replace_with_dict(scramble, HIGHKARN)
    return scramble

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
    while replace_with_dict(scramble, OPTIM) != scramble:
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
        funct = isOBL
    else:
        [u, d] = [end_state[0:LAYERL], end_state[LAYERL:]]
        funct = isPBL
    while True:
        if random.randint(0,1) == 0:
            # A start
            moves += "A/"
            top_a = True # bool: top misalign?
            state = SLICE_A if obl else SLICE_A_PBL
        else:
            # a start
            moves += "a/"
            top_a = False
            state = SLICE_a if obl else SLICE_a_PBL

        for i in range(max_slice-1):
            abf = randAMove() if top_a else randaMove()
            state = slice(move(state, abf[0], abf[1]))
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
