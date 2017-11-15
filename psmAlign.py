#!/usr/bin/python
# -*- coding:utf-8 -*-

from itertools import islice

class PSM:
    psm_id=0
    spectra_id=0
    peaks=0
    charge=0
    precursor_mass=0
    protein_id=0
    protein_name="unKnown"
    protein_mass=0
    first_residue=0
    last_residue=0
    modification_number=0
    matched_peaks=0
    matched_fragment_ions=0
    p_value=0
    e_value=0
    protein_taget_decoy="None"
    def __init__(self, psm_id, spectra_id, peaks, charge, precursor_mass, protein_id,protein_name, protein_mass,
        first_residue,last_residue,modification_number, matched_peaks, matched_fragment_ions, p_value,e_value,protein_flag):
        self.psm_id=psm_id
        self.spectra_id=spectra_id
        self.peaks=peaks
        self.charge=charge
        self.precursor_mass=precursor_mass
        self.protein_id=protein_id
        self.protein_name=protein_name  
        self.protein_mass=protein_mass
        self.first_residue=first_residue
        self.last_residue=last_residue
        self.modification_number=modification_number
        self.matched_peaks=float(matched_peaks)
        self.matched_fragment_ions=float(matched_fragment_ions)
        self.p_value=float(p_value)
        self.e_value=float(e_value)
        self.protein_taget_decoy=protein_flag
    def __cmp__(self,other):  
        return cmp(self.matched_peaks, other.matched_peaks)  
def readPSM():
    psm_list=list()
    input_file_path = "C:\Users\Administrator\Desktop\msalign+\msoutput\Ecoli_result_table_FDR.txt.pre"
    input_file = open(unicode(input_file_path, "utf-8"), "r")
    for line in islice(input_file, 1, None):
        tokens = line.strip().replace(" ", "\t").split("\t")
        protein_flag=tokens[9].split("_")[0]
        psm=PSM(tokens[1],tokens[2],tokens[4],tokens[5],tokens[6],tokens[8],tokens[9],tokens[10],tokens[11],tokens[12],tokens[14],tokens[15],tokens[16],
        tokens[17],tokens[18],protein_flag)
        psm_list.append(psm)
    print "number of psm:",len(psm_list)
    psm_list.sort(reverse=True)
    print psm_list[0].matched_peaks,psm_list[len(psm_list)-1].matched_peaks


if __name__ == "__main__":
    readPSM()   
