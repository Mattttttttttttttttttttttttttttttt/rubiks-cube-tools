def converter(sign):
    return f"R{sign[0]}{sign[0]} D{sign[1]}{sign[1]}"

while True:
    x = ""
    carrot = []
    for line in iter(input, x):
        carrot.append(line)
    for i in range(len(carrot)):
        carrot[i] = carrot[i].strip()
        carrot[i] = carrot[i].split(" ")
    for i in range(len(carrot)):
        for m in range(len(carrot[i])):
            if m != (len(carrot[i])-1):
                carrot[i][m] = converter(carrot[i][m])
        carrot[i] = " ".join(carrot[i])
    carrot = "\n".join(carrot)
    print(carrot)
