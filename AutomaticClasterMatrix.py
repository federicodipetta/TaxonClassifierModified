import os
import glob
import sys
import ClusterMatrix as cm
import numpy as np
import json as j


def find_files(pattern, path):
    return glob.glob(os.path.join(path, '**', pattern), recursive=True)

def list_files(path):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def compare_files(file1, file2):
    return cm.calculate_ClusterMatrix(file1, file2)


def compare_files2(file1, file2):
    return cm.calculate_ClusterMatrix_json(file1, file2)


def write_results_to_txt(results, output_file):
    with open(output_file, 'w') as f:
        f.write(results)


def write_results_to_json(json, output_file):
    with open(output_file, 'w') as f:
        j.dump(json, f, indent=4)

def main_Moleculus_new(dir1, dir2):
    files_dir1 = list_files(dir1)
    files_dir2 = list_files(dir2)
    results = ""
    json = []
    for file1 in files_dir1:
        for file2 in files_dir2:
            if os.path.basename(file1)[4:] == os.path.basename(file2)[4:]:
                print(f"Comparing {file1} with {file2}")
                #  results+= compare_files(file1, file2)
                results += "-------------------------------------------------------\n\n"
                tmp = compare_files2(file1, file2)
                tmp["key"] = os.path.basename(file1).replace('.csv', '')
                json.append(tmp)
                break
    write_results_to_json({"data": json}, 'output.json')

def main_Moleculus(dir1, dir2):
    patterns = ['*5S*', '*16S*', '*23S*']
    patterns2 = ['*5S-*', '*16S-*', '*23S-*']
    files_dir1 = []
    for pattern in patterns:
        files_dir1.append(find_files(pattern, dir1))
    files_dir1 = np.array(files_dir1).flatten()
    files_dir2 = []
    for pattern in patterns2:
        files_dir2.append(find_files(pattern, dir2))
    files_dir2 = np.array(files_dir2).flatten()
    results = ""
    json = []
    for file1 in files_dir1:
        for file2 in files_dir2:
            relative_path1 = os.path.relpath(os.path.dirname(file1), dir1)
            relative_path2 = os.path.relpath(os.path.dirname(file2), dir2)
            if relative_path1 == relative_path2 and os.path.basename(file1)[:3] == os.path.basename(file2)[:3]:
                results += "-------------------------------------------------------\n\n"
                tmp = compare_files2(file1, file2)
                tmp["key"] = os.path.basename(file1).replace('.csv', '')
                json.append(tmp)
                break
    write_results_to_json({"data": json}, 'output.json')

def main_molecules_experiment(dir1, dir2):
    """
    The folder is expected to be dir2 with a folder for each experiment, named Confronto1...ConfrontoN
    with a file named SERNAlignComparisonResults.csv in the folder or only a csv file.
    The dir2, with the labels, is a folder containing a list of csv named with the prefix of the experiment
    Confronto1-..., Confronto2-..., Confronto3-,..., ConfrontoN-...
    """
    results = ""
    json = []
    # Cerca tutte le cartelle Confronto* in dir1
    for exp_folder in os.listdir(dir1):
        exp_path = os.path.join(dir1, exp_folder)
        if os.path.isdir(exp_path) and exp_folder.startswith("Confronto"):
            # Cerca il file SERNAlignComparisonResults.csv nella cartella
            cmp_file = os.path.join(exp_path, "SERNAlignComparisonResults.csv")
            if not os.path.exists(cmp_file):
                # Se non esiste, cerca un csv qualsiasi nella cartella
                csvs = [f for f in os.listdir(exp_path) if f.endswith(".csv")]
                if not csvs:
                    print(f"Nessun file CSV trovato in {exp_path}")
                    continue
                cmp_file = os.path.join(exp_path, csvs[0])
            # Cerca il file delle label in dir2 con lo stesso prefisso
            label_prefix = exp_folder + "-"
            label_file = None
            for f in os.listdir(dir2):
                if f.startswith(label_prefix) and f.endswith(".csv"):
                    label_file = os.path.join(dir2, f)
                    break
            if label_file is None:
                print(f"Nessun file label trovato per {exp_folder} in {dir2}")
                continue
            print(f"Comparing {cmp_file} with {label_file}")
            tmp = compare_files2(label_file, cmp_file)
            tmp["key"] = exp_folder
            json.append(tmp)
    write_results_to_json({"data": json}, 'output.json')

def main_molecules_experiment_direct(dir1, dir2):
    """
    The folder dir1 is expected to contain files named Confronto1.csv, Confronto2.csv, ..., ConfrontoN.csv
    with the comparison results.
    The dir2, with the labels, is a folder containing a list of csv named with the prefix of the experiment
    Confronto1-..., Confronto2-..., Confronto3-,..., ConfrontoN-...
    """
    results = ""
    json = []
    
    # Cerca tutti i file Confronto*.csv direttamente in dir1
    for filename in os.listdir(dir1):
        if filename.startswith("Confronto") and filename.endswith(".csv"):
            # Estrai il nome dell'esperimento (es: "Confronto1" da "Confronto1.csv")
            exp_name = filename.replace(".csv", "")
            
            # Percorso completo del file dei risultati
            cmp_file = os.path.join(dir1, filename)
            
            # Cerca il file delle label in dir2 con lo stesso prefisso
            label_prefix = exp_name + "-"
            label_file = None
            
            for f in os.listdir(dir2):
                if f.startswith(label_prefix) and f.endswith(".csv"):
                    label_file = os.path.join(dir2, f)
                    break
            
            if label_file is None:
                print(f"Nessun file label trovato per {exp_name} in {dir2}")
                continue
            
            print(f"Comparing {cmp_file} with {label_file}")
            tmp = compare_files2(label_file, cmp_file)
            tmp["key"] = exp_name
            json.append(tmp)
    
    write_results_to_json({"data": json}, 'output.json')

if __name__ == "__main__":
    # Carica le impostazioni dal file JSON
    with open('settings.json') as f:
        settings = j.load(f)["automaticClasterMatrix"]

    # Percorsi delle directory
    dir1 = settings["dir1"]
    dir2 = settings["dir2"]
    type = settings["type"]
    if type == "normal":
        main_Moleculus(dir1, dir2)
    elif type == "new":
        main_Moleculus_new(dir1, dir2)
    elif type == "experiment":
        main_molecules_experiment(dir1, dir2)
    elif type == "experiment_direct":
        main_molecules_experiment_direct(dir1, dir2)
    else:
        print("Invalid type. Please use 'normal' or 'new'.")
        sys.exit(1)
 
