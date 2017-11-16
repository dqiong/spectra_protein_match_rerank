#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
def countProtiens():
    protien_file=unicode("E:\快盘\研二文件\模板\data数据论文\Ecoli\Ecoli.fasta", "utf-8")
    protein_number=0
    for line in open(protien_file,"r"):
        if line[0]==">":
            protein_number+=1
    print "protein numbers:",protein_number

def processProteinName():
    protein_file=unicode("C:\Users\Administrator\Desktop\msalign+\msinput\Ecoli_database.fasta", "utf-8")
    out_file="C:\Users\Administrator\Desktop\msalign+\msinput\Ecoli_database_target.fasta"
    f = open(out_file, "w")
    protein_number=0
    for line in open(protein_file,"r"):
        if line[0]==">":
            f.write(">target_"+str(protein_number)+"\n")
            protein_number+=1
        else:
            f.write(line)
    print "protein numbers:",protein_number

def shuffleProtein():
    protein_file=unicode("C:\Users\Administrator\Desktop\msalign+\msinput\Ecoli_database.fasta", "utf-8")
    out_file="C:\Users\Administrator\Desktop\msalign+\msinput\Ecoli_database_shuffle.fasta"
    f = open(out_file, "w")
    protein_number=0
    temp_protein=""
    for line in open(protein_file,"r"):
        if line[0]==">":
            f.write(">decoy_"+str(protein_number)+"\n")
            protein_number+=1
        if line[0]!=">" and len(line.strip())>0:
            temp_protein+=line.strip()
        if len(line.strip())==0:
            p_list=list(temp_protein.strip())
            random.shuffle(p_list)
            protein_line_num=len(p_list)/70
            for i in range(0, protein_line_num):
                f.write("".join(p_list[70*i:70*(i+1)])+"\n")
            if len(p_list)%70>0:
                f.write("".join(p_list[70*protein_line_num:len(p_list)])+"\n\n")
            temp_protein=""
    print "shuffle over!"


if __name__ == "__main__":
    l=list()
    for i in range(0,5):
       l.append(i)
    print l
    l=l[1:3]
    print l
    shuffleProtein()