# -*- coding: utf-8 -*-
import dlib
import filePath as fp
from sklearn import datasets as ds

from sklearn.cross_validation import train_test_split 
from random import randint

class Item():
    lable=0
    score=0.0
    def __init__(self, lable, score):
        self.lable=int(lable)
        self.score=float(score)
    def __cmp__(self,other):  
        return cmp(self.score, other.score)

def calFDR(entry_list):
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
            if entr.lable>0:
                target_num+=1
            else:
                decoy_num+=1
            fdr=float(decoy_num)/float(num)
            if fdr<FDR_bound:
                res=target_num
            if fdr>FDR_bound:
                break

        print " FDR:",FDR_bound,"target number:",res

def svm_rank(train_file,test_file):
    x_train_pre, y_train_pre, x_test, y_test = ds.load_svmlight_files( (unicode(train_file, "utf-8"), unicode(test_file, "utf-8")))
    x_train, x_train_left, y_train, y_train_left = train_test_split(x_train_pre, y_train_pre, test_size=0.5, random_state=randint(1,1))
    print x_train[1]
    x_train=x_train.toarray()
    x_test=x_test.toarray()
    train_data = dlib.ranking_pair()
    train_index=0
    for i in y_train:
        if i>0:
            train_data.relevant.append(dlib.vector(x_train[train_index]))
        else:
            train_data.nonrelevant.append(dlib.vector(x_train[train_index]))
        train_index+=1
    
    trainer=dlib.svm_rank_trainer()
    trainer.c=10
    print "--------------"
    rank_modle=trainer.train(train_data)
 
    item_list=list()
    for lable,test_vector in y_test,x_test:
        item_temp=Item(lable,rank_modle(dlib.vector(test_vector)))
        item_list.append(item_temp)
    item_list.sort(reverse=True)
    calFDR(item_list)
    print item_list[0].lable,item_temp[0].score
    
    '''
    data.relevant.append(dlib.vector([1,0]))
    data.nonrelevant.append(dlib.vector([0,1]))
    trainer=dlib.svm_rank_trainer()
    trainer.c=10
    rank=trainer.train(data)
    print 'Ranking score for a relevant vector: ',rank(data.relevant[0])
    print 'Ranking score for a nonrelevant vector: ',rank(data.nonrelevant[0])
    print dlib.test_ranking_function(rank, data)

    queries = dlib.ranking_pairs()
    queries.append(data)
    queries.append(data)
    queries.append(data)
    queries.append(data)
    rank=trainer.train(queries)
    print dlib.cross_validate_ranking_trainer(trainer, queries, 4)
    '''

if __name__ == "__main__":
   svm_rank(fp.ST_file_out_evalue_train,fp.ST_file_out_evalue_test)