import Utils as utils
import json
import os
import decimal
#get FolderName from file name
#input : archea/5S-filename.csv -> output : archea

def get_folder_name(file_name):
    return os.path.basename(os.path.dirname(file_name))
def format_file_name(file_name : str) -> str:
    return file_name.split('-')[0]
settings = json.load(open('settings.json'))["numberOfAlignments"]

output = {}
# the input folder must have this structure: 
# inputFolder
# ├── Archaea
# │   ├── 5S-filename.csv
# │   ├── 16S-filename.csv
# │   └── 23S-filename.csv
# ├── Bacteria
# │   ├── 5S-filename.cs
#...
# ├── Eukaryota
# │   ├── 5S-filename.csv
# ...

inputFolder = settings["input"]

patterns = ['*5S*', '*16S*', '*23S*']
folders = utils.find_files(patterns, inputFolder)
for folder in folders:
    for file in folder:
        file_name = format_file_name(os.path.basename(file))
        folder_name = get_folder_name(file)
        if folder_name not in output:
            output[folder_name] = {}
        if "structures" not in os.path.basename(file) and file_name not in output[folder_name] and os.path.isfile(file):
            csv = utils.open_pandas(file)
            csv = csv.dropna()
            csv["NumberOfAlignments"] = csv["NumberOfAlignments"].apply(decimal.Decimal)
            output[folder_name][file_name] = {}
            output[folder_name][file_name]["allRows"] = len(csv)
            output[folder_name][file_name]["WithOne"] = len(csv[csv["NumberOfAlignments"] == decimal.Decimal(1)])
            output[folder_name][file_name]["withMoreThanOne"] = len(csv[csv["NumberOfAlignments"] > decimal.Decimal(1)])
            #now the percentage
            output[folder_name][file_name]["percentageWithOne"] = output[folder_name][file_name]["WithOne"] / output[folder_name][file_name]["allRows"]
            output[folder_name][file_name]["percentageWithMoreThanOne"] = output[folder_name][file_name]["withMoreThanOne"] / output[folder_name][file_name]["allRows"]

utils.write_results_to_json(output, settings["output"])



