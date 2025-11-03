"""this module adds times (e.g. 2.3, 1:45.678)"""

# imports
from helpers import minutes, seconds

# code
print("enter twice when done.")
data: list[str] = []
data.append(input())
while data[-1] != "":
    data.append(input())
del data[-1]
print(seconds(round(sum([minutes(i) for i in data]), max([len(i.split(".")[1]) for i in data]))))
