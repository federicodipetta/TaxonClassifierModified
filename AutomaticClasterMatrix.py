import os
import glob
import ClusterMatrix as cm
import numpy as np
import json as j


def find_files(pattern, path):
    return glob.glob(os.path.join(path, '**', pattern), recursive=True)


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

settings = j.load(open('settings.json'))["automaticClasterMatrix"]


# Percorsi delle directory
dir1 = settings["dir1"]
dir2 = settings["dir2"]

# Pattern dei file
patterns = ['*5S*', '*16S*', '*23S*']
patterns2 = ['*5S-Sern*', '*16S-Sern*', '*23S-Sern*']
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
            #  results+= compare_files(file1, file2)
            results += "-------------------------------------------------------\n\n"
            tmp = compare_files2(file1, file2)
            tmp["key"] = os.path.basename(file1).replace('.csv', '')
            json.append(tmp)
            break
        # Scrivi i risultati in un file di testo
#write_results_to_txt(results, 'output.txt')
write_results_to_json({"data": json}, 'output.json')
