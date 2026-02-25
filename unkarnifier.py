"""this module unkarnifies one/more move sequences"""

import re
import sys
import pyperclip
from get_scramble import unkarnify

try:
    while True:
        u = []
        for line in iter(input, ""):
            u.append(line)

        for i, l in enumerate(u):
            u[i] = re.sub(r"\"|\(|\)|\\|\/", "", l) # remove quotes
            u[i] = " " + u[i].strip() + " "

        R = "\n".join([unkarnify(i).strip() for i in u])
        pyperclip.copy(R)
        print(R)
except KeyboardInterrupt:
    sys.exit()
