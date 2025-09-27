import pandas as pd
import Aligners.alignerLen as al
import json as js
import Aligners.alignerBP as bp
import Aligners.alignerGC as gc
import os 
import parser.ctParser as ct
def get_settings():
    return js.load(open('Aligners/benchmark.conf.json'))

def get_df_from_file(file : str) -> pd.DataFrame:
    if file.endswith(".ct"):
        return ct.parse_ct(file)
    elif file.endswith(".bpseq.txt"):
        return ct.parse_bpseq(file)
    elif file.endswith(".db"):
        return ct.parse_db(file)
    elif file.endswith(".txt"):
        return ct.parse_db(file)
    else:
        raise ValueError("Unsupported file format: " + file)

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
    
    list = pd.DataFrame(columns=["FileName1", "FileName2", "SERNADistance"])
    files = os.listdir(folder)
    files = [file for file in files if file.endswith(".txt")]
    list = []
    processed_files = []
    for file in files:
        print("file: ", file)
        processed_files.append(file)
        for file2 in files:
            if file != file2 and file2 not in processed_files:
                df1 = get_df_from_file(folder + "\\" + file)
                df2 = get_df_from_file(folder + "\\" + file2)
                distance = aligner(df1, df2).get_distance()
                list.append({"FileName1": file.replace(".txt", ""), "FileName2": file2.replace(".txt", ""), "SERNADistance": distance})

    return pd.DataFrame(list)

def write_results(folder : str, output_folder : str):
    name = os.path.abspath(folder)
    #prendo la cartella indietro come nome del file
    paths = name.split("\\")
    name = paths[-1]
    print("folder: ", folder)
    get_benchmark_folder(folder).to_csv(output_folder + "\\" + name + ".csv", index=False)

if __name__ == "__main__":
    settings = get_settings()
    output_folder = settings["output_folder"]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    write_results(settings["folder"], output_folder)