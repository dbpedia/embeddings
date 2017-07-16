f=open("train.txt","r")

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


f=open("test.txt","r")
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
        
        
f=open("valid.txt","r")
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
fw=open("entity2id.txt","w")

for key in id_dict:
    fw.write(key+"\t"+str(id_count)+"\n")
    id_count=id_count+1

fw.close()
    
id_count=0        
fw=open("relation2id.txt","w")

for key in relation_dict:
    fw.write(key+"\t"+str(id_count)+"\n")
    id_count=id_count+1

fw.close()

print "Done"
