"""this module provides valid oblp memo for visualization"""

import random


CORNERS = [[""], ["A", "B", "C", "D"],
          [ "AB", "AC", "AD", "BC", "BD", "CD"], ["ABC", "ABD", "ACD", "BCD"], ["ABCD"]]
TOTAL_CORNERS = ["", "A", "B", "C", "D",
           "AB", "AC", "AD", "BC", "BD", "CD", "ABC", "ABD", "ACD", "BCD", "ABCD"]
EDGES = [[""], ["1", "2", "3", "4"],
        [ "12", "13", "14", "23", "24", "34"], ["123", "124", "134", "234"], ["1234"]]
TOTAL_EDGES = ["", "1", "2", "3", "4",
         "12", "13", "14", "23", "24", "34", "123", "124", "134", "234", "1234"]
GROUPS = len(CORNERS)

try:
    while True:
        top_corner = random.choice(TOTAL_CORNERS)
        bottom_corner = random.choice(CORNERS[GROUPS - 1 - len(top_corner)])
        top_edge = random.choice(TOTAL_EDGES)
        bottom_edge = random.choice(EDGES[GROUPS - 1 - len(top_edge)])
        print(bottom_corner+bottom_edge+" "+top_corner+top_edge)
        input()
except KeyboardInterrupt:
    exit()
