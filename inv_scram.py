"""this module generates the inverse scramble from a normal 3x3 scramble"""

def inverse(move: str) -> str:
    """inverts a move

    Args:
        move (str): the original move

    Returns:
        str: the inverted move
    """
    if len(move) == 1:
        return move + "'"
    elif move[-1] == "2":
        return move
    else:
        return move[0]

scram: list = input("normal scram here: ").split(" ")
inv = []
for i in range(1, len(scram) + 1):
    inv.append(inverse(scram[-i]))
print(f"\nnormal: {" ".join(scram)}\ninverse: {" ".join(inv)}")
