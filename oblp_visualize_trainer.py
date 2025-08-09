"""this module provides valid oblp memo for visualization"""

import random


CORNER_0 = [""]
CORNER_1 = ["A", "B", "C", "D"]
CORNER_2 = ["AB", "AC", "AD", "BC", "BD", "CD"]
CORNER_3 = ["ABC", "ABD", "ACD", "BCD"]
CORNER_4 = ["ABCD"]
CORNERS = ["", "A", "B", "C", "D",
           "AB", "AC", "AD", "BC", "BD", "CD", "ABC", "ABD", "ACD", "BCD", "ABCD"]
PERMUTATIONS = len(CORNERS)

EDGE_0 = [""]
EDGE_1 = ["1", "2", "3", "4"]
EDGE_2 = ["12", "13", "14", "23", "24", "34"]
EDGE_3 = ["123", "124", "134", "234"]
EDGE_4 = ["1234"]
EDGES = ["", "1", "2", "3", "4",
         "12", "13", "14", "23", "24", "34", "123", "124", "134", "234", "1234"]

COMPLEMENT_CORNER = {0: CORNER_4, 
                     1: CORNER_3,
                     2: CORNER_2,
                     3: CORNER_1,
                     4: CORNER_0}
COMPLEMENT_EDGE = {0: EDGE_4,
                   1: EDGE_3,
                   2: EDGE_2,
                   3: EDGE_1,
                   4: EDGE_0}

try:
    while True:
        top_corner = random.choice(CORNERS)
        bottom_corner = random.choice(COMPLEMENT_CORNER[len(top_corner)])
        top_edge = random.choice(EDGES)
        bottom_edge = random.choice(COMPLEMENT_EDGE[len(top_edge)])
        print(bottom_corner+bottom_edge+" "+top_corner+top_edge)
        input()
except KeyboardInterrupt:
    exit()
