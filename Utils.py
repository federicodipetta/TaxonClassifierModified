import glob
import os
import pandas as pd
import json as j
def find_files(patterns : list, path) -> list[list[str]]:
    list_files = []
    for pattern in patterns:
        list_files.append(glob.glob(os.path.join(path, '**', pattern), recursive=True))
    return list_files

def open_csv(file):
    with open(file) as f:
        return f.read()
    
def write_results_to_txt(results, output_file):
    with open(output_file, 'w') as f:
        f.write(results)

def open_pandas(file):
    return pd.read_csv(file)

def write_results_to_json(json, output_file):
    with open(output_file, 'w') as f:
        data = {}
        data["data"] = json
        j.dump(data, f, indent=4)

def loadJson(file):
    with open(file) as f:
        return j.load(f)