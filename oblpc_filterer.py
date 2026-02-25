"""this module will generate viable OBLPC cases given base alg and extensions"""

import sys
import pyperclip
from get_scramble import is_obl, OBL, move, LAYERL, get_non_spe, do_moves, inverse, OBL_LEN
from get_scramble import OBL_TRANSLATION, SOLVED_U, shift, layer_flip_name, layer_flip

OBL_NAMING = {"solved": "-",

       "1c": "1c",
       "cadj": "ac",
       "copp": "oc",
       "3c": "3c",
       "4e": "4e",
       "3e": "3e",
       "line": "oe",
       "L": "ae",
       "1e": "1e",

       "left pair": "pm", # for U layer; we invert elsewhere
       "right pair": "pa",
       "left arrow": "am",
       "right arrow": "aa",
       "gem": "g",
       "left knight": "hl",
       "right knight": "hr",
       "left axe": "xl",
       "right axe": "xr",
       "squid": "s",
       "left thumb": "thm",
       "right thumb": "tha",
       "left bunny": "ua",
       "right bunny": "um",

       "shell": "sh",
       "left bird": "bm",
       "right bird": "ba",
       "hazard": "z",
       "left kite": "ka",
       "right kite": "km",
       "left cut": "cm",
       "right cut": "ca",
       "black T": "tu",
       "white T": "td",
       "left N": "nm",
       "right N": "na",
       "black tie": "iu",
       "white tie": "id",
       "left yoshi": "ya",
       "right yoshi": "ym"
}

LEN1 = ["-", "g", "s", "h"]

def get_obl(s: str, n: bool = False) -> str:
    """get the obl name of a cube state

    Args:
        s (str): e.g. "bBBbBBbBBbBBwWWwWWwWWwWW"
        n (bool): whether to use new names. defaults to false

    Returns:
        str: e.g. "good pair/pair" or "pa/pm"
    """
    u, d = get_obl_layer(s[0:LAYERL], n), get_obl_layer(s[LAYERL:], n)
    if n:
        if d[-1] in ["a", "m"]:
            # gotta invert
            a = ["a", "m"]
            a.remove(d[-1])
            d = d[:-1] + a[0]
        return u + d
    return get_non_spe(f"{u}/{d}")


def get_obl_layer(l: str, n: bool) -> str:
    """get the obl name of a layer

    Args:
        l (str): e.g. "bBBbBBbBBbBB"
        n (bool): whether to use new names

    Returns:
        str: e.g. "left pair"
    """
    d = OBL_NAMING if n else OBL
    for [o, o2] in d.items():
        if is_obl(l, o):
            return o2 if n else o
    raise ValueError("no such OBL correspond to: "+l)

def get_matt_memo(s: str) -> str:
    """get the matt tracing memo for a cube state

    Args:
        s (str): in cube shape, e.g. bBBbBBbBBbBBwWWwWWwWWwWW

    Returns:
        str: U names first, e.g. "- 12345678"
    """
    u, d = s[0:LAYERL], s[LAYERL:]
    u = shift(u, 3) if u[0].lower() != u[0] else shift(u, 2)
    d = shift(d, 3) if d[0].lower() != d[0] else shift(d, 2)
    # now everything is corners first
    mem = ""
    p = 1
    for x in range(0, LAYERL, 3):
        mem += str(p) if u[x] == "B" else ""
        mem += str(p+1) if u[x+2] == "b" else ""
        p += 2
    mem = "- " if mem == "" else mem+" "
    p = 1
    for x in range(0, LAYERL, 3):
        mem += str(p) if d[x] == "B" else ""
        mem += str(p+1) if d[x+2] == "b" else ""
        p += 2
    return mem + "-" if mem[-1] == " " else mem

def add_comma(ms: str) -> str:
    """adds comma into moves

    Args:
        m (str): "/21/30/"

    Returns:
        str: e.g. "/2,1/3,0/"
    """
    ml = ms.split("/")
    ret = []
    for m in ml:
        match len(m):
            case 0:
                ret.append("")
                continue
            case 2:
                x = 1
            case 3:
                x = 2 if m[0] == "-" else 1
            case 4:
                x = 2
            case _:
                raise ValueError("not a move: "+m+" in "+ms)
        ret.append(m[0:x]+","+m[x:])
    return "/".join(ret)

