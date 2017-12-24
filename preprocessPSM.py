#!/usr/bin/python
# -*- coding:utf-8 -*-

from itertools import islice
from random import randint
import sys
import os
import time
path = "E:\Libsvm\libsvm-3.22\windows"
sys.path.append(path)
os.chdir(path)  # 请根据实际路径修改
from datetime import datetime
from grid import *
from svmutil import *
from numpy import *
import xgboost as xgb
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn import datasets as ds
import sklearn.metrics as skMetrics
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import train_test_split 
from sklearn.naive_bayes import GaussianNB 

from sklearn import preprocessing 
from sklearn.feature_selection import RFE  
from sklearn.feature_selection import RFECV 
from sklearn.ensemble import RandomForestClassifier

import filePath as fp


def preprocess():
    input_file_path = "E:\快盘\研三\data\yeast-01.tab"
    input_file = open(unicode(input_file_path, "utf-8"), "r")
    output_file_path = "E:\快盘\研三\data\yeast-01.scale"
    output_file = file(unicode(output_file_path, "utf-8"), "w+")
    for line in islice(input_file, 1, None):
        tokens = line.strip().replace(" ", "\t").split("\t")
        new_line = tokens[1]
        for i in range(2, 21):
            if tokens[i] == str(0):
                continue
            new_line += " " + str(i - 1) + ":" + tokens[i]
        output_file.write(new_line + "\n")
    output_file.close


def random_index(rate):
    """随机变量的概率函数"""
    #
    # 参数rate为list<int>
    #
    start = 0
    randnum = randint(1, sum(rate))
    for index, item in enumerate(rate):
        start += item
        if randnum <= start:
            break
    return index


def get_items(data_set, train_set, test_set):
    rate = [7, 3]
    res_flag = ["train", "test"]
    for item in data_set:
        if res_flag[random_index(rate)] == "train":
            train_set.append(item)
        else:
            test_set.append(item)


def split_file():
    input_file_path = "E:\快盘\研三\data\yeast-01.scale"
    input_file = open(unicode(input_file_path, "utf-8"), "r")
    output_file_path1 = "E:\快盘\研三\data\yeast-01-train.scale"
    output_file1 = file(unicode(output_file_path1, "utf-8"), "w+")
    output_file_path2 = "E:\快盘\研三\data\yeast-01-test.scale"
    output_file2 = file(unicode(output_file_path2, "utf-8"), "w+")
    data_set_positive = list()
    data_set_negative = list()
    train_set = list()
    test_set = list()
    for line in input_file:
        if line[0] == "1":
            data_set_positive.append(line)
        if line[0] == "-" and line[1] == "1":
            data_set_negative.append(line)
    get_items(data_set_positive, train_set, test_set)
    get_items(data_set_negative, train_set, test_set)
    print "length of trian set: ", len(train_set), "length of test set: ", len(test_set)
    for item in train_set:
        output_file1.write(item)
    for item in test_set:
        output_file2.write(item)

train_file="E:\快盘\研三\data\yeast-01-train.scale"
test_file="E:\快盘\研三\data\yeast-01-test.scale"
def svm():
    #rate, param = find_parameters('train.1.scale','-log2c -3,3,1 -log2g -3,3,1')
    # print rate,param
    print "read train data begin", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    y, x = svm_read_problem(unicode(train_file, "utf-8"))  # 读取自带数据
    print "read train data over",  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    yt, xt = svm_read_problem(unicode(test_file, "utf-8"))
    print "read test data over",  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print "train begin", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    m = svm_train(y, x, '-c 1.0 -g 8.0 -b 1')
    print "train end",  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    p_label, p_acc, p_val = svm_predict(yt, xt, m, '-b 1')
    ACC, MSE, SCC = evaluations(yt, p_label)

    out_file="E:\快盘\研三\data\yeast-01-out.scale"
    f = file(unicode(out_file, "utf-8"), "w+")
    for i in range(0, len(p_label)):
         f.write(str(p_label[i]) + " " + str(p_val[i][0]) +" " + str(p_val[i][1]) + "\n")
    f.close

class entry():
    entry_flag=0
    positive_pro=0.0
    negative_pro=0.0
    def __init__(self, entry_falg, positive_pro,negative_pro):
        self.entry_flag=int(entry_falg)
        self.positive_pro=float(positive_pro)
        self.negative_pro=float(negative_pro)
    def __cmp__(self,other):  
        return cmp(self.positive_pro, other.positive_pro) 

def calFDR(entry_list,num,method,fdr_list):
    target_num=0
    decoy_num=0
    res=0
    FDR_bound_list=[0.01,0.02,0.03,0.05,0.08,0.1]
    print "the number of entry:",num
    for FDR_bound in FDR_bound_list:
        target_num=0
        decoy_num=0
        res=0
        for entr in entry_list:
            if entr.entry_flag==1:
                target_num+=1
            else:
                decoy_num+=1
            fdr=float(decoy_num)/float(num)
            if fdr<FDR_bound:
                res=target_num
            if fdr>FDR_bound:
                break
        fdr_list.append(res)
        #print method," FDR:",FDR_bound,"target number:",res

def convertSortedEntry(y_test,y_probality,method):
    entry_list=list()
    for i in range(0,len(y_test)):
        if method=="xgb" or method=="ASSMBLE":
            entr=entry(y_test[i],y_probality[i],0.0)
        else:
            entr=entry(y_test[i],y_probality[i][0],y_probality[i][1])
        entry_list.append(entr)
    entry_list.sort(reverse=True)
    fdr_list=list()
    calFDR(entry_list, len(entry_list),method,fdr_list)
    return fdr_list

