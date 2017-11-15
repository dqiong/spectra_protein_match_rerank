#!/usr/bin/python
# -*- coding:utf-8 -*-


def countProtiens():
    protien_file=unicode("E:\快盘\研二文件\模板\data数据论文\Ecoli\Ecoli.fasta", "utf-8")
    protein_number=0
    for line in open(protien_file,"r"):
        if line[0]==">":
            protein_number+=1
    print "protein numbers:",protein_number

def processProtein():
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


if __name__ == "__main__":
    processProtein()