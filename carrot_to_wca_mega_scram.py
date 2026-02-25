"""converts carrot notation to wca mega scramble"""

import sys

def converter(sign: list) -> str:
    """converts a ["-", "+"] to normal notation

    Args:
        sign (list): [move 1, move 2]

    Returns:
        str: string of wca notation
    """
    return f"R{sign[0]}{sign[0]} D{sign[1]}{sign[1]}"

while True:
    c = []
    try:
        for l in iter(input, ""):
            c.append(l)
    except KeyboardInterrupt:
        sys.exit()
    for i, move in enumerate(c):
        move = move.strip()
        c[i] = move.split()
    for i, line in enumerate(c):
        c[i] = " ".join(converter(m) if m not in ["U", "U'"] else m for m in line)
    CARROT = "\n".join(c)
    print(CARROT)
