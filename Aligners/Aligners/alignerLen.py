import pandas as pd
from parser.ctParser import parse_ct
class RNADistanceLen : 
    def __init__(self, df1, df2) -> None:
        self.df = df1
        self.df2 = df2
        self.distance = abs(len(self.df) - len(self.df2))
    def get_distance(self) -> int:
        return self.distance