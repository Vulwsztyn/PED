ids=[]
for filename in ['ids1.txt','ids2.txt','ids3.txt']:
    with open(filename) as f:
        content = f.readlines()
    ids += [x.strip() for x in content] 
print(len(ids))
print(len(list(set(ids))))
f = open("ids.txt", "w")
for i in list(set(ids)):
    f.write(i)
    f.write('\n')
f.close()