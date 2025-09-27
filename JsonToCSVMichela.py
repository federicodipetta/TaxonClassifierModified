import argparse
import pandas as pd
import json
import os

def main(json_path: list[str], csv_path: str) -> None:
    jsons = {}
    for path in json_path:
        with open(path) as f:
            jsons[path] = json.load(f)
    dfs = {}
    for path, json_file in jsons.items():
        # Estrai il nome del file JSON senza estensione
        json_name = os.path.splitext(os.path.basename(path))[0]
        # Aggiungi il prefisso al nome del dizionario
        prefixed_dfs = {f"{json_name}_{key}": value for key, value in convert_single(json_file).items()}
        dfs.update(prefixed_dfs)
    print(f"Converted {len(dfs)} dataframes")
    print(f"Saving to {csv_path}")
    for name, df in dfs.items():
        df.to_csv(f"{csv_path}/{name}.csv", index=False)

def convert_single(json: json) -> dict[str, pd.DataFrame]:
    dfs = dict()
    for comparison in json["data"]:
        name = get_name(comparison["title"])
        # lloyd_df = convert_single_linkage(comparison["auto"])
        # dfs[f"lloyd_{name}"] = lloyd_df 
        single_df = convert_single_linkage(comparison["single"])
        average_df = convert_single_linkage(comparison["average"])
        complete_df = convert_single_linkage(comparison["complete"])
        dfs[f"single_{name}"] = single_df
        dfs[f"average_{name}"] = average_df
        dfs[f"complete_{name}"] = complete_df
    return dfs

def convert_single_linkage(linkage: json) -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            "Id",
            "Organism",
            "Taxon",
            "Predicted",
            "True"
        ]
    )
    for prediction in linkage["predicted"]:
        df = df._append({
            "Id": prediction["Id"],
            "Organism": prediction["Organism"],
            "Taxon": prediction["Taxon"],
            "Predicted": prediction["Predicted"],
            "True": prediction["True"]
        }, ignore_index=True)
    return df

def get_name(title) -> str:
    title = title.split(".csv")[0]
    title = title.split("\\")[-1]
    return title

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Convert a cluster json file into csv")
    parse.add_argument("--json_folder", help="Path to the json folder", default="JSON-shape", required=False)
    parse.add_argument("--out", help="Path to save the csv files", default="CSV-shape", required=False)
    args = parse.parse_args()

    # Normalizza i percorsi
    json_folder = os.path.abspath(args.json_folder)
    csv_path = os.path.abspath(args.out)

    # Controlla se la cartella JSON esiste
    if not os.path.exists(json_folder):
        print(f"Error: The folder '{json_folder}' does not exist.")
        exit(1)

    # Crea la cartella di output se non esiste
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    # Trova tutti i file JSON nella cartella
    json_paths = [os.path.join(json_folder, file) for file in os.listdir(json_folder) if file.endswith(".json")]
    if len(json_paths) == 0:
        print(f"No JSON files found in '{json_folder}'")
        exit(1)

    # Esegui la conversione
    main(json_paths, csv_path)