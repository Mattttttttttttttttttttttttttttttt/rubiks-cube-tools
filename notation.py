"""generates cube notation from natural code"""

CODE : str = ""
dictionary = {"i": "R", "k": "R'",
              "j": "U", "f": "U'",
              "d": "L", "e": "L'",
              "h": "F", "g": "F'",
              "w": "B", "o": "B'",
              "s": "D", "l": "D'",
              "c": "M", "x": "M'",
              "y": "S", "t": "S'",
              "5": "E", "6": "E'",
              "-": "f", "1": "f'",
              "n": "u", "b": "u'",
              "v": "l", "r": "l'",
              "u": "r", "m": "r'",
              "z": "d", "/": "d'",
              "0": "x", ".": "x'",
              ";": "y", "a": "y'",
              "p": "z", "q": "z'",
              "\n": "\n"}


while True:
    moves = []
    X = ""
    u = []
    for line in iter(input, X):
        u.append(line)
    CODE = "\n".join(u).strip().lower()
    if CODE.strip().lower() == "quit":
        exit()
    GO = False
    for i, move in enumerate(CODE):
        move = dictionary[move]
        if GO:
            GO = False
            continue
        elif i != (len(CODE) - 1):
            if CODE[i + 1] == CODE[i]:
                GO = True
                moves.append(move[0] + "2")
                continue
        moves.append(move)
    for i in moves:
        print(i, end = "" if i == "\n" else " ")
    print("")
