import Aligners.alignerGC as gc
# Test
if __name__ == "__main__":
    aligner = gc.AlignerGCStruct("BenchMark/ct/Archaea/5S/CRW_5S_A_C_20.ct", "BenchMark/ct/Archaea/5S/CRW_5S_A_C_22.ct")
    print(aligner.get_distance())
    aligner = gc.AlignerGCSeq("BenchMark/ct/Archaea/5S/CRW_5S_A_C_20.ct", "BenchMark/ct/Archaea/5S/CRW_5S_A_C_22.ct")
    print(aligner.get_distance())
