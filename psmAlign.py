#!/usr/bin/python
# -*- coding:utf-8 -*-

from itertools import islice
import random

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
    protein_flag="None"
    def __init__(self, psm_id, spectra_id, peaks, charge, precursor_mass, protein_id,protein_name, protein_mass,
        first_residue,last_residue,modification_number, matched_peaks, matched_fragment_ions, p_value,e_value,protein_flag):
        self.psm_id=psm_id
        self.spectra_id=int(spectra_id)
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
        self.protein_flag=protein_flag
    def __cmp__(self,other):  
        return cmp(self.matched_peaks, other.matched_peaks)  
def calFDR(psm_list,num):
    target_num=0
    decoy_num=0
    for psm in psm_list:
        if psm.protein_flag=="target":
            target_num+=1
        else:
            decoy_num+=1
        fdr=float(decoy_num)/float(num)
        if fdr<0.01:
            print "FDR:",fdr,"target number:",target_num,"shared peaks:",psm.matched_peaks
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
    for i in range(0,10):
        print psm_list[i].spectra_id
    calFDR(psm_list,len(psm_list))

if __name__ == "__main__":
    sss="abc"
    li=list(sss)
    random.shuffle(li)
    sre="".join(li)
    print sss,sre