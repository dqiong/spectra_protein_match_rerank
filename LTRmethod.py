# -*- coding: utf-8 -*-
import dlib
import filePath as fp
from sklearn import datasets as ds

from sklearn.cross_validation import train_test_split 
from random import randint

def svm_rank(train_file,test_file):
    x_train_pre, y_train_pre, x_test, y_test = ds.load_svmlight_files( (unicode(train_file, "utf-8"), unicode(test_file, "utf-8")))
    x_train, x_train_left, y_train, y_train_left = train_test_split(x_train_pre, y_train_pre, test_size=0.5, random_state=randint(1,1))
    print x_train[1]
    x_train=x_train.toarray()
    data = dlib.ranking_pair()
    train_index=0
    for i in y_train:
        if i>0:
            data.relevant.append(dlib.vector(x_train[train_index]))
        else:
            data.nonrelevant.append(dlib.vector(x_train[train_index]))
        train_index+=1
    

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