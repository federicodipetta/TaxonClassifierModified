from Bio.Seq import Seq
import pandas as pd

def parse_ct(ct_file_name : str) -> pd.DataFrame:
    with open(ct_file_name, 'r') as file:
        lines = file.readlines()
    
    # Trova l'indice della prima riga valida
    start_index = 0
    for i, line in enumerate(lines):
        if len(line.split()) > 3 and line.split()[0].isdigit():
            start_index = i + 1
            break
    
    # Leggi le righe valide in un DataFrame
    df = pd.read_csv(ct_file_name, sep='\s+', skiprows=start_index, header=None,
                     names=['index', 'base', 'next', 'pair', 'position'], on_bad_lines='skip')
    
    return df

