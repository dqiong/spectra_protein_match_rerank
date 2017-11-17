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
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn import datasets as ds
import sklearn.metrics as skMetrics
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import train_test_split  

from sklearn import preprocessing 
from sklearn.feature_selection import RFE  
from sklearn.feature_selection import RFECV 


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

def libsvm(input_file):
    #rate, param = find_parameters('train.1.scale','-log2c -3,3,1 -log2g -3,3,1')
    # print rate,param
    y, x = svm_read_problem(unicode(input_file, "utf-8"))  # 读取自带数据
    print "read data over",  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    x_train, x_test, y_train, y_test = train_test_split(x_, y_, test_size=0.4, random_state=42)

    print "train begin", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    m = svm_train(y_train, x_train, '-c 1.0 -g 8.0 -b 1')
    print "train end",  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    p_label, p_acc, p_val = svm_predict(y_test, x_test, m, '-b 1')
    ACC, MSE, SCC = evaluations(y_test, p_label)
     
def LR(input_file):
    x_,y_=ds.load_svmlight_file(unicode(input_file, "utf-8")) 
    x_=  preprocessing.MaxAbsScaler().fit_transform(x_)
    x_train, x_test, y_train, y_test = train_test_split(x_, y_, test_size=0.4, random_state=42)
    lr=LogisticRegression(penalty='l2', C=1.0, solver='liblinear')
   # param_grid=[{'C':[1,10,20],'penalty':['l1','l2']}]
    #clf=GridSearchCV(lr,param_grid)
   # print clf.best_estimator_
    rfe = RFECV(estimator=lr, step=1)
    rfe.fit(x_train,y_train)
    y_pred=rfe.predict(x_test)
    y_probality=rfe.predict_proba(x_test)
    print skMetrics.accuracy_score(y_test, y_pred)


if __name__ == "__main__":
    input_path="C:\Users\Administrator\Desktop\msalign+\msoutput\Ecoli_svm_format.txt"
    libsvm(input_path)
