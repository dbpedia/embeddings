# -*- coding: utf-8 -*-
# Code to convert standard dataset to compressed bin file
# input to HolE is a bin file. 
# Save into a dictionary usingg a pickle.

# Required files :  entity2id.txt,relation2id.txt,train.txt,test.txt,valid.txt for FB15K



#Author: Nausheen Fatma, 25th June 2017

import pickle


data={}

f=open("standard_data/entity2id.txt","r")
entity_dict={}


entities=[]

for line in f:
    line=line.strip()
    tokens=line.split()
    entity_dict[tokens[0]]=int(tokens[1])
    entities.append(tokens[0].decode('utf-8'))
    
data[u'entities']=entities
    
    
f=open("standard_data/relation2id.txt","r")
relation_dict={}


relation=[]

for line in f:
    line=line.strip()
    tokens=line.split("\t")
    stri="$$"+tokens[0]+"$$"
    #print stri
    relation_dict[tokens[0].strip()]=int(tokens[1])  
    relation.append(tokens[0].decode('utf-8'))
    
    
data[u'relations']=relation


f=open("standard_data/test.txt")
test_sub=[]

for line in f:
    line=line.strip()
    line_tokens=line.split()
    e1=line_tokens[0]
    e2=line_tokens[2]
    r=line_tokens[1]
    
    test_sub.append((entity_dict[e1],entity_dict[e2],relation_dict[r]))
    
data[u'test_subs']=test_sub
    

f=open("standard_data/train.txt")
train_sub=[]

for line in f:
    line=line.strip()
    line_tokens=line.split()
    e1=line_tokens[0]
    e2=line_tokens[2]
    r=line_tokens[1]
    
    train_sub.append((entity_dict[e1],entity_dict[e2],relation_dict[r]))
    
data[u'train_subs']=train_sub


f=open("standard_data/valid.txt")
valid_sub=[]

for line in f:
    line=line.strip()
    line_tokens=line.split()
    e1=line_tokens[0]
    e2=line_tokens[2]
    r=line_tokens[1]
    
    valid_sub.append((entity_dict[e1],entity_dict[e2],relation_dict[r]))
    
data[u'valid_subs']=valid_sub


pickle.dump( data, open( "data/DBpediaSet1.bin", "wb" ) )

