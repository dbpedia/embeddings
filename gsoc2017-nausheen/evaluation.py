# -*- coding: utf-8 -*-
"""
Created on Fri May 26 19:25:46 2017

@author: nausheenfatma
"""

import numpy as np
import linecache
import operator

##########dictionary for entity###################
f=open("entity2id.txt","r")
entity_dict={}

for line in f:
    line=line.strip()
    tokens=line.split()
    entity_dict[tokens[0]]=int(tokens[1])
    
f=open("relation2id.txt","r")
relation_dict={}

for line in f:
    line=line.strip()
    tokens=line.split("\t")
    relation_dict[tokens[0]]=int(tokens[1])    



#def 


def predict_t(h,r):
    print "-------------predict_t-----------------"
    
    t_distance_list={}
    
    #print type(h),type(r)
    h_plus_r=np.add(h,r) #store value of h+r
    print h_plus_r
    
    f=open("/home/nausheenfatma/Summer2017/GSoC_2017/Code/KB2E-master/TransE/FB15kembeddings/entity2vec.bern","r")
    line_number=0
    for line in f : #check distance with each entity
        line=line.strip()
        
        t=[float(i) for i in line.split()]
        
        
        euclidean_dist=np.linalg.norm(h_plus_r-t)
        #print euclidean_dist
        t_distance_list[line_number]=euclidean_dist
        line_number=line_number+1
    sorted_t = sorted(t_distance_list.items(), key=operator.itemgetter(1), reverse=True)
    return  sorted_t[0:10]   #returns list of line number and distance
    
    
        #pp
        
########Mean Rank################################# 
#def mean_rank()   




##########Predict##############

f=open("data/test.txt")

for line in f:
    line=line.strip()
    line_tokens=line.split()
    h_key=line_tokens[0]
#    print "h_key",h_key
#    print "h_value",entity_dict[h_key]
#    print type(entity_dict[h_key])
    r_key=line_tokens[2]
#    print r_key
#    print type(r_key)
#    print relation_dict[r_key]
    
    try:
        #print entity_dict[h_key]+1
        h_value=linecache.getline('/home/nausheenfatma/Summer2017/GSoC_2017/Code/KB2E-master/TransE/FB15kembeddings/entity2vec.bern', entity_dict[h_key]+1)
        print type(h_value)
        list_h_value=[float(i) for i in h_value.split()]
        #print list_h_value
        #pp
        
        h=np.asarray(list_h_value)
        
        r_value=linecache.getline('/home/nausheenfatma/Summer2017/GSoC_2017/Code/KB2E-master/TransE/FB15kembeddings/relation2vec.bern', relation_dict[r_key]+1)
        
        list_r_value=[float(i) for i in r_value.split()]
        
        r=np.asarray(list_r_value)
        
        #print r
    except:
        print "entity not found"
        pass
    
    
    #r=np.asarray()
    #print h,r
    predict_t(h,r)
    pp
    
    



