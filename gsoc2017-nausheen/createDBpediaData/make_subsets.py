# -*- coding: utf-8 -*-
"""
Created on  July 9, 2017
@author: nausheenfatma
"""




#############################without properties(rdf:type,subject,same as),wikilinks, dbp and literals######################

def make_set1(full_file_path, set_file_path):
        f=open(full_file_path)
        fw=open(set_file_path,"w")        
        count=0
        for line in f:
            line=line.strip()
            tokens=line.split()
            if count%100==0:
                print count
            try:
                if tokens[2].startswith("<http") and not tokens[1]=="<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>" and not tokens[1]=="<http://dbpedia.org/ontology/wikiPageWikiLink>" and not tokens[1]=="<http://dbpedia.org/ontology/wikiPageExternalLink>" and not tokens[1]=="<http://www.w3.org/2002/07/owl#sameAs>" and not tokens[1].startswith("<http://dbpedia.org/property/")  and not tokens[1]=="<http://purl.org/dc/terms/subject>" and not tokens[1]=="<http://www.w3.org/2002/07/owl#sameAs>":
                    fw.write(line+"\n")
            except:
                print "Exception",line
            count=count+1
        fw.close()


make_set1("shuffled_test_new.txt","DBpedia_set1_test.txt")
print "Test made"
make_set1("shuffled_valid_new.txt","DBpedia_set1_valid.txt")
print "Valid made"
make_set1("shuffled_train.txt","DBpedia_set1_train.txt")
print "Train made"



##############################without literals#####################################################





def make_set2(full_file_path, set_file_path):
        f=open(full_file_path)
        fw=open(set_file_path,"w")        
        count=0
        for line in f:
            line=line.strip()
            tokens=line.split()
            if count%100==0:
                print count
            try:
                if tokens[2].startswith("<http") :
                    fw.write(line+"\n")
            except:
                print "Exception",line
            count=count+1
        fw.close()


make_set2("shuffled_test_new.txt","DBpedia_set2_test.txt")
print "Test made"
make_set2("shuffled_valid_new.txt","DBpedia_set2_valid.txt")
print "Valid made"
make_set2("shuffled_train.txt","DBpedia_set2_train.txt")
print "Train made"
 
##########################################################################################################






