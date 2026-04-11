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

        # remove quotes, then unkarnify
        R = "\n".join([unkarnify(re.sub(r"\"|\(|\)|\\|\/", "", i)).strip() for i in u])
        pyperclip.copy(R)
        print(R)
except KeyboardInterrupt:
    sys.exit()
