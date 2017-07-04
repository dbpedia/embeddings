# -*- coding: utf-8 -*-
"""
Created on  March 13, 2017
@author: nausheenfatma
"""


from SPARQLWrapper import SPARQLWrapper,JSON
import re
import sys
import logging


sparql=SPARQLWrapper("http://dbpedia.org/sparql") #query the online DBpedia RDF database

def run_query(query):                #query returns triples #json
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            triple_list={}
            try :            
                results = sparql.query().convert()
                #print "len--",len(results["results"]["bindings"])
                i=0
                for result in results["results"]["bindings"]:
                    s=""
                    p=""
                    o=""
                    #print result
                    if "s" in result:
                        s=(result["s"]["value"])
                        s="<"+s+">"
                    if "p" in result:
                        p=(result["p"]["value"])
                        p="<"+p+">"
                        
                    if "o" in result :
                        o=(result["o"]["value"])
                    
                        if (re.match("http",o)):
                        #print "match"
                            o="<"+o+">"
                    triple_list[i]={"s":s,"p":p,"o":o}
                    i=i+1
            except :
                print "exception"
                pass
            #print "---"
            return triple_list  

###################################################################

def find_all_FB15k_subjects(FB15kfilepath):
    f=open(FB15kfilepath)
    a={}
    for line in f:
        line=line.strip()
        entity=line.split()[0]
        a[entity]=0
    
    return a
    
def find_DBpedia_equivalent_for_freebase_entity(entity_f):
    query="""
PREFIX owl:<http://www.w3.org/2002/07/owl#>
SELECT ?s WHERE {
    ?s (owl:sameAs|^owl:sameAs)* freebase:"""+entity_f+"""
}
"""
    list_one=run_query(query)
    DBpedia_entities_list=[]
    for triple in list_one.values(): 
        subject=triple["s"]
        if subject.startswith("<http://dbpedia.org/resource/"):
            DBpedia_entities_list.append(subject)

    return DBpedia_entities_list

def make_DBpedia_relationships_for_freebase_entities(entity_f_list):
    DBpedia_entities={}
    DBpedia_equivalent_list=[]
    m=0
    for entity_freebase in entity_f_list:
        m=m+1
        if m%100==0:
            print m
        
         # /m/01qscs of freebase is represented as freebase:m.01qscs in DBpedia
        entity_freebase=entity_freebase[1:]
        entity_freebase=entity_freebase.replace("/",".")
        #print entity_freebase
        DBpedia_equivalent_list=DBpedia_equivalent_list+find_DBpedia_equivalent_for_freebase_entity(entity_freebase)
    #    pp
    # take unique entities
    for entity in DBpedia_equivalent_list:
        DBpedia_entities[entity]=0
    return DBpedia_entities
    
def make_DBpedia_dataset(DBpedia_entities,datasetfilepath):
    fw=open(datasetfilepath,"w")
    m=0
    for entity_DBpedia in DBpedia_entities:
        m=m+1
        if m%100==0:
            print m
        query="""select  ?p ?o 
        where {"""+entity_DBpedia+""" ?p ?o .}"""
        list_one=run_query(query)
        
        for triple in list_one.values():
            s=entity_DBpedia
            p=triple["p"]
            o=triple["o"]
            #print p,o
            #print type(p)
            #print str(p).startswith("<http://dbpedia.org/resource/")
            #print str(o).startswith("<http://dbpedia.org/resource/")
            #limiting to only dbpedia resource entities
            if str(p).startswith("<http://dbpedia.org/")  and str(o).startswith("<http://dbpedia.org/"): 
                #print "Yes"
                fw.write(s+"\t"+p+"\t"+o+"\n")
    fw.close()
            



reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig()            
#print "Test==========================================="
#entity_f_list=find_all_FB15k_subjects("/media/nausheenfatma/01CFC8995ADC9230/gsoc2017/Datasets/FB15k/freebase_mtr100_mte100-test.txt")
#print "entity_f_list found",len(entity_f_list)
#
#DBpedia_entities=make_DBpedia_relationships_for_freebase_entities(entity_f_list)
#print "DBpedia_entities mappings found",len(DBpedia_entities)
#
#make_DBpedia_dataset(DBpedia_entities,"DBpedia-test.txt")
#print "Dataset made !"


#print "Train==========================================="
#entity_f_list=find_all_FB15k_subjects("/media/nausheenfatma/01CFC8995ADC9230/gsoc2017/Datasets/FB15k/freebase_mtr100_mte100-train.txt")
#print "entity_f_list found",len(entity_f_list)
#
#DBpedia_entities=make_DBpedia_relationships_for_freebase_entities(entity_f_list)
#print "DBpedia_entities mappings found",len(DBpedia_entities)
#
#make_DBpedia_dataset(DBpedia_entities,"DBpedia-train.txt")
#print "Dataset made !"


print "Train==========================================="
entity_f_list=find_all_FB15k_subjects("/media/nausheenfatma/01CFC8995ADC9230/gsoc2017/Datasets/FB15k/freebase_mtr100_mte100-valid.txt")
print "entity_f_list found",len(entity_f_list)

DBpedia_entities=make_DBpedia_relationships_for_freebase_entities(entity_f_list)
print "DBpedia_entities mappings found",len(DBpedia_entities)

make_DBpedia_dataset(DBpedia_entities,"DBpedia-valid.txt")
print "Dataset made !"



#print "Train=========================================="
#
#
#entity_f_list=find_all_FB15k_subjects("/media/nausheenfatma/01CFC8995ADC9230/gsoc2017/Datasets/FB15k/freebase_mtr100_mte100-train.txt")
#
#print "entity_f_list found",len(entity_f_list)
#
#DBpedia_entities=make_DBpedia_relationships_for_freebase_entities(entity_f_list)
#print "DBpedia_entities mappings found",len(DBpedia_entities)
#
#make_DBpedia_dataset(DBpedia_entities,"DBpedia-train.txt")
#print "Dataset made !"



#print "Valid==========================================="
#entity_f_list=find_all_FB15k_subjects("/media/nausheenfatma/01CFC8995ADC9230/gsoc2017/Datasets/FB15k/freebase_mtr100_mte100-valid.txt")
#print "entity_f_list found",len(entity_f_list)
#
#DBpedia_entities=make_DBpedia_relationships_for_freebase_entities(entity_f_list)
#print "DBpedia_entities mappings found",len(DBpedia_entities)
#
#make_DBpedia_dataset(DBpedia_entities,"DBpedia-valid.txt")
#print "Dataset made !"
#




query="""

PREFIX owl:<http://www.w3.org/2002/07/owl#>

SELECT ?s WHERE {
    ?s (owl:sameAs|^owl:sameAs)* freebase:m.082gq
}



"""

