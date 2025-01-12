import pandas as pd
import Aligners.alignerLen as al
import json as js
import Aligners.alignerBP as bp
import Aligners.alignerGC as gc
import os 
def get_settings():
    return js.load(open('Aligners/benchmark.conf.json'))

def select_aligner() : 
    aligner = get_settings()["aligner"]
    if aligner == "len":
        return al.RNADistanceLen
    elif aligner == "bp":
        return bp.AlignerBP
    elif aligner == "gcStruc":
        return gc.AlignerGCStruct
    elif aligner == "gcSeq":
        return gc.AlignerGCSeq
    else:
        return None
    
def get_benchmark_folder(folder : str) -> pd.DataFrame:
    aligner = select_aligner()
    if aligner is None:
        return None
    folder = folder 
    print(os.path.abspath(folder))
    folders = os.listdir(os.path.abspath(folder))
    
    data_5S = pd.DataFrame(columns=["FileName1", "FileName2", "SERNADistance"])
    data_16S = pd.DataFrame(columns=["FileName1", "FileName2", "SERNADistance"])
    data_23S = pd.DataFrame(columns=["FileName1", "FileName2", "SERNADistance"])
    for folder_in_folders in folders:
        if folder_in_folders.endswith(".csv") or folder_in_folders.endswith(".DS_Store"):
            continue
        folder_S = folder + "/" +  folder_in_folders + "/"
        files = os.listdir(folder_S)
        files = [file for file in files if file.endswith(".ct")]
        list = []

        processed_files = []
        for file in files:
            print("file: ", file)
            processed_files.append(file)
            for file2 in files:
                if file != file2 and file2 not in processed_files:
                    distance = aligner(folder_S + file, folder_S + file2).get_distance()
                    list.append({"FileName1": file.replace(".ct", ""), "FileName2": file2.replace(".ct", ""), "SERNADistance": distance})
        if folder_in_folders.endswith("5S"):
            data_5S = pd.DataFrame(list)
        elif folder_in_folders.endswith("16S"):
            data_16S = pd.DataFrame(list)
        elif folder_in_folders.endswith("23S"):
            data_23S = pd.DataFrame(list)
    return {"5S": data_5S, "16S": data_16S, "23S": data_23S}

def write_results(folder : str, output_folder : str):
    archaea = get_benchmark_folder(folder + "Archaea")
    archaea["5S"].to_csv(output_folder + "Archaea/5S-distance.csv", index=False)
    archaea["16S"].to_csv(output_folder + "Archaea/16S-distance.csv", index=False)
    archaea["23S"].to_csv(output_folder + "Archaea/23S-distance.csv", index=False)

    bacteria = get_benchmark_folder(folder + "Bacteria")
    bacteria["5S"].to_csv(output_folder + "Bacteria/5S-distance.csv", index=False)
    bacteria["16S"].to_csv(output_folder + "Bacteria/16S-distance.csv", index=False)
    bacteria["23S"].to_csv(output_folder + "Bacteria/23S-distance.csv", index=False)
    
    eukarya = get_benchmark_folder(folder + "Eukaryota")
    eukarya["5S"].to_csv(output_folder + "Eukaryota/5S-distance.csv", index=False)
    eukarya["16S"].to_csv(output_folder + "Eukaryota/16S-distance.csv", index=False)
    eukarya["23S"].to_csv(output_folder + "Eukaryota/23S-distance.csv", index=False)

if __name__ == "__main__":
    settings = get_settings()
    output_folder = settings["output_folder"]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        os.makedirs(output_folder + "/Archaea")
        os.makedirs(output_folder + "/Bacteria")
        os.makedirs(output_folder + "/Eukaryota")
    write_results(settings["folder"], output_folder)