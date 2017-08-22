f_train=open("shuffled_train.txt")


entity_dict={}

k=0
for line in f_train:

	if k % 1000==0:
		print k
	k=k+1
	line=line.strip()
	line_tokens=line.split()
	if line.startswith("<http"):
		try:
			s=entity_dict[line_tokens[0]]
		except:
			entity_dict[line_tokens[0]]=0
		try:
			o=entity_dict[line_tokens[2]]
		except:
			try:
				if line_tokens[2].startswith("<http"):
					entity_dict[line_tokens[2]]=0
			except:
					pass

print "training dict made",len(	entity_dict)	
not_found=0
f_test=open("shuffled_test.txt")

f_test_new=open("shuffled_test_new.txt","w")



k=0
for line in f_test:
	if k % 1000==0:
		print k
	k=k+1
	line=line.strip()
	line_tokens=line.split()
	if line.startswith("<http"):
		count=0
		try:
			s=entity_dict[line_tokens[0]]
			count=count+1
		except:
			not_found=not_found+1
		try:
			o=entity_dict[line_tokens[2]]
			count=count+1
		except:
			not_found=not_found+1


		if count==2:
			f_test_new.write(line+"\n")
		
f_test_new.close()





f_valid=open("shuffled_valid.txt")
f_valid_new=open("shuffled_valid_new.txt","w")



k=0
for line in f_valid:
	if k % 1000==0:
		print k
	k=k+1
	line=line.strip()
	line_tokens=line.split()
	if line.startswith("<http"):
		count=0
		try:
			s=entity_dict[line_tokens[0]]
			count=count+1
		except:
			not_found=not_found+1
		try:
			o=entity_dict[line_tokens[2]]
			count=count+1
		except:
			not_found=not_found+1


		if count==2:
			f_valid_new.write(line+"\n")
		
f_valid_new.close()



print "not_found number",not_found