def get_obl_len(o: str) -> int:
    """get the optimal slice count of an obl

    Args:
        o (str): e.g. "good pair/pair"

    Returns:
        int: e.g. 2
    """
    try:
        return OBL_LEN[o]
    except KeyError:
        return OBL_LEN[layer_flip_name(o)]

def sorter(s: str) -> tuple:
    """sort helper for return_array

    Args:
        s (str): e.g. "tdna → kmka (4567 1238), -4"

    Returns:
        tuple: e.g. (-4, "natd", "natd", "kmka (4567 1238), -4")
                slice_saved, alphabetize TODO
    """
    ret = [s[-1]]
    u, d = "", ""
    [i, l] = s.split(" → ", 1) # i: tdna
    if len(i) % 2 == 0:
        u, d = i[0:len(i)//2], i[len(i)//2:]
    else:
        match len(i):
            case 3:
                u, d = (i[:1], i[1:]) if i[0] in LEN1 else (i[:2], i[2:])
            case 5:
                # one is tha/thm
                u, d = (i[:3], i[3:]) if i[0:2] == "th" else (i[:2], i[2:])
            case _:
                raise ValueError(s+" is not an obl case")
    ret.append(i if u < d else d + u)
    ret.append(l)
    return tuple(ret)

def load_easy_obls(cutoff: int) -> set[str]:
    """returns a compiled set of the cube state of the easy OBLs

    Args:
        cutoff (int): <= what slice to keep

    Returns:
        set[str]: compiled set
    """
    r = {move(SOLVED_U, -1, 0)} # starting with solved
    for [o, l] in OBL_LEN.items():
        if l > cutoff:
            continue
        for s in OBL_TRANSLATION[o]:
            sl = s.split("/")
            c = "".join([OBL[sl[0]], layer_flip(OBL[sl[1]])])
            for u in range(-3, 7, 3):
                for d in range(-5, 5, 3):
                    r.add(move(c, u, d))
            if sl[0] != sl[1]:
                sl = [sl[1], sl[0]]
                c = "".join([OBL[sl[0]], layer_flip(OBL[sl[1]])])
                for u in range(-3, 7, 3):
                    for d in range(-5, 5, 3):
                        r.add(move(c, u, d))
    return r

def main():
    """main program"""
    print("please input all your algs like /-1-2/-30/")
    cut = int(input("check up to what slice (<=): "))
    easyobls = load_easy_obls(cut)
    base = add_comma(input("base CS alg: "))
    while True:
        try:
            alt = input("alt CS alg (from the same angle!): ").replace("\\", "/").replace("|", "/")
            if "python" in alt:
                # oops
                sys.exit(0)
            try:
                alt = add_comma(alt)
                inv_alt = inverse(alt)
                save_cut = int(input("save at least how many slices: "))
                return_array = []
                for obl_state in easyobls:
                    end_state = do_moves(base, do_moves(inv_alt, obl_state))
                    slices_saved = (get_obl_len(get_obl(end_state)) -
                                    get_obl_len(get_obl(obl_state)) -
                                    (alt.count("/")-base.count("/")))
                    if slices_saved >= save_cut:
                        return_array.append(get_obl(end_state, True) + " → " +
                                            # f" ({get_matt_memo(end_state)}) → " +
                                            get_obl(obl_state, True) +
                                            f" ({get_matt_memo(obl_state)}), -" +
                                            str(slices_saved))
                return_array.sort(key=sorter, reverse=True)
                return_value = "\n".join(return_array)
                pyperclip.copy(return_value)
                print(return_value, end = "\n\n")
            except ValueError as e:
                print(str(e)+", your alg is prob wrong.")
                continue
        except KeyboardInterrupt:
            sys.exit(0)

# main()
# print(sorted(["natu → kakm (3456 5678), -4",
# "natu → kakm (1278 5678), -4",
# "natd → kakm (3456 1234), -4",
# "natd → kakm (1278 1234), -4",
# "tdna → kmka (4567 2345), -4",
# "tdna → kmka (4567 1678), -4",
# "iuna → kmka (2345 2345), -4",
# "iuna → kmka (2345 1678), -4",
# "idna → kmka (1678 2345), -4",
# "idna → kmka (1678 1678), -4",
# "tuna → kmka (1238 2345), -4",
# "tuna → kmka (1238 1678), -4"], key=sorter, reverse=True))
