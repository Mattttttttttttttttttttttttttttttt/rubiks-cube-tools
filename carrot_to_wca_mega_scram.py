"""converts carrot notation to wca mega scramble"""

def converter(sign: list) -> str:
    """converts a ["-", "+"] to normal notation

    Args:
        sign (list): [move 1, move 2]

    Returns:
        str: string of wca notation
    """
    return f"R{sign[0]}{sign[0]} D{sign[1]}{sign[1]}"

while True:
    carrot = []
    try:
        for l in iter(input, ""):
            carrot.append(l)
    except KeyboardInterrupt:
        exit()
    for i, move in enumerate(carrot):
        move = move.strip()
        carrot[i] = move.split()
    for i, line in enumerate(carrot):
        carrot[i] = " ".join(converter(m) if m not in ["U", "U'"] else m for m in line)
    carrot = "\n".join(carrot)
    print(carrot)
