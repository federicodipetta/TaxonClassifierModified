
from parser.ctParser import parse_ct


class AlignerBP : 
    def __init__(self, file_name_1, file_name_2) -> None:
        self.df = parse_ct(file_name_1)
        self.df2 = parse_ct(file_name_2)
        self.weak_bonds_1 = self.__build_weak_bonds(self.df)
        self.weak_bonds_2 = self.__build_weak_bonds(self.df2)
        self.distance_set = self.weak_bonds_1.symmetric_difference(self.weak_bonds_2)

    def get_distance(self) -> int:
        return len(self.distance_set)

    def __build_weak_bonds(self, df) -> set[tuple[int, int]]:
        # Filtra le righe dove 'pair' è diverso da 0
        df = df[df['pair'] != 0]
        
        # Crea un set di weak bonds
        weak_bonds = set()
        for row in df.itertuples(index=True):
            if row.pair > row.Index:
                weak_bonds.add((row.Index, row.pair))
        
        return weak_bonds
