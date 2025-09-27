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
                     names=['index', 'base', 'row', 'next', 'pair', 'position'], on_bad_lines='skip')
    
    return df

def parse_bpseq(bpseq_file_name : str) -> pd.DataFrame:
    with open(bpseq_file_name, 'r') as file:
        lines = file.readlines()
    
    # Trova l'indice della prima riga valida
    start_index = 0
    for i, line in enumerate(lines):
        if len(line.split()) > 3 and line.split()[0].isdigit():
            start_index = i + 1
            break
    
    # Leggi le righe valide in un DataFrame
    df = pd.read_csv(bpseq_file_name, sep='\s+', skiprows=start_index, header=None,
                     names=['index', 'base', 'pair'], on_bad_lines='skip')
    
    return df


def parse_db(db_file_name):
    """
    Parse a dot bracket notation file.
    Supports parentheses (), square brackets [], and braces {} for different base pair types.
    """
    with open(db_file_name, 'r') as file:
        lines = file.readlines()
    
    # Trova la sequenza e la struttura
    sequence = ""
    structure = ""
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('>') or line.startswith('#'):
            continue  # Salta commenti e intestazioni
        
        # Se contiene solo basi nucleotidiche, è una sequenza
        if all(c in 'ACGTU' for c in line.upper()):
            sequence += line.upper()
        # Se contiene caratteri di struttura, è la notazione dot-bracket
        elif any(c in '().<>[]{}' for c in line):
            structure += line
    
    if len(sequence) != len(structure):
        raise ValueError(f"Lunghezza sequenza ({len(sequence)}) e struttura ({len(structure)}) non corrispondono")
    
    # Verifica se ci sono caratteri non supportati
    supported_chars = set('().[]{}')
    unsupported_chars = set(structure) - supported_chars
    if unsupported_chars:
        raise ValueError(f"Caratteri non supportati nella notazione: {unsupported_chars}. Supportati: {supported_chars}")
    
    # Converti in formato simile a CT/BPSEQ
    pairs = []
    paren_stack = []   # Stack per parentesi ()
    bracket_stack = [] # Stack per quadre []
    brace_stack = []   # Stack per graffe {}
    
    for i, char in enumerate(structure):
        pos = i + 1  # +1 per indici 1-based
        
        if char == '(':
            paren_stack.append(pos)
        elif char == ')':
            if not paren_stack:
                raise ValueError(f"Parentesi chiusa ')' senza corrispondente aperta alla posizione {pos}")
            partner = paren_stack.pop()
            pairs.append((partner, pos))
        elif char == '[':
            bracket_stack.append(pos)
        elif char == ']':
            if not bracket_stack:
                raise ValueError(f"Quadra chiusa ']' senza corrispondente aperta alla posizione {pos}")
            partner = bracket_stack.pop()
            pairs.append((partner, pos))
        elif char == '{':
            brace_stack.append(pos)
        elif char == '}':
            if not brace_stack:
                raise ValueError(f"Graffa chiusa '}}' senza corrispondente aperta alla posizione {pos}")
            partner = brace_stack.pop()
            pairs.append((partner, pos))
        # '.' non fa nulla, indica base non accoppiata
    
    # Verifica che tutti gli stack siano vuoti
    if paren_stack:
        raise ValueError(f"Parentesi aperte '(' non chiuse alle posizioni: {paren_stack}")
    if bracket_stack:
        raise ValueError(f"Quadre aperte '[' non chiuse alle posizioni: {bracket_stack}")
    if brace_stack:
        raise ValueError(f"Graffe aperte '{{' non chiuse alle posizioni: {brace_stack}")
    
    # Crea il DataFrame
    data = []
    pair_dict = {}
    
    # Crea dizionario delle coppie
    for p1, p2 in pairs:
        pair_dict[p1] = p2
        pair_dict[p2] = p1
    
    # Crea le righe del DataFrame
    for i in range(len(sequence)):
        index = i + 1
        base = sequence[i]
        pair = pair_dict.get(index, 0)  # 0 se non è accoppiato
        
        data.append({
            'index': index,
            'base': base,
            'pair': pair
        })
    
    df = pd.DataFrame(data)
    return df
    
