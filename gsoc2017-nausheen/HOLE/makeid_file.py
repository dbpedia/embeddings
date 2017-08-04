# -*- coding: utf-8 -*-
###Generates unique id for every entity and relation (predicate)
#Author: Nausheen Fatma, 25th June 2017


f=open("standard_data/train.txt","r")

id_dict={}
relation_dict={}

for line in f:
    line=line.strip()
    line_tokens=line.split()
    try:
        a=id_dict[line_tokens[0]]
    except:
        id_dict[line_tokens[0]]=0
    
    try:
        a=id_dict[line_tokens[2]]
    except:
        id_dict[line_tokens[2]]=0

    try:
        a=relation_dict[line_tokens[1]]
    except:
        relation_dict[line_tokens[1]]=0


f=open("standard_data/test.txt","r")
for line in f:
    line=line.strip()
    line_tokens=line.split()
    try:
        a=id_dict[line_tokens[0]]
    except:
        id_dict[line_tokens[0]]=0
    
    try:
        a=id_dict[line_tokens[2]]
    except:
        id_dict[line_tokens[2]]=0

    try:
        a=relation_dict[line_tokens[1]]
    except:
        relation_dict[line_tokens[1]]=0
        
        
f=open("standard_data/valid.txt","r")
for line in f:
    line=line.strip()
    line_tokens=line.split()
    try:
        a=id_dict[line_tokens[0]]
    except:
        id_dict[line_tokens[0]]=0
    
    try:
        a=id_dict[line_tokens[2]]
    except:
        id_dict[line_tokens[2]]=0

    try:
        a=relation_dict[line_tokens[1]]
    except:
        relation_dict[line_tokens[1]]=0    
        
        
id_count=0        
fw=open("standard_data/entity2id.txt","w")

for key in id_dict:
    fw.write(key+"\t"+str(id_count)+"\n")
    id_count=id_count+1

fw.close()
    
id_count=0        
fw=open("standard_data/relation2id.txt","w")

for key in relation_dict:
    fw.write(key+"\t"+str(id_count)+"\n")
    id_count=id_count+1

fw.close()

print "Done"
