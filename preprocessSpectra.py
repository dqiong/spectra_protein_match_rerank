#!/usr/bin/python
# -*- coding:utf-8 -*-

from itertools import islice
from random import randint
import sys
import os
import time

class Peak:
    peak_number=0
    intensity=0
    three=0
    def __init__(self, peak_number,intensity,three):
        self.peak_number=peak_number
        self.intensity=intensity
        self.three=three

class Spectra:
    id=0
    scans=0
    activitation="HCD"
    precursor_mz=0
    precursor_charge=0
    precursor_mass=0
    peaks=list()
    def __init__(self, id, scans, activitation, mz, charge, mass, peaks):
        self.id=id
        self.scans=scans
        self.activitation=activitation
        self.precursor_mz=mz
        self.precursor_charge = charge
        self.precursor_mass=mass
        self.peaks=peaks
    def write_spectra(self,f):
        f.write("BEGIN IONS"+"\n")
        f.write("ID="+str(self.id)+"\n")
        f.write("ACTIVATION="+self.activitation+"\n")
        f.write("PRECURSOR_MZ="+str(self.precursor_mz)+"\n")
        f.write("PRECURSOR_CHARGE="+str(self.precursor_charge)+"\n")
        f.write("PRECURSOR_MASS="+str(self.precursor_mass)+"\n")
        for peak in self.peaks:
            f.write(peak)
        f.write("END IONS"+"\n"+"\n")
def init_para(scans,activitation,mz,charge,mass):
    scans=0
    activitation="HCD"
    mz=0
    charge=0
    mass=0
##数据转化为ma-align+格式
def processSpectra():
    spectra_file=unicode("C:\Users\Administrator\Desktop\msalign+\msinput\Yeast_12_1_msdeconv.msalign", "utf-8")
    out_file="C:\Users\Administrator\Desktop\msalign+\msinput\Ecoli_spectra.msalign"
    f = open(out_file, "w")
    spectra_number=0
    scans=0
    activitation="HCD"
    mz=0
    charge=0
    mass=0
    peaks=list()
    for line in open(spectra_file,"r"):
        if line.strip().split("=")[0]=="SCANS":
            scans=line.strip().split("=")[1]
        elif line.strip().split("=")[0]=="ACTIVATION":
            activitation=line.strip().split("=")[1]
        elif line.strip().split("=")[0]=="PRECURSOR_MZ":
            mz=float(line.strip().split("=")[1])
        elif line.strip().split("=")[0]=="PRECURSOR_CHARGE":
            charge=int(line.strip().split("=")[1])
        elif line.strip().split("=")[0]=="PRECURSOR_MASS":
            mass=float(line.strip().split("=")[1])
        elif len(line.strip().split("\t"))==3:
            peaks.append(line)
        elif line.strip()=="END IONS":
            if mass>2500 and len(peaks)>9:
                spectra_temp=Spectra(spectra_number,scans,activitation,mz,charge,mass,peaks)
                spectra_temp.write_spectra(f)
                spectra_number+=1
               # print str(mass)," ",str(len(peaks))
            init_para(scans,activitation,mz,charge,mass)
            peaks=[]
        else :
            continue
    print "spectra numbers:",spectra_number
    f.close
def processResult():
    input_file_path = "C:\Users\Administrator\Desktop\msalign+\msoutput\Ecoli_result_table_FDR.txt.pre"
    input_file = open(unicode(input_file_path, "utf-8"), "r")
    matched_target_protein_nbumber=0
    up15_numbers=0
    bound=14.99
    for line in islice(input_file, 1, None):
        tokens = line.strip().replace(" ", "\t").split("\t")
        if tokens[9].split("_")[0]=="target":
            matched_target_protein_nbumber+=1
        if float(tokens[15])>bound:
            up15_numbers+=1
    print "> 15 matched peaks number: ",up15_numbers
    print "matched target protein number:",matched_target_protein_nbumber
def align2SVMFmat():
    input_file_path = "C:\Users\Administrator\Desktop\msalign+\msinput\yeast-01.tab"
    input_file = open(unicode(input_file_path, "utf-8"), "r")
    output_file_path = "C:\Users\Administrator\Desktop\msalign+\msinput\yeast-01.scale"
    output_file = file(unicode(output_file_path, "utf-8"), "w+")
    for line in islice(input_file, 1, None):
        tokens = line.strip().replace(" ", "\t").split("\t")
        ###
        output_file.write(new_line + "\n")
    output_file.close

if __name__ == "__main__":
    processResult()