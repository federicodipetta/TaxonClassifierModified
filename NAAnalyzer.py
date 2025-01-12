import pandas as pd
import matplotlib.pyplot as plt
import Utils as utils

# Carica i dati JSON
settings = utils.loadJson('settings.json')['NAAnalyzer']
data = utils.loadJson(settings["input"])['data']

# Converti i dati in un DataFrame
df = pd.json_normalize(data, sep='_')

# Calcola il totale delle righe
total_rows = df[[col for col in df.columns if 'allRows' in col]].sum().sum()

# Calcola il totale delle righe con un solo allineamento
total_with_one = df[[col for col in df.columns if 'WithOne' in col]].sum().sum()

# Calcola il totale delle righe con più di un allineamento
total_with_more_than_one = df[[col for col in df.columns if 'withMoreThanOne' in col]].sum().sum()

# Calcola le percentuali
percentage_with_one = (total_with_one / total_rows) * 100
percentage_with_more_than_one = (total_with_more_than_one / total_rows) * 100

# Crea un DataFrame per le percentuali totali
total_percentages = pd.DataFrame({
    'Category': ['WithOne', 'WithMoreThanOne'],
    'Percentage': [percentage_with_one, percentage_with_more_than_one]
})

# Visualizza il DataFrame delle percentuali totali
print(total_percentages)

