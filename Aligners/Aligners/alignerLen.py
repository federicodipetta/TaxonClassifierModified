import pandas as pd
from parser.ctParser import parse_ct
class RNADistanceLen : 
    def __init__(self, file_name, file_name_2) -> None:
        self.df = parse_ct(file_name)
        self.df2 = parse_ct(file_name_2)
        self.distance = abs(len(self.df) - len(self.df2))
    def get_distance(self) -> int:
        return self.distance