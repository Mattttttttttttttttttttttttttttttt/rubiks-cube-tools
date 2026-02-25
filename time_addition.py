"""this module adds times (e.g. 2.3, 1:45.678)"""

import sys
from helpers import minutes, seconds

print("enter twice when done. if there are no decimals, put \".0\"")
data: list[str] = []
try:
    for line in iter(input, ""):
        data.append(line)
except KeyboardInterrupt:
    sys.exit()
print(seconds(round(sum(minutes(i) for i in data), max(len(i.split(".")[1]) for i in data))))
