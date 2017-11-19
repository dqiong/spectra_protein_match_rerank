#!/usr/bin/python
# -*- coding:utf-8 -*-

from itertools import islice
import random
import preprocessPSM as psmRerank

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
        return cmp(self.e_value, other.e_value)  

def calFDR(psm_list,num):
    target_num=0
    decoy_num=0
    res=0
    FDR_bound_list=[0.01,0.02,0.03,0.05,0.08,0.1]
    psm_list.sort()
    print "the number of PSM:",num
    for FDR_bound in FDR_bound_list:
        target_num=0
        decoy_num=0
        res=0
        for psm in psm_list:
            if psm.protein_flag=="decoy":
                decoy_num+=1
            else:
                target_num+=1
            fdr=float(decoy_num)/float(num)
            if fdr<FDR_bound:
                res=target_num
            if fdr>FDR_bound:
                break
        print "MS-align+"," FDR:",FDR_bound,"target number:",res


def readPSM(input_file_path,psm_list):
    input_file = open(unicode(input_file_path, "utf-8"), "r")
    for line in islice(input_file, 1, None):
        tokens = line.strip().split("\t")
        protein_flag=tokens[9].split("_")[0]
        if protein_flag=="decoy" or protein_flag=="DECOY":
            protein_flag="decoy"
        else:
            protein_flag="target"
        psm=PSM(tokens[1],tokens[2],tokens[4],tokens[5],tokens[6],tokens[8],tokens[9],tokens[10],tokens[11],tokens[12],tokens[14],tokens[15],tokens[16],
        tokens[17],tokens[18],protein_flag)
        psm_list.append(psm)

def readTargetAndDecoy(input_file_path_target,input_file_path_decoy,psm_list):
    readPSM(input_file_path_target,psm_list)
    readPSM(input_file_path_decoy,psm_list)
    print "number of psm:",len(psm_list)
    calFDR(psm_list,len(psm_list))

def align2SVMFormat(psm_list,out_path):
    output_file = file(unicode(out_path, "utf-8"), "w+")
    for psm in psm_list:
        if psm.protein_flag=="decoy":
            new_line="0"
        else:
            new_line="1"
        new_line+=(" "+"1:"+str(psm.peaks)+" 2:"+str(psm.charge)+" 3:"+str(psm.precursor_mass)+" 4:"+str(psm.protein_mass)+
         " 5:"+str(psm.first_residue)+" 6:"+str(psm.last_residue)+" 7:"+str(psm.modification_number)+" 8:"+str(psm.matched_peaks)+
         " 9:"+str(psm.matched_fragment_ions)+" 10:"+str(psm.p_value)+" 11:"+str(psm.e_value)+"\n")
        output_file.write(new_line)
    output_file.close

def initPara():
    psm_list=list()
    input_file_path_target = "C:\Users\Administrator\Desktop\msalign+\msoutput\Ecoli_result_table.txt"
    input_file_path_decoy = "C:\Users\Administrator\Desktop\msalign+\msoutput\Ecoli_result_table_decoy.txt"
    readTargetAndDecoy(input_file_path_target,input_file_path_decoy,psm_list)
   # svmFormat_path="C:\Users\Administrator\Desktop\msalign+\msoutput\Ecoli_svm_format.txt"
   # align2SVMFormat(psm_list,svmFormat_path)
   # return svmFormat_path

if __name__ == "__main__":
    initPara()
    #test ST data
    '''
    input_path="C:\Users\Administrator\Desktop\msalign+\msoutput\ST_result_table_FDR.txt.pre"
    psm_list=list()
    readPSM(input_path,psm_list)
    calFDR(psm_list,len(psm_list))
    '''
    #psmRerank.LR(input_path)