from parser.ctParser import parse_ct
from pandas import DataFrame
class AlignerGCStruct: 
    def __init__(self, df1, df2) -> None:
        self.df = df1
        self.df2 = df2
        self.distance = abs(self.__get_gc_number(self.df) - self.__get_gc_number(self.df2))

    def get_distance(self) -> int:
        return self.distance
    
    def __get_gc_number(self, df: DataFrame) -> int:
        '''
            return the number of GC pairs divided by all the pairs, divided by 2 becouse the pairs are counted twice
        '''
        # note: G-C  will be countend once becouse the we count only when the base is G and the pair is C
        # but also C-G is taken into account because the couple are showed two times in the ct file
        c_indices = df[df['base'] == 'C']['index']
        gc_pairs = df[(df['base'] == 'G') & (df['pair'].isin(c_indices))]
        return len(gc_pairs) / (len(df['pair'] != 0) / 2)
    
class AlignerGCSeq:
    def __init__(self, df1, df2) -> None:
        self.df = df1
        self.df2 = df2
        self.distance = abs(self.__get_gc_number(self.df) - self.__get_gc_number(self.df2))
    
    def get_distance(self) -> int:
        return self.distance
    
    def __get_gc_number(self, df: DataFrame) -> int:
        return (len(df[df['base'] == 'G']) + len(df[df['base'] == 'C'])) / len(df)
    