def libsvm(train_file,test_file):
    #rate, param = find_parameters('train.1.scale','-log2c -3,3,1 -log2g -3,3,1')
    # print rate,param
    y_train_pre, x_train_pre = svm_read_problem(unicode(train_file, "utf-8"))  # 读取自带数据
    y_test, x_test = svm_read_problem(unicode(test_file, "utf-8"))
    #20%的数据中随机取10%
    x_train, x_train_left, y_train, y_train_left = train_test_split(x_train_pre, y_train_pre, test_size=0.5, random_state=randint(1,1000))
    m = svm_train(y_train, x_train, '-c 1.0 -g 8.0 -b 1')

    p_label, p_acc, p_val = svm_predict(y_test, x_test, m, '-b 1')
    ACC, MSE, SCC = evaluations(y_test, p_label)
    print ACC,MSE,SCC
    return y_test,p_val
    convertSortedEntry(y_test,p_val,"svm")

def myxgboost(train_file,test_file):
    x_train_pre, y_train_pre, x_test, y_test = ds.load_svmlight_files( (unicode(train_file, "utf-8"), unicode(test_file, "utf-8")))
    x_train, x_train_left, y_train, y_train_left = train_test_split(x_train_pre, y_train_pre, test_size=0.5, random_state=randint(1,10000))
    #x_train =  preprocessing.MaxAbsScaler().fit_transform(x_train)
   # x_test = preprocessing.MaxAbsScaler().fit_transform(x_test)
    dtrain = xgb.DMatrix(x_train,y_train)
    dtest=xgb.DMatrix(x_test,y_test)
    y_test = dtest.get_label()
    param = {'booster':'gbtree','gamma':0.1,'max_depth':6,'lambda':3, 'eta':0.01, 'silent':0, 'objective':'binary:logistic' }
    num_round = 200
    bst = xgb.train(param, dtrain, num_round)
    # make prediction
    preds = bst.predict(dtest)
    return y_test,preds
    '''
    convertSortedEntry(y_test,preds,"xgboost")
    predictions = [round(value) for value in preds]
    accuracy = skMetrics.accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%"% (accuracy * 100.0))
    '''

def LR(train_file,test_file):
    x_train_pre, y_train_pre, x_test, y_test = ds.load_svmlight_files( (unicode(train_file, "utf-8"), unicode(test_file, "utf-8")))
    x_train, x_train_left, y_train, y_train_left = train_test_split(x_train_pre, y_train_pre, test_size=0.5, random_state=randint(1,10000))
   # x_train =  preprocessing.MaxAbsScaler().fit_transform(x_train)
   # x_test = preprocessing.MaxAbsScaler().fit_transform(x_test)
    lr=LogisticRegression(penalty='l2', C=1.0, solver='liblinear')
   # param_grid=[{'C':[1,10,20],'penalty':['l1','l2']}]
    #clf=GridSearchCV(lr,param_grid)
   # print clf.best_estimator_
    rfe = RFECV(estimator=lr, step=1)
    rfe.fit(x_train,y_train)
    y_pred=rfe.predict(x_test)
    y_probality=rfe.predict_proba(x_test)
    print skMetrics.accuracy_score(y_test, y_pred)
    return y_test,y_probality
    #convertSortedEntry(y_test,y_probality,"LR")

def NB(train_file,test_file):
    x_train, y_train, x_test, y_test = ds.load_svmlight_files( (unicode(train_file, "utf-8"), unicode(test_file, "utf-8")))
    #x_train =  preprocessing.MaxAbsScaler().fit_transform(x_train)
    #x_test = preprocessing.MaxAbsScaler().fit_transform(x_test)

    clf = GaussianNB()
    x_train=x_train.todense()
    x_test=x_test.todense()
    clf.fit(x_train, y_train)
    y_pred=clf.predict(x_test)
    y_probality=clf.predict_proba(x_test)
    print skMetrics.accuracy_score(y_test, y_pred)
    convertSortedEntry(y_test,y_probality,"NB")

def RF(train_file,test_file):
    x_train, y_train, x_test, y_test = ds.load_svmlight_files( (unicode(train_file, "utf-8"), unicode(test_file, "utf-8")))
    #x_train =  preprocessing.MaxAbsScaler().fit_transform(x_train)
    #x_test = preprocessing.MaxAbsScaler().fit_transform(x_test)

    clf = RandomForestClassifier()
    clf.fit(x_train, y_train)
    y_pred=clf.predict(x_test)
    y_probality=clf.predict_proba(x_test)
    print skMetrics.accuracy_score(y_test, y_pred)
    convertSortedEntry(y_test,y_probality,"RF")

def repeatMethod(train_file,test_file,method):
    res_file = file(unicode(fp.result_file, "utf-8"), "w+")
    fdr_res=[0,0,0,0,0,0]
    for k in range(0,100):
        if method=="xgb":
            y_test,pro=myxgboost(train_file,test_file)
        elif method=="svm":
            y_test,pro=libsvm(train_file,test_file)
        else:
            y_test,pro=LR(train_file,test_file)
        print k," over............................................................."
        fdr_list=convertSortedEntry(y_test,pro,method)
        print fdr_list
        for i in range(0,len(fdr_list)):
            if fdr_list[i]>fdr_res[i]:
                fdr_res[i]=fdr_list[i]
        line=""
        for number in [x*5.0/3.0 for x in fdr_list]:
            line=line+str(int(number))+"\t"
    res_file.write( "the result:"+line+"\n")

if __name__ == "__main__":
   repeatMethod(fp.ST_file_out_evalue_train,fp.ST_file_out_evalue_test,"xgb")
   # p=[p1[i][0]+p2[i]+p3[i][0] for i in range(0,len(y1))]
    
    

